import json
from pathlib import Path

BASE_DIR = Path(r"S:\qa-devops-ai")

CHUNKS_FILE = BASE_DIR / "data" / "processed" / "chunks.jsonl"
TRAIN_FILE = BASE_DIR / "data" / "final" / "devops_train.jsonl"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "combined_knowledge.jsonl"


def load_jsonl(path):
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records


def save_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )


def main():

    handbook = load_jsonl(CHUNKS_FILE)
    training = load_jsonl(TRAIN_FILE)

    combined = []

    # Handbook knowledge
    for i, item in enumerate(handbook):

        text = (
            item.get("text")
            or item.get("content")
            or ""
        )

        if not text.strip():
            continue

        combined.append({
            "id": f"handbook_{i:06d}",
            "source": "handbook",
            "category": "devops_handbook",
            "text": text.strip()
        })

    # External DevOps knowledge
    for i, item in enumerate(training):

        question = item.get("question", "").strip()
        answer = item.get("answer", "").strip()

        if not question or not answer:
            continue

        combined.append({
            "id": f"external_{i:06d}",
            "source": "general_devops_knowledge",
            "category": item.get("category", "devops"),
            "text": f"Question: {question}\nAnswer: {answer}"
        })

    save_jsonl(
        OUTPUT_FILE,
        combined
    )

    print("=" * 60)
    print("COMBINED KNOWLEDGE CREATED")
    print("=" * 60)
    print(f"Handbook records : {len(handbook)}")
    print(f"Training records : {len(training)}")
    print(f"Combined records : {len(combined)}")
    print()
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()