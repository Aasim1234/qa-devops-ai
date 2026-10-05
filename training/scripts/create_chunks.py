from pathlib import Path
import json
import re

INPUT = Path(
    r"S:\qa-devops-ai\data\processed\handbook.txt"
)

OUTPUT = Path(
    r"S:\qa-devops-ai\data\processed\chunks.jsonl"
)


def clean(text):

    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def split_into_sections(text):

    text = clean(text)

    # Keep paragraph/section boundaries wherever possible
    sections = re.split(
        r'\n\s*\n',
        text
    )

    sections = [
        section.strip()
        for section in sections
        if section.strip()
    ]

    return sections


def create_chunks(text):

    sections = split_into_sections(text)

    chunks = []

    current = ""
    chunk_id = 1

    for section in sections:

        # If adding this section keeps chunk reasonably small
        if len(current) + len(section) <= 900:

            if current:
                current += "\n\n"

            current += section

        else:

            if current:

                chunks.append({
                    "id": chunk_id,
                    "text": current
                })

                chunk_id += 1

            # Large individual section
            if len(section) > 900:

                parts = [
                    section[i:i + 800]
                    for i in range(
                        0,
                        len(section),
                        800
                    )
                ]

                for part in parts:

                    chunks.append({
                        "id": chunk_id,
                        "text": part.strip()
                    })

                    chunk_id += 1

                current = ""

            else:

                current = section

    if current:

        chunks.append({
            "id": chunk_id,
            "text": current
        })

    return chunks


def main():

    if not INPUT.exists():

        raise FileNotFoundError(
            f"Input file not found: {INPUT}"
        )

    text = INPUT.read_text(
        encoding="utf-8"
    )

    chunks = create_chunks(text)

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:

        for chunk in chunks:

            f.write(
                json.dumps(
                    chunk,
                    ensure_ascii=False
                ) + "\n"
            )

    print(
        f"Characters: {len(text)}"
    )

    print(
        f"Created chunks: {len(chunks)}"
    )

    print(
        f"Output: {OUTPUT}"
    )


if __name__ == "__main__":
    main()