from pathlib import Path
import pickle
import faiss

from sentence_transformers import SentenceTransformer


INDEX = Path(
    r"S:\qa-devops-ai\models\handbook.index"
)

METADATA = Path(
    r"S:\qa-devops-ai\models\handbook_metadata.pkl"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 3
MIN_SIMILARITY = 0.55


def main():

    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    print("Loading FAISS index...")

    index = faiss.read_index(
        str(INDEX)
    )

    with METADATA.open("rb") as f:
        records = pickle.load(f)

    print(
        f"Knowledge base: {len(records)} chunks"
    )

    while True:

        question = input(
            "\nQuestion "
            "(type 'exit' to stop): "
        ).strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        embedding = model.encode(
            [question],
            normalize_embeddings=True
        )

        scores, ids = index.search(
            embedding,
            TOP_K
        )

        print("\n" + "=" * 80)
        print("RETRIEVAL RESULTS")
        print("=" * 80)

        result_count = 0

        for rank, (score, idx) in enumerate(
            zip(scores[0], ids[0]),
            start=1
        ):

            if score < MIN_SIMILARITY:
                continue

            result_count += 1

            print(
                f"\nRESULT #{rank}"
            )

            print(
                f"Similarity: {score:.4f}"
            )

            print("-" * 80)

            text = records[idx]["text"]

            # Keep terminal output manageable
            print(text[:1200])

            print("-" * 80)

        if result_count == 0:

            print(
                "\nNo sufficiently relevant "
                "handbook content found."
            )


if __name__ == "__main__":
    main()