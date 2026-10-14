"""Run with python -m knowledge_agent."""

import argparse
from pathlib import Path
from .search import load_passages, search


def main() -> None:
    parser = argparse.ArgumentParser(description="Search company documents with source references.")
    parser.add_argument("question")
    parser.add_argument("--docs", type=Path, default=Path("sample_docs"))
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    try:
        matches = search(args.question, load_passages(args.docs), args.limit)
    except (ValueError, OSError, UnicodeError) as error:
        parser.exit(2, f"Error: {error}\n")
    if not matches:
        print("No matching passages found. Try different keywords or add relevant documents.")
        return
    print("Matching passages (keyword search; not an AI-generated answer):\n")
    for match in matches:
        passage = match.passage
        print(f"[{passage.source}:{passage.start_line}-{passage.end_line}]\n{passage.text}\n")


if __name__ == "__main__":
    main()
