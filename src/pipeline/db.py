"""SQLite database over the regulations: catalogue, paragraphs (+ FTS5), obligations and the cases' expected answers.
The pipeline reads everything through it (pipeline.regs); pipeline.run calls ensure_fresh() first, which rebuilds
the database when one of its inputs is newer.

    .venv/bin/python -m src.pipeline.db                    # (re)build work/regulations.db
    .venv/bin/python -m src.pipeline.db search "rear position lamp height" --regulation "UN R48"

The database is derived, never edited: every build starts from scratch and loads
- the catalogue (data/regulations/index.json) and the paragraph index (work/index/*.jsonl);
- each case's expected.json, resolved to paragraphs, as gold labels for measuring filters;
- the obligation builder's output (work/obligations/*.jsonl), so paid LLM work survives a rebuild.

One obligation per line in work/obligations/*.jsonl:
    {"regulation": "UN R48", "role": "base", "paragraph": "6.10.4.2", "text": "...", "kind": "installation",
     "condition": "...", "applies_to": ["rear position lamp"], "vehicle_categories": ["M", "N", "O"], "model": "..."}
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

try:
    from src.pipeline import regs
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import regs
    else:
        raise

DB_PATH = regs.DB_PATH
OBLIGATIONS_DIR = regs.REPO_ROOT / "work" / "obligations"
CASES_DIR = regs.DATA_DIR / "cases"
SECTION_TITLE_CHARS = 80
OBLIGATION = re.compile(r"\b(shall|must)\b", re.IGNORECASE)
TABLE_SUFFIX = re.compile(r"\.?\s*Table\s+\S+$", re.IGNORECASE)

SCHEMA = """
CREATE TABLE regulations (
    regulation TEXT PRIMARY KEY,            -- "UN R148"
    title TEXT NOT NULL,
    source_url TEXT
);
CREATE TABLE versions (
    regulation TEXT NOT NULL REFERENCES regulations,
    role TEXT NOT NULL,                     -- base | latest
    version TEXT NOT NULL,
    status TEXT,
    PRIMARY KEY (regulation, role)
);
CREATE TABLE paragraphs (
    id INTEGER PRIMARY KEY,
    regulation TEXT NOT NULL,
    role TEXT NOT NULL,
    version TEXT NOT NULL,
    file TEXT NOT NULL,                     -- the PDF the paragraph comes from
    seq INTEGER NOT NULL,                   -- order within the document
    paragraph TEXT NOT NULL,                -- label as indexed: "5.1.4.3", "Annex 6 Part 4 1"
    key TEXT,                               -- regs.paragraph_key(paragraph), what the scorer compares
    section TEXT NOT NULL,                  -- "5", "Annex 6", "Preamble"
    section_title TEXT,
    page INTEGER NOT NULL,
    end_page INTEGER NOT NULL,
    annex TEXT,                             -- "6" in Annex 6, NULL in the main body
    text TEXT NOT NULL,
    obligation INTEGER NOT NULL             -- 1 when the text says shall or must
);
CREATE INDEX paragraphs_key ON paragraphs (regulation, role, key);
CREATE INDEX paragraphs_section ON paragraphs (regulation, role, section);
CREATE VIRTUAL TABLE paragraphs_fts USING fts5 (
    paragraph, text, content = 'paragraphs', content_rowid = 'id', tokenize = 'porter unicode61'
);
CREATE TABLE obligations (
    id INTEGER PRIMARY KEY,
    regulation TEXT NOT NULL,
    role TEXT NOT NULL,
    paragraph TEXT NOT NULL,                -- label as the builder wrote it
    paragraph_id INTEGER REFERENCES paragraphs,  -- NULL when the label does not resolve
    ordinal INTEGER NOT NULL,               -- position among the paragraph's obligations
    text TEXT NOT NULL,
    kind TEXT,
    condition TEXT,
    model TEXT
);
CREATE INDEX obligations_paragraph ON obligations (paragraph_id);
CREATE TABLE obligation_tags (
    obligation_id INTEGER NOT NULL REFERENCES obligations,
    facet TEXT NOT NULL,                    -- applies_to | vehicle_category
    value TEXT NOT NULL,
    PRIMARY KEY (obligation_id, facet, value)
);
CREATE INDEX obligation_tags_value ON obligation_tags (facet, value);
CREATE TABLE expected (
    case_id TEXT NOT NULL,
    requirement_id TEXT NOT NULL,
    regulation TEXT NOT NULL,
    version TEXT,
    paragraph TEXT,
    page INTEGER,
    paragraph_id INTEGER REFERENCES paragraphs,  -- NULL when the citation does not resolve
    text TEXT NOT NULL,
    PRIMARY KEY (case_id, requirement_id)
);
"""


def section_of(label: str) -> str:
    """"5.1.4.3" -> "5", "Annex 6 Part 4 1" -> "Annex 6", "Preamble" -> "Preamble"."""
    match = re.match(r"Annex \S+|\d+", label)
    return match.group() if match else label


def lookup_key(paragraph: str) -> str:
    """The scorer's key for a cited label, without a table suffix ("5.1.4.4.1. Table 3")."""
    return regs.paragraph_key(TABLE_SUFFIX.sub("", paragraph)) or ""


