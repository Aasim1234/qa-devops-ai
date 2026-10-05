import json
import re
from pathlib import Path
from collections import Counter

BASE_DIR = Path(r"S:\qa-devops-ai")

INPUT_FILE = BASE_DIR / "data" / "external" / "devops_large.jsonl"
OUTPUT_FILE = BASE_DIR / "data" / "external" / "devops_quality.jsonl"
REPORT_FILE = BASE_DIR / "data" / "external" / "quality_report.json"


def normalize(text):
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[?.!,;:]+$", "", text)
    return text


def load_jsonl(path):
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()

            if not line:
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"Invalid JSON at line {line_number}")

    return records


def valid_record(record):
    required = [
        "question",
        "answer",
        "category"
    ]

    for field in required:
        if field not in record:
            return False

        if not str(record[field]).strip():
            return False

    question = str(record["question"]).strip()
    answer = str(record["answer"]).strip()

    # Remove extremely short records
    if len(question) < 10:
        return False

    if len(answer) < 20:
        return False

    return True


def main():

    if not INPUT_FILE.exists():
        print("ERROR: Input file not found:")
        print(INPUT_FILE)
        return

    records = load_jsonl(INPUT_FILE)

    print("=" * 50)
    print("DEVOPS DATASET QUALITY CONTROL")
    print("=" * 50)

    print(f"Input records: {len(records)}")

    valid = []
    invalid = 0

    for record in records:

        if valid_record(record):
            valid.append(record)
        else:
            invalid += 1

    print(f"Invalid/weak records removed: {invalid}")

    # Exact duplicate removal
    seen_questions = set()
    unique = []
    duplicates = 0

    for record in valid:

        key = normalize(record["question"])

        if key in seen_questions:
            duplicates += 1
            continue

        seen_questions.add(key)
        unique.append(record)

    print(f"Exact duplicates removed: {duplicates}")

    # Reassign clean IDs
    for index, record in enumerate(unique, 1):
        record["id"] = f"devops_clean_{index:05d}"

    # Category statistics
    categories = Counter(
        record.get("category", "unknown")
        for record in unique
    )

    print()
    print("CATEGORY DISTRIBUTION")
    print("-" * 40)

    for category, count in categories.most_common():
        print(f"{category:25} {count}")

    # Save
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:

        for record in unique:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    report = {
        "input_records": len(records),
        "invalid_removed": invalid,
        "exact_duplicates_removed": duplicates,
        "final_records": len(unique),
        "categories": dict(categories)
    }

    with REPORT_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 50)
    print("QUALITY CONTROL COMPLETED")
    print("=" * 50)
    print(f"Final records : {len(unique)}")
    print(f"Output        : {OUTPUT_FILE}")
    print(f"Report        : {REPORT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()