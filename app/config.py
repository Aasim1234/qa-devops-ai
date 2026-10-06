"""Runtime configuration.

Everything is read from environment variables (and, for local development,
an optional .env file in the project root). Nothing here touches the network
or loads models, so importing this module is instant.
"""
import os
from dataclasses import dataclass
from pathlib import Path

# Project root (the folder that contains app/, models/, data/ ...).
BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv() -> None:
    env_file = BASE_DIR / ".env"
    if not env_file.is_file():
        return
    try:
        from dotenv import load_dotenv  # installed with uvicorn[standard]
    except ImportError:
        return
    # Real environment variables (e.g. on Render) always win over .env.
    load_dotenv(env_file, override=False)


_load_dotenv()


def _str(name: str, default: str = "") -> str:
    value = os.getenv(name, "").strip()
    return value or default


def _int(name: str, default: int) -> int:
    try:
        return int(_str(name, str(default)))
    except ValueError:
        return default


def _float(name: str, default: float) -> float:
    try:
        return float(_str(name, str(default)))
    except ValueError:
        return default


def _bool(name: str, default: bool) -> bool:
    value = _str(name).lower()
    if not value:
        return default
    return value in ("1", "true", "yes", "on")


def _path(name: str, default: Path) -> Path:
    """Absolute paths are used as-is; relative paths are resolved against BASE_DIR."""
    raw = _str(name)
    if not raw:
        return default
    path = Path(raw).expanduser()
    return path if path.is_absolute() else BASE_DIR / path


def _list(name: str) -> list[str]:
    return [item.strip() for item in _str(name).split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    service_name: str
    version: str
    log_level: str

    # Knowledge base (FAISS + metadata built by training/scripts/08_build_combined_embeddings.py)
    index_path: Path
    metadata_path: Path
    embedding_model: str
    model_cache_dir: Path
    faiss_top_k: int
    final_contexts: int
    min_faiss_score: float
    warmup_on_startup: bool
    rag_retry_seconds: int

    # Answer generation
    llm_provider: str  # "ollama" | "openai" | "none"
    llm_timeout: int
    llm_max_tokens: int
    llm_temperature: float
    ollama_base_url: str
    ollama_model: str
    llm_base_url: str
    llm_model: str
    llm_api_key: str
    kb_fallback: bool

    # HTTP
    cors_allow_origins: list[str]
    max_question_chars: int


def load_settings() -> Settings:
    ollama_url = _str("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    # Accept the old full endpoint form too (".../api/generate").
    if ollama_url.endswith("/api/generate"):
        ollama_url = ollama_url[: -len("/api/generate")]

    return Settings(
        service_name="QA DevOps AI",
        version="1.1.0",
        log_level=_str("LOG_LEVEL", "INFO").upper(),
        index_path=_path("INDEX_PATH", BASE_DIR / "models" / "combined.index"),
        metadata_path=_path("METADATA_PATH", BASE_DIR / "models" / "combined_metadata.pkl"),
        embedding_model=_str("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
        model_cache_dir=_path("MODEL_CACHE_DIR", BASE_DIR / ".cache"),
        faiss_top_k=_int("FAISS_TOP_K", 3),
        final_contexts=_int("FINAL_CONTEXTS", 2),
        min_faiss_score=_float("MIN_FAISS_SCORE", 0.25),
        warmup_on_startup=_bool("WARMUP_ON_STARTUP", True),
        rag_retry_seconds=_int("RAG_RETRY_SECONDS", 60),
        llm_provider=_str("LLM_PROVIDER", "ollama").lower(),
        llm_timeout=_int("LLM_TIMEOUT", 120),
        llm_max_tokens=_int("LLM_MAX_TOKENS", 160),
        llm_temperature=_float("LLM_TEMPERATURE", 0.2),
        ollama_base_url=ollama_url,
        ollama_model=_str("OLLAMA_MODEL", "llama3.2:1b"),
        llm_base_url=_str("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
        llm_model=_str("LLM_MODEL"),
        llm_api_key=_str("LLM_API_KEY"),
        kb_fallback=_bool("KB_FALLBACK", True),
        cors_allow_origins=_list("CORS_ALLOW_ORIGINS"),
        max_question_chars=_int("MAX_QUESTION_CHARS", 4000),
    )


settings = load_settings()
