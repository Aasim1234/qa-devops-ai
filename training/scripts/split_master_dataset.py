import json
import random
from pathlib import Path

BASE_DIR = Path(r"S:\qa-devops-ai")

INPUT_FILE = BASE_DIR / "data" / "final" / "master_dataset.jsonl"
OUTPUT_DIR = BASE_DIR / "data" / "final"

TRAIN_FILE = OUTPUT_DIR / "train.jsonl"
VAL_FILE = OUTPUT_DIR / "validation.jsonl"
TEST_FILE = OUTPUT_DIR / "test.jsonl"

TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
TEST_RATIO = 0.10

SEED = 42


def load_jsonl(path):
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def save_jsonl(path, records):
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )


def main():

    if not INPUT_FILE.exists():
        print(f"ERROR: Master dataset not found:")
        print(INPUT_FILE)
        return

    records = load_jsonl(INPUT_FILE)

    print(f"Total records: {len(records)}")

    random.seed(SEED)
    random.shuffle(records)

    total = len(records)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_records = records[:train_end]
    val_records = records[train_end:val_end]
    test_records = records[val_end:]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    save_jsonl(TRAIN_FILE, train_records)
    save_jsonl(VAL_FILE, val_records)
    save_jsonl(TEST_FILE, test_records)

    print()
    print("Dataset split completed.")
    print("--------------------------------")
    print(f"Train      : {len(train_records)}")
    print(f"Validation : {len(val_records)}")
    print(f"Test       : {len(test_records)}")
    print("--------------------------------")
    print(f"Train file      : {TRAIN_FILE}")
    print(f"Validation file : {VAL_FILE}")
    print(f"Test file       : {TEST_FILE}")


if __name__ == "__main__":
    main()