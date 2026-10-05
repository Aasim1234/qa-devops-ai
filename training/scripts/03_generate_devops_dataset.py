import json
import random
from pathlib import Path

BASE_DIR = Path(r"S:\qa-devops-ai")

INPUT_FILE = BASE_DIR / "data" / "external" / "devops_clean.jsonl"
OUTPUT_FILE = BASE_DIR / "data" / "external" / "devops_large.jsonl"

TARGET_COUNT = 3000
SEED = 42

random.seed(SEED)


def load_jsonl(path):
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records


def save_jsonl(path, records):
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )


def classify_category(record):
    text = json.dumps(record).lower()

    categories = [
        "kubernetes",
        "docker",
        "terraform",
        "ansible",
        "jenkins",
        "github actions",
        "aws",
        "linux",
        "git",
        "prometheus",
        "grafana",
        "sre",
        "troubleshooting",
        "qa",
        "python",
        "bash",
        "networking",
    ]

    for category in categories:
        if category in text:
            return category

    return "devops"


def generate_variations(record, index):
    messages = record.get("messages", [])

    user_message = next(
        (m["content"] for m in messages if m["role"] == "user"),
        ""
    )

    assistant_message = next(
        (m["content"] for m in messages if m["role"] == "assistant"),
        ""
    )

    category = classify_category(record)

    variations = [
        user_message,
        f"Explain {user_message.lower()}",
        f"How would you answer this in a DevOps interview: {user_message}",
        f"Give a practical explanation of: {user_message}",
        f"What is the production perspective of: {user_message}",
    ]

    question = random.choice(variations)

    return {
        "id": f"devops_{index:05d}",
        "category": category,
        "difficulty": random.choice(
            ["beginner", "intermediate", "advanced"]
        ),
        "question_type": random.choice(
            [
                "definition",
                "explanation",
                "interview",
                "practical",
                "scenario"
            ]
        ),
        "question": question,
        "answer": assistant_message,
        "source": "general_devops_knowledge"
    }


def main():

    if not INPUT_FILE.exists():
        print("ERROR: Input dataset not found:")
        print(INPUT_FILE)
        return

    base_records = load_jsonl(INPUT_FILE)

    if not base_records:
        print("ERROR: Dataset is empty.")
        return

    print(f"Base records: {len(base_records)}")

    generated = []

    # Keep original records
    for i, record in enumerate(base_records):
        messages = record.get("messages", [])

        user_message = next(
            (m["content"] for m in messages if m["role"] == "user"),
            ""
        )

        assistant_message = next(
            (m["content"] for m in messages if m["role"] == "assistant"),
            ""
        )

        generated.append({
            "id": f"base_{i:05d}",
            "category": classify_category(record),
            "difficulty": "mixed",
            "question_type": "qa",
            "question": user_message,
            "answer": assistant_message,
            "source": "general_devops_knowledge"
        })

    counter = len(generated)

    # Generate variations
    while len(generated) < TARGET_COUNT:

        record = random.choice(base_records)

        item = generate_variations(
            record,
            counter
        )

        generated.append(item)

        counter += 1

    # Shuffle
    random.shuffle(generated)

    save_jsonl(
        OUTPUT_FILE,
        generated
    )

    print()
    print("===================================")
    print("Large dataset created")
    print("===================================")
    print(f"Records : {len(generated)}")
    print(f"Output  : {OUTPUT_FILE}")
    print("===================================")


if __name__ == "__main__":
    main()