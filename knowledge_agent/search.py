"""Dependency-free keyword retrieval baseline."""

from dataclasses import dataclass
from pathlib import Path
import re

STOP_WORDS = frozenset("a an the is are was were do does how what when where who why can could should would to of for in on at by with and or my our their employees employee get".split())


@dataclass(frozen=True)
class Passage:
    source: str
    start_line: int
    end_line: int
    text: str


@dataclass(frozen=True)
class Match:
    passage: Passage
    score: float


def terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP_WORDS


def load_passages(folder: Path) -> list[Passage]:
    if not folder.is_dir():
        raise ValueError(f"Document folder does not exist: {folder}")
    passages = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        buffer: list[str] = []
        start = 0
        for number, line in enumerate(lines + [""], start=1):
            if line.strip():
                if not buffer:
                    start = number
                buffer.append(line)
            elif buffer:
                passages.append(Passage(path.relative_to(folder).as_posix(), start, number - 1, "\n".join(buffer)))
                buffer = []
    return passages


def search(question: str, passages: list[Passage], limit: int = 3) -> list[Match]:
    if limit < 1:
        raise ValueError("Limit must be at least 1")
    query = terms(question)
    if not query:
        return []
    matches = []
    for passage in passages:
        overlap = query & terms(passage.text)
        if overlap:
            matches.append(Match(passage, len(overlap) / len(query)))
    return sorted(matches, key=lambda match: (-match.score, match.passage.source, match.passage.start_line))[:limit]
