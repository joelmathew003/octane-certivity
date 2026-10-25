"""Dedupe: drop requirements that repeat an obligation another requirement of the same paragraph states (Claude).

    .venv/bin/python -m src.pipeline.dedupe cases/dev-rear-lamp --submission submissions/dev-rear-lamp.scope.json

The platform matches requirements one to one, so a second requirement for the same obligation can only be wrong.
Per regulation, Claude sees every paragraph that has two or more requirements (its text and its numbered
requirements) and names the groups that state the same obligation; the most complete one of each group stays.
No specification is needed: the question is only whether two sentences say the same thing. Writes
submissions/<case>.<name>.json and work/runs/<case>/<name>.json (the dropped groups). Prompts: prompts/dedupe.*.md.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from src.pipeline import citations, db, llm, prompts, run
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, prompts, run
    else:
        raise

TEXT_CHARS = 2500


def find_duplicates(regulation: str, groups: list[tuple[dict, list[int]]], requirements: list[dict]) -> list[dict]:
    """groups: (paragraph row, indices into requirements) for one regulation; returns [{"keep": i, "drop": [j, ...]}]."""
    listing = "\n\n".join(f"### {row['paragraph']} (p{row['page']})\nText: {row['text'][:TEXT_CHARS]}\nRequirements:\n"
                          + "\n".join(f"[{i}] {requirements[i]['text']}" for i in indices) for row, indices in groups)
    schema = {"type": "object", "properties": {"duplicates": {"type": "array", "items": {
        "type": "object", "properties": {"keep": {"type": "integer"}, "drop": {"type": "array", "items": {"type": "integer"}}},
        "required": ["keep", "drop"], "additionalProperties": False}}},
        "required": ["duplicates"], "additionalProperties": False}
    task = prompts.render("dedupe.task", regulation=regulation, count=str(len(groups)), paragraphs=listing)
    answer = llm.ask_json(prompts.render("dedupe.system"), [{"type": "text", "text": task}], schema)
    # only drops within one paragraph count, and never the requirement a group keeps
    paragraph_of = {i: row["id"] for row, indices in groups for i in indices}
    return [{"keep": group["keep"], "drop": [j for j in group["drop"]
                                            if j != group["keep"] and paragraph_of.get(j) == paragraph_of.get(group["keep"])]}
            for group in answer["duplicates"] if group["keep"] in paragraph_of]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--submission", type=Path, required=True, help="the submission to dedupe")
    parser.add_argument("--name", default="dedupe", help="output variant: submissions/<case>.<name>.json")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    requirements = json.loads(args.submission.read_text(encoding="utf-8"))["requirements"]
    conn = db.connect()
    by_paragraph: dict[tuple[str, int], list[int]] = defaultdict(list)
    rows = {}
    for i, item in enumerate(requirements):
        row = db.get_paragraph(conn, item["source"]["regulation"], item["source"]["paragraph"])
        if row:
            by_paragraph[(item["source"]["regulation"], row["id"])].append(i)
            rows[row["id"]] = row
    per_regulation: dict[str, list[tuple[dict, list[int]]]] = defaultdict(list)
    for (regulation, row_id), indices in by_paragraph.items():
        if len(indices) > 1:
            per_regulation[regulation].append((rows[row_id], indices))
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        found = dict(zip(per_regulation, executor.map(
            lambda r: find_duplicates(r, per_regulation[r], requirements), per_regulation)))

    dropped = {j for groups in found.values() for group in groups for j in group["drop"]}
    for regulation, groups in found.items():
        print(f"[dedupe] {regulation:9s} {len(per_regulation[regulation]):3d} paragraphs with 2+ requirements: "
              f"{sum(len(g['drop']) for g in groups)} duplicates dropped")
    out_dir = run.RUNS_DIR / case_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{args.name}.json").write_text(json.dumps(
        {r: [{"keep": requirements[g["keep"]]["text"], "drop": [requirements[j]["text"] for j in g["drop"]]}
             for g in groups if g["drop"]] for r, groups in found.items()}, indent=2, ensure_ascii=False), encoding="utf-8")

    kept = [dict(item, id=f"R-{number:04d}") for number, item in
            enumerate((item for i, item in enumerate(requirements) if i not in dropped), 1)]
    kept, findings, examples = citations.check_all(kept)
    print(citations.report(kept, findings, examples))
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.{args.name}.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                                "requirements": kept}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"kept {len(kept)} of {len(requirements)} requirements -> {path.relative_to(run.REPO_ROOT)}")
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)
    expected = case_dir / "expected.json"
    if expected.exists():
        subprocess.run([sys.executable, str(run.TOOLS_DIR / "score_local.py"), str(path), "--expected", str(expected)],
                       check=False)


if __name__ == "__main__":
    main()
