"""Script to build the Chroma index from PDFs in `data/pdfs/`.

Usage:
    python scripts/build_chroma.py --pdf-dir data/pdfs
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from rag.chroma_index import build_chroma_from_pdfs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-dir", default=os.path.join(ROOT, 'data', 'pdfs'), help="Directory containing PDFs")
    parser.add_argument("--persist-dir", default=None, help="Chroma persist directory (optional)")
    args = parser.parse_args()

    print(f"Building Chroma index from PDFs in {args.pdf_dir}...")
    vectordb = build_chroma_from_pdfs(args.pdf_dir, persist_directory=args.persist_dir)
    print("Chroma index built and persisted.")


if __name__ == '__main__':
    main()
