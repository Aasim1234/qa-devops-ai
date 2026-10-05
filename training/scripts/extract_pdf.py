from pathlib import Path
import json
import pypdf

PDF_PATH = Path(
    r"S:\qa-devops-ai\data\raw\Aasim_Raza_Complete_DevOps_Interview_Handbook.pdf"
)

OUTPUT_TEXT = Path(
    r"S:\qa-devops-ai\data\processed\handbook.txt"
)

OUTPUT_JSONL = Path(
    r"S:\qa-devops-ai\data\processed\handbook_pages.jsonl"
)


def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    print(f"Reading PDF: {PDF_PATH}")
    print(f"Size: {PDF_PATH.stat().st_size / 1024 / 1024:.2f} MB")

    reader = pypdf.PdfReader(str(PDF_PATH))

    print(f"Total pages: {len(reader.pages)}")

    all_text = []

    with OUTPUT_JSONL.open("w", encoding="utf-8") as jsonl_file:

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text() or ""

            record = {
                "page": page_number,
                "text": text
            }

            jsonl_file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            all_text.append(
                f"\n\n===== PAGE {page_number} =====\n\n{text}"
            )

            if page_number % 10 == 0:
                print(f"Processed {page_number} pages...")

    OUTPUT_TEXT.write_text(
        "".join(all_text),
        encoding="utf-8"
    )

    print("\nExtraction completed.")
    print(f"Text file : {OUTPUT_TEXT}")
    print(f"JSONL file: {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()