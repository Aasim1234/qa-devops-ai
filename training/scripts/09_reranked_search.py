import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder


BASE_DIR = Path(r"S:\qa-devops-ai")

INDEX_FILE = BASE_DIR / "models" / "combined.index"
METADATA_FILE = BASE_DIR / "models" / "combined_metadata.pkl"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Cross-encoder reranker
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

FAISS_TOP_K = 10
FINAL_TOP_K = 2

# Start conservatively.
# We will tune this using the evaluation set.
RERANK_THRESHOLD = 0.0


def load_resources():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    with METADATA_FILE.open("rb") as f:
        metadata = pickle.load(f)

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    reranker = CrossEncoder(
        RERANKER_MODEL
    )

    return (
        index,
        metadata,
        embedding_model,
        reranker
    )


def search(
    question,
    index,
    metadata,
    embedding_model,
    reranker
):

    query_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    scores, indices = index.search(
        query_embedding,
        FAISS_TOP_K
    )

    candidates = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        idx = int(idx)

        if idx < 0 or idx >= len(metadata):
            continue

        item = metadata[idx]

        candidates.append({
            "faiss_score": float(score),
            "id": item.get("id"),
            "source": item.get("source"),
            "category": item.get("category"),
            "text": item.get("text", "")
        })

    if not candidates:
        return []

    pairs = [
        [
            question,
            candidate["text"]
        ]
        for candidate in candidates
    ]

    rerank_scores = reranker.predict(
        pairs
    )

    for candidate, score in zip(
        candidates,
        rerank_scores
    ):
        candidate["rerank_score"] = float(score)

    candidates.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    final = [
        item
        for item in candidates[:FINAL_TOP_K]
        if item["rerank_score"] >= RERANK_THRESHOLD
    ]

    return final


def main():

    print("Loading models...")

    (
        index,
        metadata,
        embedding_model,
        reranker
    ) = load_resources()

    print("Ready.")
    print()
    print("Type 'exit' to stop.")

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        results = search(
            question,
            index,
            metadata,
            embedding_model,
            reranker
        )

        print()
        print("=" * 70)

        if not results:

            print("No sufficiently relevant context found.")

        else:

            for i, result in enumerate(
                results,
                1
            ):

                print(
                    f"\nResult {i}"
                )

                print(
                    f"FAISS score  : "
                    f"{result['faiss_score']:.4f}"
                )

                print(
                    f"Rerank score : "
                    f"{result['rerank_score']:.4f}"
                )

                print(
                    f"Source       : "
                    f"{result['source']}"
                )

                print(
                    f"Category     : "
                    f"{result['category']}"
                )

                print(
                    f"Text         : "
                    f"{result['text'][:1000]}"
                )

        print("=" * 70)


if __name__ == "__main__":
    main()