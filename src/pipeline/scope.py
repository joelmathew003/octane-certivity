"""Scope: drop the requirements of paragraphs an expert would not list for this product (Claude, ~$0.6 per run).

    .venv/bin/python -m src.pipeline.scope cases/dev-rear-lamp --submission submissions/dev-rear-lamp.vote.json

On the dev case 41% of the vote's requirements cite paragraphs the experts never cite, and those paragraphs are of
a few kinds that have nothing to do with the product: pointers ("See Table 4"), what the approval mark consists of, vehicle-level presence and orientation, laboratory procedure, variants the product
does not have, administration. Per regulation, Claude sees the specification, the drawings and each cited paragraph
(headings, text, the requirements written from it) and gives the paragraph one category; the requirements of every
paragraph not in "keep" are dropped. Writes submissions/<case>.<name>.json and work/runs/<case>/<name>.json (the
category of each paragraph). Prompts: prompts/scope.*.md.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from src.pipeline import citations, db, llm, paragraph_judge, prompts, regs, run
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, paragraph_judge, prompts, regs, run
    else:
        raise

TEXT_CHARS = 2500
CATEGORIES = ["keep", "pointer", "approval_mark_composition", "presence_orientation", "test_procedure",
              "not_this_product", "administrative"]


def classify(regulation: str, rows: list[dict], written: dict[int, list[str]], spec: str,
             images: list[dict]) -> dict[str, str]:
    listing = "\n\n".join(f"### {row['paragraph']} (p{row['page']})" + (f", under {row['heading']}" if row["heading"] else "")
                          + f"\nText: {row['text'][:TEXT_CHARS]}\nRequirements written from it:\n"
                          + "\n".join(f"- {text}" for text in written[row["id"]]) for row in rows)
    labels = [row["paragraph"] for row in rows]
    schema = {"type": "object", "properties": {"paragraphs": {"type": "array", "items": {
        "type": "object", "properties": {"paragraph": {"type": "string", "enum": labels},
                                         "category": {"type": "string", "enum": CATEGORIES}},
        "required": ["paragraph", "category"], "additionalProperties": False}}},
        "required": ["paragraphs"], "additionalProperties": False}
    task = prompts.render("scope.task", spec=spec, regulation=regulation, count=str(len(rows)),
                          title=regs.catalogue()[regulation]["title"], paragraphs=listing)
    answer = llm.ask_json(prompts.render("scope.system"), [*images, {"type": "text", "text": task}], schema)
    return {item["paragraph"]: item["category"] for item in answer["paragraphs"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--submission", type=Path, required=True, help="the submission to filter (e.g. the vote)")
    parser.add_argument("--name", default="scope", help="output variant: submissions/<case>.<name>.json")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    spec, images = run.case_inputs(case_dir)
    requirements = json.loads(args.submission.read_text(encoding="utf-8"))["requirements"]
    selected = list(dict.fromkeys(item["source"]["regulation"] for item in requirements))
    conn = db.connect()
    row_of = [db.get_paragraph(conn, item["source"]["regulation"], item["source"]["paragraph"]) for item in requirements]
    written: dict[int, list[str]] = defaultdict(list)
    for item, row in zip(requirements, row_of):
        if row:
            written[row["id"]].append(item["text"])
    rows = {regulation: paragraph_judge.paragraphs(regulation, requirements) for regulation in selected}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        categories = dict(zip(selected, executor.map(
            lambda r: classify(r, rows[r], written, spec, images), selected)))

    # a paragraph Claude left out, or one the database cannot resolve, keeps its requirements
    kept = [item for item, row in zip(requirements, row_of)
            if not row or categories[item["source"]["regulation"]].get(row["paragraph"], "keep") == "keep"]
    for regulation in selected:
        counts = Counter(categories[regulation].get(row["paragraph"], "keep") for row in rows[regulation])
        print(f"[scope] {regulation:9s} {len(rows[regulation]):3d} paragraphs: "
              + ", ".join(f"{name} {counts[name]}" for name in CATEGORIES if counts[name]))
    out_dir = run.RUNS_DIR / case_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{args.name}.json").write_text(json.dumps(categories, indent=2, ensure_ascii=False), encoding="utf-8")

    kept = [dict(item, id=f"R-{number:04d}") for number, item in enumerate(kept, 1)]
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
