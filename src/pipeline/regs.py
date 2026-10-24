"""Read access to the regulations: the catalogue and the paragraphs, all from the SQLite database.

`python -m src.pipeline.db` builds work/regulations.db from the kit's regulations/index.json and the paragraph index
(work/index/*.jsonl, made by pipeline.index_pdfs). Those files are only build inputs: the pipeline reads the database.
"""

from __future__ import annotations

import re
import sqlite3
from contextlib import closing
from functools import cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" if (REPO_ROOT / "data").exists() else REPO_ROOT / "industrial-ai-hackathon"
INDEX_JSON = DATA_DIR / "regulations" / "index.json"
INDEX_DIR = REPO_ROOT / "work" / "index"
DB_PATH = REPO_ROOT / "work" / "regulations.db"
OVERVIEW_CHARS = 3000


def slug(regulation: str) -> str:
    return "_".join(regulation.replace("/", " ").split())


def query(sql: str, params: tuple = ()) -> list[sqlite3.Row]:
    """Rows from the database, over a fresh read-only connection so that worker threads can call it too."""
    if not DB_PATH.exists():
        raise SystemExit(f"{DB_PATH} is missing: run `.venv/bin/python -m src.pipeline.db` first")
    with closing(sqlite3.connect(f"{DB_PATH.as_uri()}?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(sql, params).fetchall()


@cache
def catalogue() -> dict[str, dict]:
    """Regulation -> {"regulation", "title", "source_url", "versions": [{"role", "version_label", "status"}]}."""
    entries = {row["regulation"]: {**dict(row), "versions": []}
               for row in query("SELECT * FROM regulations ORDER BY rowid")}
    for row in query("SELECT * FROM versions ORDER BY rowid"):
        entries[row["regulation"]]["versions"].append(
            {"role": row["role"], "version_label": row["version"], "status": row["status"]})
    return entries


def version_label(regulation: str, role: str = "base") -> str:
    return next(v["version_label"] for v in catalogue()[regulation]["versions"] if v["role"] == role)


@cache
def paragraphs(regulation: str, role: str = "base") -> tuple[dict, ...]:
    rows = query("SELECT regulation, version, role, file, paragraph, page, end_page, annex, text FROM paragraphs"
                 " WHERE regulation = ? AND role = ? ORDER BY seq", (regulation, role))
    if not rows:
        raise SystemExit(f"{regulation} ({role}) has no paragraphs in {DB_PATH.name}: run "
                         f"`.venv/bin/python -m src.pipeline.index_pdfs --role {role}`, then rebuild the database")
    return tuple(dict(row) for row in rows)


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
    for row in query("SELECT key, page FROM paragraphs WHERE regulation = ? AND role = ? AND key IS NOT NULL"
                     " ORDER BY seq", (regulation, role)):
        pages.setdefault(row["key"], row["page"])
    return pages


def overview(regulation: str) -> str:
    """Title, introduction and scope: enough to decide whether the regulation applies to a product."""
    entry = catalogue()[regulation]
    text = []
    for record in paragraphs(regulation):
        label = record["paragraph"]
        if label.startswith("Rationale"):
            continue
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
