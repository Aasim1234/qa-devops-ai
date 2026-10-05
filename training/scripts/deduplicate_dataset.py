from pathlib import Path
import json
import re

INPUT = Path(
    r"S:\qa-devops-ai\data\external\devops_expanded.jsonl"
)

OUTPUT = Path(
    r"S:\qa-devops-ai\data\external\devops_clean.jsonl"
)


def normalize(text):

    text = text.lower().strip()

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    text = re.sub(
        r'[?.!,]+$',
        '',
        text
    )

    return text


def main():

    seen = set()
    unique = []
    duplicates = 0

    with INPUT.open(
        encoding="utf-8"
    ) as f:

        for line in f:

            if not line.strip():
                continue

            record = json.loads(line)

            question = record[
                "messages"
            ][1]["content"]

            key = normalize(question)

            if key in seen:

                duplicates += 1
                continue

            seen.add(key)
            unique.append(record)

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:

        for record in unique:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    print(
        f"Original records : {len(unique) + duplicates}"
    )

    print(
        f"Duplicates       : {duplicates}"
    )

    print(
        f"Unique records   : {len(unique)}"
    )

    print(
        f"Output           : {OUTPUT}"
    )


if __name__ == "__main__":
    main()