def build(path: Path = DB_PATH) -> Counter[str]:
    stats: Counter[str] = Counter()
    tmp = path.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(tmp)
    conn.executescript(SCHEMA)

    first_id: dict[tuple[str, str, str], int] = {}  # (regulation, role, key) -> first paragraph with that key
    for entry in json.loads(regs.INDEX_JSON.read_text(encoding="utf-8")):
        regulation = entry["regulation"]
        conn.execute("INSERT INTO regulations VALUES (?, ?, ?)", (regulation, entry["title"], entry.get("source_url")))
        for version in entry["versions"]:
            role = version["role"]
            conn.execute("INSERT INTO versions VALUES (?, ?, ?, ?)",
                         (regulation, role, version["version_label"], version.get("status")))
            index = regs.INDEX_DIR / f"{regs.slug(regulation)}_{role}.jsonl"
            if not index.exists():
                stats["versions not indexed"] += 1
                continue
            records = [json.loads(line) for line in index.read_text(encoding="utf-8").splitlines() if line.strip()]
            titles: dict[str, str] = {}
            for record in records:
                if record["paragraph"] == section_of(record["paragraph"]):
                    titles.setdefault(record["paragraph"], record["text"][:SECTION_TITLE_CHARS])
            for seq, record in enumerate(records):
                label, key = record["paragraph"], regs.paragraph_key(record["paragraph"])
                section = section_of(label)
                cursor = conn.execute(
                    "INSERT INTO paragraphs (regulation, role, version, file, seq, paragraph, key, section,"
                    " section_title, page, end_page, annex, text, obligation)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (regulation, role, record["version"], record["file"], seq, label, key, section,
                     titles.get(section), record["page"], record["end_page"], record["annex"], record["text"],
                     int(bool(OBLIGATION.search(record["text"])))),
                )
                if key:
                    first_id.setdefault((regulation, role, key), cursor.lastrowid)
                stats["paragraphs"] += 1
    conn.execute("INSERT INTO paragraphs_fts (paragraphs_fts) VALUES ('rebuild')")

    for expected in sorted(CASES_DIR.glob("*/expected.json")):
        case_id = expected.parent.name
        for item in json.loads(expected.read_text(encoding="utf-8"))["requirements"]:
            source = item["source"]
            paragraph_id = first_id.get((source["regulation"], "base", lookup_key(source.get("paragraph") or "")))
            conn.execute("INSERT INTO expected VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (case_id, item["id"], source["regulation"], source.get("version"), source.get("paragraph"),
                          source.get("page"), paragraph_id, item["text"]))
            stats["expected"] += 1
            stats["expected unresolved"] += paragraph_id is None

    ordinals: Counter[tuple[str, str, str]] = Counter()
    for file in sorted(OBLIGATIONS_DIR.glob("*.jsonl")):
        for line in file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            role = item.get("role", "base")
            where = (item["regulation"], role, item["paragraph"])
            paragraph_id = first_id.get((item["regulation"], role, lookup_key(item["paragraph"])))
            cursor = conn.execute(
                "INSERT INTO obligations (regulation, role, paragraph, paragraph_id, ordinal, text, kind, condition,"
                " model) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (*where, paragraph_id, ordinals[where], item["text"], item.get("kind"), item.get("condition"),
                 item.get("model")),
            )
            ordinals[where] += 1
            tags = {("applies_to", v) for v in item.get("applies_to", [])}
            tags |= {("vehicle_category", v) for v in item.get("vehicle_categories", [])}
            conn.executemany("INSERT INTO obligation_tags VALUES (?, ?, ?)",
                             [(cursor.lastrowid, facet, value) for facet, value in sorted(tags)])
            stats["obligations"] += 1
            stats["obligations unresolved"] += paragraph_id is None

    conn.commit()
    conn.close()
    tmp.replace(path)
    return stats


