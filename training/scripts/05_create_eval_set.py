import json
import random
from pathlib import Path

BASE_DIR = Path(r"S:\qa-devops-ai")

INPUT_FILE = BASE_DIR / "data" / "external" / "devops_quality.jsonl"
EVAL_FILE = BASE_DIR / "data" / "evaluation" / "devops_eval.jsonl"
TRAIN_FILE = BASE_DIR / "data" / "final" / "devops_train.jsonl"

EVAL_COUNT = 100
SEED = 42


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
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():

    records = load_jsonl(INPUT_FILE)

    print(f"Input records: {len(records)}")

    random.seed(SEED)
    random.shuffle(records)

    evaluation = records[:EVAL_COUNT]
    training = records[EVAL_COUNT:]

    # Mark evaluation records
    for i, record in enumerate(evaluation, 1):
        record["eval_id"] = f"eval_{i:04d}"
        record["dataset"] = "evaluation"

    # Mark training records
    for record in training:
        record["dataset"] = "training"

    save_jsonl(EVAL_FILE, evaluation)
    save_jsonl(TRAIN_FILE, training)

    print()
    print("================================")
    print("DATASET SPLIT COMPLETED")
    print("================================")
    print(f"Evaluation records: {len(evaluation)}")
    print(f"Training records:   {len(training)}")
    print()
    print(f"Evaluation: {EVAL_FILE}")
    print(f"Training:   {TRAIN_FILE}")


if __name__ == "__main__":
    main()