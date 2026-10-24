"""Vote: keep the candidates that enough independent signals agree on. No LLM, free to rerun.

    .venv/bin/python -m src.pipeline.vote cases/dev-rear-lamp \
        --pool submissions/dev-rear-lamp.obligations-no-review.json \
        --voters submissions/dev-rear-lamp.obligations.json submissions/dev-rear-lamp.obligations-lenient.json \
        --paragraph-voters submissions/dev-rear-lamp.json --min-votes 2

Every file is a submission. A requirement voter votes for each requirement it contains (same regulation, paragraph
and text as in the pool); a paragraph voter votes for every pool requirement on a paragraph it cites (e.g. the
full-read run, whose texts differ from the obligations'). A pool requirement with at least --min-votes votes is
kept. Then table paragraphs are restated (tables.py, --no-tables skips it) and the citations checked.
Writes submissions/<case>.vote.json, then validates and scores it like run.py.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from src.pipeline import citations, db, llm, run, tables
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, run, tables
    else:
        raise


def requirement_key(item: dict) -> tuple[str, str, str]:
    return item["source"]["regulation"], db.lookup_key(item["source"]["paragraph"]), " ".join(item["text"].split())


def paragraph_key(item: dict) -> tuple[str, str]:
    return item["source"]["regulation"], db.lookup_key(item["source"]["paragraph"])


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["requirements"]


def vote(pool: list[dict], voters: list[list[dict]], paragraph_voters: list[list[dict]], min_votes: int) -> list[dict]:
    requirement_sets = [{requirement_key(item) for item in voter} for voter in voters]
    paragraph_sets = [{paragraph_key(item) for item in voter} for voter in paragraph_voters]
    kept = []
    for item in pool:
        votes = sum(requirement_key(item) in s for s in requirement_sets) + sum(paragraph_key(item) in s for s in paragraph_sets)
        if votes >= min_votes:
            kept.append(dict(item, id=f"R-{len(kept) + 1:04d}"))
    return kept


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--pool", type=Path, required=True, help="submission with every candidate")
    parser.add_argument("--voters", type=Path, nargs="*", default=[], help="submissions that vote per requirement")
    parser.add_argument("--paragraph-voters", type=Path, nargs="*", default=[], help="submissions that vote per paragraph")
    parser.add_argument("--min-votes", type=int, default=2)
    parser.add_argument("--no-tables", action="store_true", help="skip restating table paragraphs (tables.py)")
    parser.add_argument("--team-id", default=None, help="default: TEAM_ID from .env")
    args = parser.parse_args()

    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    kept = vote(load(args.pool), [load(p) for p in args.voters], [load(p) for p in args.paragraph_voters], args.min_votes)
    if not args.no_tables:
        kept, change = tables.restate(kept)
        print(f"[tables] restated table paragraphs: {change:+d} requirements")
    kept = [dict(item, id=f"R-{number:04d}") for number, item in enumerate(kept, 1)]
    kept, findings, examples = citations.check_all(kept)
    print(citations.report(kept, findings, examples))
    submission = {"team_id": args.team_id or os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                  "requirements": kept}
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.vote.json"
    path.write_text(json.dumps(submission, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(kept)} of {len(load(args.pool))} candidates have >= {args.min_votes} votes -> "
          f"{path.relative_to(run.REPO_ROOT)}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)
    expected = case_dir / "expected.json"
    if expected.exists():
        subprocess.run([sys.executable, str(run.TOOLS_DIR / "score_local.py"), str(path), "--expected", str(expected)],
                       check=False)


if __name__ == "__main__":
    main()