def inputs() -> list[Path]:
    """Every file the build reads, and this module (a schema change needs a rebuild too)."""
    return [Path(__file__), regs.INDEX_JSON, *regs.INDEX_DIR.glob("*.jsonl"), *CASES_DIR.glob("*/expected.json"),
            *OBLIGATIONS_DIR.glob("*.jsonl")]


def ensure_fresh(path: Path = DB_PATH) -> None:
    """Rebuild when the database is missing or older than one of its inputs, e.g. after `git pull` + index_pdfs."""
    if path.exists() and path.stat().st_mtime >= max(p.stat().st_mtime for p in inputs()):
        return
    stats = build(path)
    print(f"[db] rebuilt {path.relative_to(regs.REPO_ROOT)}: " + ", ".join(f"{k} {v}" for k, v in stats.items()))


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    if not path.exists():
        raise SystemExit(f"{path} is missing: run `.venv/bin/python -m src.pipeline.db` first")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def get_paragraph(conn: sqlite3.Connection, regulation: str, paragraph: str, role: str = "base") -> dict | None:
    """The paragraph a citation points to, matched the way the scorer matches labels."""
    row = conn.execute(
        "SELECT * FROM paragraphs WHERE regulation = ? AND role = ? AND key = ? ORDER BY seq LIMIT 1",
        (regulation, role, lookup_key(paragraph)),
    ).fetchone()
    return dict(row) if row else None


def fts_query(text: str) -> str:
    """Any word may match and bm25 ranks paragraphs with more of them first; quoting keeps "6.10.4.2" or "-75 V"
    from being read as FTS5 syntax."""
    return " OR ".join('"' + word.replace('"', '""') + '"' for word in text.split())


def search(conn: sqlite3.Connection, query: str, regulation: str | None = None, role: str = "base",
           limit: int = 20) -> list[dict]:
    rows = conn.execute(
        "SELECT p.* FROM paragraphs_fts JOIN paragraphs p ON p.id = paragraphs_fts.rowid"
        " WHERE paragraphs_fts MATCH ? AND p.role = ? AND (? IS NULL OR p.regulation = ?)"
        " ORDER BY bm25(paragraphs_fts) LIMIT ?",
        (fts_query(query), role, regulation, regulation, limit),
    ).fetchall()
    return [dict(row) for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("build", help="(re)build the database (the default)")
    find = commands.add_parser("search", help="full-text search over paragraphs")
    find.add_argument("query")
    find.add_argument("--regulation", default=None)
    find.add_argument("--role", default="base")
    find.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if args.command == "search":
        for row in search(connect(), args.query, args.regulation, args.role, args.limit):
            print(f"{row['regulation']:9s} p{row['page']:<4d} {row['paragraph']:22s} {row['text'][:110]}")
        return
    stats = build()
    print(f"{DB_PATH.relative_to(regs.REPO_ROOT)}: " + ", ".join(f"{k} {v}" for k, v in stats.items()))


if __name__ == "__main__":
    main()
