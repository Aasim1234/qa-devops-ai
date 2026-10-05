from pathlib import Path
import json

INPUT = Path(
    r"S:\qa-devops-ai\data\external\devops_expanded.jsonl"
)


def main():

    records = []
    errors = []

    with INPUT.open(
        encoding="utf-8"
    ) as f:

        for line_number, line in enumerate(
            f,
            start=1
        ):

            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(
                    f"Line {line_number}: {e}"
                )
                continue

            if "messages" not in record:
                errors.append(
                    f"Line {line_number}: missing messages"
                )
                continue

            messages = record["messages"]

            if len(messages) != 3:
                errors.append(
                    f"Line {line_number}: "
                    f"expected 3 messages"
                )
                continue

            if messages[0]["role"] != "system":
                errors.append(
                    f"Line {line_number}: "
                    f"first message is not system"
                )

            if messages[1]["role"] != "user":
                errors.append(
                    f"Line {line_number}: "
                    f"second message is not user"
                )

            if messages[2]["role"] != "assistant":
                errors.append(
                    f"Line {line_number}: "
                    f"third message is not assistant"
                )

            question = messages[1]["content"].strip()
            answer = messages[2]["content"].strip()

            if not question:
                errors.append(
                    f"Line {line_number}: empty question"
                )

            if not answer:
                errors.append(
                    f"Line {line_number}: empty answer"
                )

            records.append(record)

    print("=" * 60)
    print("DATASET VALIDATION")
    print("=" * 60)

    print(f"Records checked : {len(records)}")
    print(f"Errors          : {len(errors)}")

    categories = {}

    for record in records:

        category = record.get(
            "category",
            "unknown"
        )

        categories[category] = (
            categories.get(category, 0) + 1
        )

    print("\nCategories:")

    for category, count in sorted(
        categories.items()
    ):
        print(
            f"  {category:20} {count}"
        )

    if errors:

        print("\nERRORS:")

        for error in errors[:20]:
            print(error)

    else:

        print("\n✓ Dataset structure is valid.")


if __name__ == "__main__":
    main()