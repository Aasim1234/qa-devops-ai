"""QA DevOps AI - FastAPI entry point.

Run locally:   uvicorn app.api:app --host 0.0.0.0 --port 8000
Run on Render: uvicorn app.api:app --host 0.0.0.0 --port $PORT

Importing this module must stay cheap: no model downloads, no FAISS loading
and no network calls happen here, so Uvicorn can bind its port right away.
The knowledge base loads lazily (and optionally warms up in a background
thread after the server has started).
"""
import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config import settings

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)  # model-download request spam
log = logging.getLogger("qa_devops_ai")

log.info("Starting QA DevOps AI...")
log.info("Loading configuration...")

from .llm import LLMClient, LLMUnavailable  # noqa: E402
from .rag import KnowledgeBase, RagUnavailable, knowledge_base_answer  # noqa: E402

knowledge_base = KnowledgeBase(settings)
llm = LLMClient(settings)

log.info(
    "Configuration: llm_provider=%s llm_model=%s embedding_model=%s index=%s warmup=%s",
    llm.provider,
    llm.model or "-",
    settings.embedding_model,
    settings.index_path,
    settings.warmup_on_startup,
)


def _warm_up_knowledge_base() -> None:
    try:
        knowledge_base.ensure_loaded()
    except Exception:
        # Already logged by KnowledgeBase; /ask will retry later.
        log.warning("Knowledge base warm-up failed; the API keeps running without it.")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if settings.warmup_on_startup:
        # Daemon thread: the server starts listening without waiting for it.
        threading.Thread(
            target=_warm_up_knowledge_base, name="kb-warmup", daemon=True
        ).start()
        log.info("Knowledge base warm-up started in the background.")
    log.info("FastAPI startup complete.")
    yield


app = FastAPI(title=settings.service_name, version=settings.version, lifespan=lifespan)

# Chrome extension pages and local tools call this API from another origin.
if settings.cors_allow_origins:
    cors = {"allow_origins": settings.cors_allow_origins}
else:
    cors = {
        "allow_origin_regex": (
            r"^(chrome-extension://[a-p]{32}"
            r"|https?://(localhost|127\.0\.0\.1)(:\d+)?)$"
        )
    }
app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    allow_credentials=False,
    **cors,
)


class AskRequest(BaseModel):
    question: str = Field(..., max_length=settings.max_question_chars)


@app.get("/")
def root():
    return {
        "service": settings.service_name,
        "status": "running",
        "version": settings.version,
        "endpoints": ["GET /health", "GET /status", "POST /ask"],
    }


@app.get("/health")
def health():
    """Liveness check. Never loads models and never fails because of Ollama/LLM."""
    llm_available = llm.available()
    return {
        "status": "ok",
        "service": settings.service_name,
        "version": settings.version,
        "knowledge_base": knowledge_base.state,
        "llm_provider": llm.provider,
        "llm_available": llm_available,
        # Kept for the Chrome extension's status badge ("Online" vs "Ollama OFF").
        "ollama": llm_available,
    }


@app.get("/status")
def status():
    """Detailed component status (no secrets). Does not trigger model loading."""
    return {
        "service": settings.service_name,
        "version": settings.version,
        "knowledge_base": knowledge_base.status(),
        "llm": llm.status(),
        "kb_fallback": settings.kb_fallback,
    }


@app.post("/ask")
def ask(request: AskRequest):
    question = request.question.strip()

    if not question:
        return {"answer": "Please provide a question."}

    contexts = []
    rag_error = None
    try:
        contexts = knowledge_base.search(question)
    except RagUnavailable as e:
        rag_error = str(e)
        log.warning("Answering without knowledge base: %s", rag_error)

    try:
        answer = llm.generate(question, [c.text for c in contexts])
    except LLMUnavailable as e:
        llm_error = str(e)
        log.warning("LLM unavailable: %s", llm_error)

        if settings.kb_fallback and contexts:
            return {
                "question": question,
                "answer": (
                    "Note: AI model unavailable - showing the closest "
                    "knowledge-base answer.\n\n" + knowledge_base_answer(contexts)
                ),
                "contexts_used": len(contexts),
                "llm_used": False,
                "llm_error": llm_error,
            }

        detail = f"AI model unavailable: {llm_error}."
        if rag_error:
            detail += f" Knowledge base unavailable: {rag_error}"
        elif not contexts:
            detail += " No close knowledge-base match was found either."
        raise HTTPException(status_code=503, detail=detail)

    return {
        "question": question,
        "answer": answer,
        "contexts_used": len(contexts),
        "llm_used": True,
    }
