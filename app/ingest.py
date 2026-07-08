"""
Document ingestion.

Loads every supported document,
splits it into chunks,
creates embeddings,
and stores everything in ChromaDB.
"""

import argparse

from app.loaders import DocumentLoader
from app.database import (
    add_documents,
    clear_database
)


def ingest_documents(
    rebuild: bool = False
) -> None:

    loader = DocumentLoader()

    print("=" * 60)
    print("Loading documents...")
    print("=" * 60)

    documents = loader.load()

    print(f"Loaded {len(documents)} document(s).")

    if not documents:
        print("Nothing to ingest.")
        return

    print()
    print("Splitting documents...")

    chunks = loader.split(documents)

    print(f"Created {len(chunks)} chunk(s).")

    if rebuild:
        print()
        print("Clearing database...")
        clear_database()

    print()
    print("Creating embeddings...")

    total = add_documents(chunks)

    print()
    print("=" * 60)
    print(f"Successfully indexed {total} chunks.")
    print("=" * 60)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rebuild",
        action="store_true"
    )

    args = parser.parse_args()
    ingest_documents(
        rebuild=args.rebuild
    )