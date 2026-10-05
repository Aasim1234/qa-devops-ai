from pathlib import Path
import json
import random

EXTERNAL = Path(
    r"S:\qa-devops-ai\data\external\devops_clean.jsonl"
)

OUTPUT = Path(
    r"S:\qa-devops-ai\data\final\master_dataset.jsonl"
)


def load_jsonl(path):

    records = []

    with path.open(
        encoding="utf-8"
    ) as f:

        for line in f:

            if line.strip():

                records.append(
                    json.loads(line)
                )

    return records


def main():

    external = load_jsonl(
        EXTERNAL
    )

    print(
        f"External records: {len(external)}"
    )

    random.seed(42)

    random.shuffle(external)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:

        for record in external:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    print(
        f"Master dataset created: {OUTPUT}"
    )

    print(
        f"Total records: {len(external)}"
    )


if __name__ == "__main__":
    main()