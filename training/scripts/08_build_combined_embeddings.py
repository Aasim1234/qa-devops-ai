import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(r"S:\qa-devops-ai")

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "combined_knowledge.jsonl"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

INDEX_FILE = BASE_DIR / "models" / "combined.index"
METADATA_FILE = BASE_DIR / "models" / "combined_metadata.pkl"

BATCH_SIZE = 16


def load_jsonl(path):
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records


def main():

    records = load_jsonl(INPUT_FILE)

    if not records:
        print("ERROR: No knowledge records found.")
        return

    print(f"Knowledge records: {len(records)}")

    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    texts = [
        record["text"]
        for record in records
    ]

    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    print(f"Embedding dimension: {dimension}")

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    BASE_DIR.joinpath("models").mkdir(
        parents=True,
        exist_ok=True
    )

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    with METADATA_FILE.open(
        "wb"
    ) as f:
        pickle.dump(
            records,
            f
        )

    print()
    print("=" * 60)
    print("COMBINED FAISS INDEX CREATED")
    print("=" * 60)
    print(f"Vectors : {index.ntotal}")
    print(f"Index   : {INDEX_FILE}")
    print(f"Metadata: {METADATA_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()