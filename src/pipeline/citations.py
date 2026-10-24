"""Step 4, the citation check (no LLM, free): is every requirement's source real, and do its numbers come from it?

    .venv/bin/python -m src.pipeline.citations submissions/dev-rear-lamp.vote.json           # report only
    .venv/bin/python -m src.pipeline.citations submissions/dev-rear-lamp.vote.json --fix     # also fix it in place

For each requirement: the regulation must be in the catalogue, the version must be its base version, the paragraph
must exist in the base version, the page must be the page that paragraph starts on, and every number in the text must
appear in the cited paragraph, its parent headings or its sub-paragraphs. Fixing sets version and page from the
database. Nothing is dropped unless --drop-unresolved, and then only requirements whose regulation or paragraph does
not exist: a number that is missing is reported, since the text may write it another way ("6.0∙10^1" for "60").
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

try:
    from src.pipeline import db, regs
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import db, regs
    else:
        raise

NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
POWER_OF_TEN = re.compile(r"\s*[∙·×x*]\s*10\^?[-−]?\d+")  # "6.0∙10^1": the PDF text loses the superscript
UNRESOLVED = ("regulation not in the catalogue", "paragraph not in the base version")
FOLLOWING_ROWS = 8  # tables often land in the rows after their paragraph
EXAMPLES = 8


def numbers(text: str) -> set[str]:
    """The numbers in a text that a requirement must not invent: "1,500" and "1500" are the same number; paragraph
    references ("3.3.2.1"), powers of ten and single digits (list items, categories) are left out."""
    found = (number.replace(",", "") for number in NUMBER.findall(POWER_OF_TEN.sub("", text)))
    return {number for number in found if number.count(".") < 2 and len(number) > 1}


def check(conn: sqlite3.Connection, item: dict) -> tuple[dict, list[str]]:
    """The requirement with version and page set from the database, and what was wrong with it."""
    source = dict(item["source"])
    regulation = source["regulation"]
    if regulation not in regs.catalogue():
        return item, [UNRESOLVED[0]]
    problems = []
    base = regs.version_label(regulation)
    if source.get("version") != base:
        problems.append(f"version {source.get('version')} -> {base}")
        source["version"] = base
    found = db.get_paragraph(conn, regulation, source.get("paragraph") or "")
    if not found:
        return dict(item, source=source), [*problems, UNRESOLVED[1]]
    if source.get("page") != found["page"]:
        problems.append(f"page {source.get('page')} -> {found['page']}")
        source["page"] = found["page"]
    parents = (db.get_paragraph(conn, regulation, label) for label in db.ancestors(found["paragraph"]))
    following = conn.execute("SELECT text FROM paragraphs WHERE regulation = ? AND role = 'base' AND seq > ?"
                             " ORDER BY seq LIMIT ?", (regulation, found["seq"], FOLLOWING_ROWS)).fetchall()
    context = [found, *(parent for parent in parents if parent), *db.children(conn, regulation, found), *following]
    missing = sorted(numbers(item["text"]) - numbers(" ".join(row["text"] for row in context)))
    if missing:
        problems.append(f"numbers not in the cited paragraph: {', '.join(missing)}")
    return dict(item, source=source), problems


def kind(problem: str) -> str:
    """"page 12 -> 13" -> "page fixed"; "numbers not in the cited paragraph: 60, 185" -> "numbers not in ..."."""
    return f"{problem.split()[0]} fixed" if " -> " in problem else problem.split(":")[0]


def check_all(requirements: list[dict], drop_unresolved: bool = False) -> tuple[list[dict], Counter, list[str]]:
    """Every requirement checked and fixed; the count of each kind of problem; a few examples to show."""
    conn = db.connect()
    kept, counts, examples = [], Counter(), []
    for item in requirements:
        fixed, problems = check(conn, item)
        for problem in problems:
            counts[kind(problem)] += 1
            if len(examples) < EXAMPLES and " -> " not in problem:
                source = fixed["source"]
                examples.append(f"{source['regulation']} {source.get('paragraph')}: {problem} | {fixed['text'][:90]}")
        if not (drop_unresolved and any(problem in UNRESOLVED for problem in problems)):
            kept.append(fixed)
    return kept, counts, examples


def report(requirements: list[dict], counts: Counter, examples: list[str]) -> str:
    clean = len(requirements) - sum(counts[problem] for problem in UNRESOLVED) - counts["numbers not in the cited paragraph"]
    lines = [f"[citations] {len(requirements)} requirements; {clean} without a problem"]
    lines += [f"[citations]   {problem}: {count}" for problem, count in counts.most_common()]
    lines += [f"[citations]   e.g. {example}" for example in examples]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("submission", type=Path)
    parser.add_argument("--fix", action="store_true", help="write the fixed versions and pages back to the file")
    parser.add_argument("--drop-unresolved", action="store_true", help="with --fix: drop requirements whose "
                                                                       "regulation or paragraph does not exist")
    args = parser.parse_args()

    data = json.loads(args.submission.read_text(encoding="utf-8"))
    kept, counts, examples = check_all(data["requirements"], args.drop_unresolved)
    print(report(data["requirements"], counts, examples))
    if args.fix:
        kept = [dict(item, id=f"R-{number:04d}") for number, item in enumerate(kept, 1)]
        args.submission.write_text(json.dumps(dict(data, requirements=kept), indent=2, ensure_ascii=False),
                                   encoding="utf-8")
        print(f"[citations] fixed -> {args.submission} ({len(kept)} requirements)")


if __name__ == "__main__":
    main()
