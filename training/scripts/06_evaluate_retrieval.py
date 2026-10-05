import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(r"S:\qa-devops-ai")

EVAL_FILE = BASE_DIR / "data" / "evaluation" / "devops_eval.jsonl"
INDEX_FILE = BASE_DIR / "models" / "handbook.index"
METADATA_FILE = BASE_DIR / "models" / "handbook_metadata.pkl"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5
RELEVANCE_THRESHOLD = 0.55


def load_jsonl(path):
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records


def normalize(text):
    return " ".join(str(text).lower().split())


def main():

    if not EVAL_FILE.exists():
        print("ERROR: Evaluation dataset not found.")
        return

    if not INDEX_FILE.exists():
        print("ERROR: FAISS index not found.")
        print(INDEX_FILE)
        return

    if not METADATA_FILE.exists():
        print("ERROR: Metadata file not found.")
        print(METADATA_FILE)
        return

    print("Loading evaluation dataset...")
    eval_records = load_jsonl(EVAL_FILE)

    print(f"Evaluation questions: {len(eval_records)}")

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Loading FAISS index...")
    index = faiss.read_index(str(INDEX_FILE))

    print("Loading metadata...")
    with METADATA_FILE.open("rb") as f:
        metadata = pickle.load(f)

    questions = []

    for record in eval_records:
        questions.append(
            record.get("question", "")
        )

    print("Generating embeddings...")

    embeddings = model.encode(
        questions,
        batch_size=16,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    scores, indices = index.search(
        embeddings,
        TOP_K
    )

    total = len(eval_records)
    above_threshold = 0
    low_confidence = 0

    print()
    print("=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)

    for i, record in enumerate(eval_records):

        best_score = float(scores[i][0])

        if best_score >= RELEVANCE_THRESHOLD:
            above_threshold += 1
        else:
            low_confidence += 1

        print()
        print(f"[{i + 1}/{total}]")
        print("Question:")
        print(record.get("question", ""))

        print(f"Best similarity: {best_score:.4f}")

        print("Retrieved:")
        for rank in range(TOP_K):

            idx = int(indices[i][rank])

            if idx < 0 or idx >= len(metadata):
                continue

            item = metadata[idx]

            if isinstance(item, dict):
                text = item.get(
                    "text",
                    item.get(
                        "content",
                        str(item)
                    )
                )
            else:
                text = str(item)

            text = text.replace("\n", " ")

            print(
                f"  {rank + 1}. "
                f"{float(scores[i][rank]):.4f} "
                f"{text[:250]}"
            )

    retrieval_rate = (
        above_threshold / total
        if total
        else 0
    )

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total questions        : {total}")
    print(f"Above threshold       : {above_threshold}")
    print(f"Low confidence        : {low_confidence}")
    print(
        f"Threshold pass rate   : "
        f"{retrieval_rate * 100:.2f}%"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()