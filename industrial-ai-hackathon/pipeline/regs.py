"""The regulation catalogue (regulations/index.json) and the paragraph index built by pipeline.index_pdfs."""

from __future__ import annotations

import json
import re
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_JSON = ROOT / "regulations" / "index.json"
INDEX_DIR = ROOT / "work" / "index"
OVERVIEW_CHARS = 3000


def slug(regulation: str) -> str:
    return "_".join(regulation.replace("/", " ").split())


@cache
def catalogue() -> dict[str, dict]:
    return {entry["regulation"]: entry for entry in json.loads(INDEX_JSON.read_text(encoding="utf-8"))}


def version_label(regulation: str, role: str = "base") -> str:
    return next(v["version_label"] for v in catalogue()[regulation]["versions"] if v["role"] == role)


@cache
def paragraphs(regulation: str, role: str = "base") -> tuple[dict, ...]:
    path = INDEX_DIR / f"{slug(regulation)}_{role}.jsonl"
    if not path.exists():
        raise SystemExit(f"{path} is missing: run `.venv/bin/python -m pipeline.index_pdfs --role {role}` first")
    return tuple(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def paragraph_key(paragraph: object) -> str | None:
    """Same normalisation as tools/score_local.py: "Annex 4, Part 1, 1.2." and "annex 4 part 1 1.2" are one key."""
    text = str(paragraph or "").casefold().replace("§", " ")
    text = re.sub(r"[,;:()\[\]]", " ", text)
    text = re.sub(r"(?<![0-9a-z])\.|\.(?![0-9a-z])", " ", text)
    text = " ".join(text.split())
    text = re.sub(r"^(paragraphs?|para|par|section|clause)\s+", "", text)
    return text or None


@cache
def pages_by_paragraph(regulation: str, role: str = "base") -> dict[str, int]:
    """Paragraph key -> the page the paragraph starts on (the first occurrence wins)."""
    pages: dict[str, int] = {}
    for record in paragraphs(regulation, role):
        if key := paragraph_key(record["paragraph"]):
            pages.setdefault(key, record["page"])
    return pages


def overview(regulation: str) -> str:
    """Title, introduction and scope: enough to decide whether the regulation applies to a product."""
    entry = catalogue()[regulation]
    text = []
    for record in paragraphs(regulation):
        label = record["paragraph"]
        if label.startswith("Annex") or re.match(r"^[3-9]|^\d{2}", label):
            break
        text.append(f"{label} {record['text']}")
    body = " ".join(text)[:OVERVIEW_CHARS]
    return f"## {regulation}: {entry['title']}\n{body}"


def render(regulation: str) -> str:
    """The whole regulation, one paragraph per line, tagged with its page so the model can cite it."""
    lines = [f"# {regulation} (version {version_label(regulation)}): {catalogue()[regulation]['title']}"]
    for record in paragraphs(regulation):
        lines.append(f"[p{record['page']}] {record['paragraph']} | {record['text']}")
    return "\n".join(lines)
