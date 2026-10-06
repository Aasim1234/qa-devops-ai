"""Pre-download the embedding model and validate the knowledge base.

Intended for the Render build step:

    pip install -r requirements.txt && python -m app.prefetch

The model is cached under MODEL_CACHE_DIR (default: <project>/.cache), which is
part of the deployed build, so the running service does not download it again.
This script never fails the build: if anything goes wrong the API still starts
and loads the knowledge base lazily on first use.
"""
import logging
import sys

from .config import settings
from .rag import KnowledgeBase


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    log = logging.getLogger("qa_devops_ai.prefetch")

    try:
        kb = KnowledgeBase(settings)
        kb.ensure_loaded()
        log.info("Prefetch OK: %s vectors, model cached in %s",
                 kb.status()["vectors"], settings.model_cache_dir)
    except Exception as e:
        log.warning("Prefetch skipped (%s). The API will load lazily at runtime.", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
