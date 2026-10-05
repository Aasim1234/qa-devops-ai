from pathlib import Path
import json
import pickle

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


INPUT = Path(
    r"S:\qa-devops-ai\data\processed\chunks.jsonl"
)

OUTPUT_INDEX = Path(
    r"S:\qa-devops-ai\models\handbook.index"
)

OUTPUT_META = Path(
    r"S:\qa-devops-ai\models\handbook_metadata.pkl"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():

    if not INPUT.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {INPUT}"
        )

    print("Loading chunks...")

    records = []

    with INPUT.open(
        encoding="utf-8"
    ) as f:

        for line in f:

            if line.strip():

                records.append(
                    json.loads(line)
                )

    print(f"Loaded chunks: {len(records)}")

    texts = [
        record["text"]
        for record in records
    ]

    print()
    print("Loading embedding model:")
    print(MODEL_NAME)
    print()

    model = SentenceTransformer(
        MODEL_NAME
    )

    print("Creating embeddings...")
    print("This may take some time.")

    embeddings = model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    dimension = embeddings.shape[1]

    print(
        f"Embedding dimension: {dimension}"
    )

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    OUTPUT_INDEX.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    faiss.write_index(
        index,
        str(OUTPUT_INDEX)
    )

    with OUTPUT_META.open(
        "wb"
    ) as f:

        pickle.dump(
            records,
            f
        )

    print()
    print("====================================")
    print("Embedding creation completed")
    print("====================================")
    print()
    print(f"Index: {OUTPUT_INDEX}")
    print(f"Metadata: {OUTPUT_META}")
    print(f"Vectors: {index.ntotal}")


if __name__ == "__main__":
    main()