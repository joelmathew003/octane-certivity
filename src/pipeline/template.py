"""Worked-example template: keep only the kinds of paragraph the worked examples' experts cite (free, no model).

    .venv/bin/python -m src.pipeline.template cases/heldout-front-bumper --submission submissions/<case>.<file>.json

The kit's worked examples (data/cases/*/expected.json, never the case itself) show which paragraphs experts cite for a
regulation. For each regulation that also appears in a worked example, a requirement is kept when its paragraph is
- cited by a worked example, or a sub-paragraph of a cited one, or
- in a slot the experts cite for every function: regulations such as R48 and R148 repeat the same clause for each
  lamp function (a.b.c: section a, function b, clause c; "Colour:", "Number"). A slot (a, c) is learned when the
  worked examples cite it under at least SLOT_FUNCTIONS functions and those clauses read alike (their first OPENING
  words have text similarity >= SLOT_SIMILARITY), so the template carries over to the functions this product has.
Every other requirement of such a regulation is dropped; regulations no worked example covers are left as they are.
Writes submissions/<case>.<name>.json.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

try:
    from src.pipeline import citations, db, llm, run, vote
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, run, vote
    else:
        raise

SLOT_FUNCTIONS = 3      # a clause cited under at least this many functions of a section is a slot
SLOT_SIMILARITY = 0.5   # and the cited clauses must open alike (a parallel structure, not a coincidence of numbering)
OPENING = 2             # words compared: the clause title ("Colour: The ...", "Number Two ...")
LABEL = re.compile(r"((?:annex \S+)?(?: ?part \S+)?)\s*([\d.]+)?$")


def split(key: str) -> tuple[str, list[str]]:
    """"annex 3 2.7.1" -> ("annex 3", ["2", "7", "1"])."""
    m = LABEL.match(key)
    return (m.group(1).strip(), [p for p in (m.group(2) or "").split(".") if p]) if m else (key, [])


def cited(case_dir: Path) -> dict[str, set[str]]:
    """Paragraph keys the worked examples' experts cite, per regulation (the case itself is never read)."""
    found: dict[str, set[str]] = defaultdict(set)
    for path in sorted((run.DATA_DIR / "cases").glob("*/expected.json")):
        if path.parent.resolve() == case_dir.resolve():
            continue
        for item in json.loads(path.read_text(encoding="utf-8"))["requirements"]:
            found[item["source"]["regulation"]].add(db.lookup_key(item["source"]["paragraph"]))
    return found


def slots(conn, regulation: str, keys: set[str]) -> set[tuple[str, str, str]]:
    """(head, a, c) clauses cited for at least SLOT_FUNCTIONS functions b whose a.b.c clauses open alike."""
    under: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for key in keys:
        head, parts = split(key)
        if len(parts) >= 3:
            under[(head, parts[0], parts[2])].add(parts[1])
    learned = set()
    for (head, a, c), functions in under.items():
        if len(functions) < SLOT_FUNCTIONS:
            continue
        openings = []
        for b in functions:
            row = db.get_paragraph(conn, regulation, f"{head} {a}.{b}.{c}".strip())
            openings.append(" ".join(row["text"].split()[:OPENING]) if row else "")
        pairs = list(combinations(openings, 2))
        if sum(vote.text_similarity(x, y) for x, y in pairs) / len(pairs) >= SLOT_SIMILARITY:
            learned.add((head, a, c))
    return learned


def keep(key: str, keys: set[str], learned: set[tuple[str, str, str]]) -> bool:
    if any(key == k or key.startswith(k + ".") for k in keys):
        return True
    head, parts = split(key)
    return len(parts) >= 3 and (head, parts[0], parts[2]) in learned


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--name", default="template", help="output variant: submissions/<case>.<name>.json")
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    requirements = json.loads(args.submission.read_text(encoding="utf-8"))["requirements"]
    conn = db.connect()
    examples = cited(case_dir)
    learned = {regulation: slots(conn, regulation, keys) for regulation, keys in examples.items()}
    kept = []
    for regulation in dict.fromkeys(item["source"]["regulation"] for item in requirements):
        own = [item for item in requirements if item["source"]["regulation"] == regulation]
        if regulation not in examples:
            kept += own
            print(f"[template] {regulation:9s} {len(own):3d} requirements, no worked example: kept")
            continue
        mine = [item for item in own if keep(vote.paragraph_key(item)[1], examples[regulation], learned[regulation])]
        kept += mine
        print(f"[template] {regulation:9s} {len(own):3d} requirements, kept {len(mine):3d}  (worked example: "
              f"{len(examples[regulation])} paragraphs, slots {sorted(f'{h} {a}.*.{c}'.strip() for h, a, c in learned[regulation])})")

    kept = [dict(item, id=f"R-{n:04d}") for n, item in enumerate(kept, 1)]
    kept, findings, examples_ = citations.check_all(kept)
    print(citations.report(kept, findings, examples_))
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.{args.name}.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                                "requirements": kept}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"kept {len(kept)} of {len(requirements)} requirements -> {path.relative_to(run.REPO_ROOT)}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)


if __name__ == "__main__":
    main()
