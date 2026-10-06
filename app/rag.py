"""Lazy, thread-safe FAISS knowledge base.

The FAISS index, its metadata and the embedding model are loaded on first use
(or by the optional background warm-up), never at import time, so Uvicorn can
open its port immediately.

Query embeddings use fastembed (ONNX Runtime) with the same
sentence-transformers/all-MiniLM-L6-v2 model the index was built with. It
produces the same normalized vectors as sentence-transformers without pulling
in PyTorch, which keeps memory low enough for small cloud instances.
"""
import logging
import os
import pickle
import threading
import time
from dataclasses import dataclass

import numpy as np

from .config import Settings

log = logging.getLogger("qa_devops_ai.rag")


class RagUnavailable(Exception):
    """The knowledge base could not be loaded."""


@dataclass
class Context:
    text: str
    score: float
    source: str


class KnowledgeBase:
    def __init__(self, settings: Settings):
        self._s = settings
        self._lock = threading.Lock()
        self._index = None
        self._metadata = None
        self._embedder = None
        self._state = "not_loaded"  # not_loaded | loading | ready | error
        self._error: str | None = None
        self._failed_at = 0.0
        self._load_seconds: float | None = None

    # ------------------------------------------------------------------
    # Status (never triggers loading)
    # ------------------------------------------------------------------
    @property
    def state(self) -> str:
        return self._state

    def status(self) -> dict:
        return {
            "state": self._state,
            "vectors": self._index.ntotal if self._index is not None else None,
            "embedding_model": self._s.embedding_model,
            "index_file_present": self._s.index_path.is_file(),
            "metadata_file_present": self._s.metadata_path.is_file(),
            "load_seconds": self._load_seconds,
            "error": self._error,
        }

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------
    def ensure_loaded(self) -> None:
        if self._state == "ready":
            return

        # Only one thread loads; concurrent callers wait here and then reuse it.
        with self._lock:
            if self._state == "ready":
                return

            if (
                self._state == "error"
                and time.monotonic() - self._failed_at < self._s.rag_retry_seconds
            ):
                raise RagUnavailable(self._error)

            self._state = "loading"
            started = time.monotonic()
            try:
                self._load()
            except Exception as e:
                self._state = "error"
                self._error = f"{type(e).__name__}: {e}"
                self._failed_at = time.monotonic()
                log.exception("Knowledge base failed to load")
                raise RagUnavailable(self._error) from e

            self._load_seconds = round(time.monotonic() - started, 2)
            self._error = None
            self._state = "ready"
            log.info(
                "Knowledge base ready: %d vectors (%.1fs)",
                self._index.ntotal,
                self._load_seconds,
            )

    def _load(self) -> None:
        for path in (self._s.index_path, self._s.metadata_path):
            if not path.is_file():
                raise FileNotFoundError(
                    f"{path} not found. Build it with "
                    "training/scripts/08_build_combined_embeddings.py or set "
                    "INDEX_PATH / METADATA_PATH."
                )

        import faiss

        log.info("Loading FAISS index: %s", self._s.index_path)
        index = faiss.read_index(str(self._s.index_path))

        # The metadata file is produced by this project's own build script.
        with self._s.metadata_path.open("rb") as f:
            metadata = pickle.load(f)

        if len(metadata) != index.ntotal:
            raise ValueError(
                f"Metadata has {len(metadata)} records but the index has "
                f"{index.ntotal} vectors; rebuild both together."
            )

        embedder = self._load_embedder()

        probe = self._encode(embedder, "dimension check")
        if probe.shape[1] != index.d:
            raise ValueError(
                f"Embedding model '{self._s.embedding_model}' produces "
                f"{probe.shape[1]}-d vectors but the index expects {index.d}-d."
            )

        self._index = index
        self._metadata = metadata
        self._embedder = embedder

    def _load_embedder(self):
        cache_dir = self._s.model_cache_dir
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Keep Hugging Face downloads inside the project cache instead of the
        # user-wide ~/.cache/huggingface (unless HF_HOME is set explicitly).
        os.environ.setdefault("HF_HOME", str(cache_dir / "huggingface"))

        from fastembed import TextEmbedding

        log.info(
            "Loading embedding model %s (cache: %s)",
            self._s.embedding_model,
            cache_dir / "fastembed",
        )
        return TextEmbedding(
            model_name=self._s.embedding_model,
            cache_dir=str(cache_dir / "fastembed"),
        )

    @staticmethod
    def _encode(embedder, text: str) -> np.ndarray:
        vectors = np.asarray(list(embedder.embed([text])), dtype="float32")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------
    def search(self, question: str) -> list[Context]:
        self.ensure_loaded()

        embedding = self._encode(self._embedder, question)
        scores, indices = self._index.search(embedding, self._s.faiss_top_k)

        contexts: list[Context] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or float(score) < self._s.min_faiss_score:
                continue

            item = self._metadata[idx]
            if isinstance(item, dict):
                text = item.get("text") or item.get("content") or item.get("chunk") or ""
                source = item.get("source", "")
            else:
                text, source = str(item), ""

            if text:
                contexts.append(Context(text=text, score=float(score), source=source))

            if len(contexts) >= self._s.final_contexts:
                break

        return contexts


def knowledge_base_answer(contexts: list[Context], max_chars: int = 1200) -> str:
    """Turn retrieved chunks into a readable answer when no LLM is available."""
    # Prefer a curated "Question: ... Answer: ..." entry over a raw handbook slice.
    qa = next((c for c in contexts if c.text.lstrip().startswith("Question:")), None)
    if qa is not None and "Answer:" in qa.text:
        text = qa.text.split("Answer:", 1)[1].strip()
    else:
        lines = contexts[0].text.strip().splitlines()
        # Handbook chunks are fixed-size slices: drop the cut-off first/last lines
        # and the "===== PAGE n =====" markers.
        if len(lines) > 2:
            lines = lines[1:-1]
        text = "\n".join(l for l in lines if not l.strip().startswith("=====")).strip()

    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + " ..."
    return text
