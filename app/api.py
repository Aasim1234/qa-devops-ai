from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import requests
import numpy as np

app = FastAPI(title="QA DevOps AI")

# -----------------------------
# Configuration
# -----------------------------
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"

INDEX_PATH = r"S:\qa-devops-ai\models\combined.index"
METADATA_PATH = r"S:\qa-devops-ai\models\combined_metadata.pkl"

FAISS_TOP_K = 3
FINAL_CONTEXTS = 2
MIN_FAISS_SCORE = 0.25

# -----------------------------
# Load models
# -----------------------------
print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS knowledge base...")
index = faiss.read_index(INDEX_PATH)

with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

print(f"Knowledge base loaded: {index.ntotal} vectors")


# -----------------------------
# Request model
# -----------------------------
class AskRequest(BaseModel):
    question: str


# -----------------------------
# Health
# -----------------------------
@app.get("/")
def root():
    return {
        "service": "QA DevOps AI",
        "status": "running",
        "model": OLLAMA_MODEL
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "QA DevOps AI",
        "model": OLLAMA_MODEL,
        "vectors": index.ntotal
    }


# -----------------------------
# Knowledge retrieval
# -----------------------------
def retrieve_context(question: str):

    embedding = embedder.encode(
        [question],
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(
        embedding,
        FAISS_TOP_K
    )

    contexts = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        if float(score) < MIN_FAISS_SCORE:
            continue

        item = metadata[idx]

        if isinstance(item, dict):
            text = (
                item.get("text")
                or item.get("content")
                or item.get("chunk")
                or ""
            )
        else:
            text = str(item)

        if text:
            contexts.append(text)

        if len(contexts) >= FINAL_CONTEXTS:
            break

    return contexts


# -----------------------------
# Answer generation
# -----------------------------
def generate_answer(question: str, contexts):

    context_text = "\n\n---\n\n".join(contexts)

    prompt = f"""
You are a real-time DevOps and QA interview assistant.

Answer the interviewer's question directly.

IMPORTANT RULES:
- Be concise and natural.
- Do not think aloud.
- Do not explain your reasoning process.
- Do not repeat the question.
- For simple definitions: 1-3 sentences.
- For technical questions: give the key answer first, then important details.
- For troubleshooting scenarios: give a clear step-by-step approach.
- Mention commands when they are genuinely useful.
- Do not invent personal experience, metrics, companies, projects, or results.
- Use the supplied knowledge when relevant.
- If the supplied knowledge is insufficient, use reliable general DevOps knowledge.
- Do not dump the entire knowledge base into the answer.
- Sound like a candidate answering an interviewer, not like a textbook.

Knowledge context:
{context_text}

Interview question:
{question}

Answer:
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 160
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data.get("response", "").strip()


# -----------------------------
# Ask endpoint
# -----------------------------
@app.post("/ask")
def ask(request: AskRequest):

    question = request.question.strip()

    if not question:
        return {
            "answer": "Please provide a question."
        }

    contexts = retrieve_context(question)

    answer = generate_answer(
        question,
        contexts
    )

    return {
        "question": question,
        "answer": answer,
        "contexts_used": len(contexts)
    }


