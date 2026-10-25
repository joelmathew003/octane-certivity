"""Complete: for every paragraph a submission cites, add the obligations it states that no requirement states yet (Claude).

    .venv/bin/python -m src.pipeline.complete cases/dev-rear-lamp --submission submissions/dev-rear-lamp.vote-clean.json

The vote keeps the right paragraphs, but its requirements miss some of the obligations in them: a second constraint
merged into one sentence, a list item, a conditional exemption. Experts match one to one, so each of those is lost
recall. Per regulation, Claude sees the specification, the drawings, and each cited paragraph's full text with the
requirements already written for it, and writes only the missing obligations. Writes submissions/<case>.complete.json
(the submission plus the additions) and work/runs/<case>/complete.json. Prompts: prompts/complete.*.md.
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
    from src.pipeline import citations, db, llm, prompts, regs, run
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, prompts, regs, run
    else:
        raise

TEXT_CHARS = 6000  # a paragraph with a table can be long; the rest of the table follows in its text


def paragraphs(regulation: str, requirements: list[dict]) -> list[dict]:
    """The cited paragraphs of one regulation, in document order, each with the requirements that cite it."""
    conn = db.connect()
    found, written = {}, defaultdict(list)
    for item in requirements:
        if item["source"]["regulation"] == regulation:
            row = db.get_paragraph(conn, regulation, item["source"]["paragraph"])
            if row:
                found[row["id"]] = row
                written[row["id"]].append(item["text"])
    return [dict(row, written=written[row["id"]]) for row in sorted(found.values(), key=lambda r: r["seq"])]


def complete(regulation: str, rows: list[dict], spec: str, images: list[dict]) -> list[dict]:
    listing = "\n\n".join(f"### {row['paragraph']} (p{row['page']})\nText: {row['text'][:TEXT_CHARS]}\n"
                          "Requirements already written:\n" + "\n".join(f"- {text}" for text in row["written"])
                          for row in rows)
    labels = [row["paragraph"] for row in rows]
    schema = {"type": "object", "properties": {"additions": {"type": "array", "items": {
        "type": "object", "properties": {"paragraph": {"type": "string", "enum": labels}, "text": {"type": "string"}},
        "required": ["paragraph", "text"], "additionalProperties": False}}},
        "required": ["additions"], "additionalProperties": False}
    task = prompts.render("complete.task", spec=spec, regulation=regulation, count=str(len(rows)),
                          title=regs.catalogue()[regulation]["title"], paragraphs=listing)
    return llm.ask_json(prompts.render("complete.system"), [*images, {"type": "text", "text": task}],
                        schema)["additions"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--submission", type=Path, required=True, help="the submission to complete (e.g. the vote)")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    spec, images = run.case_inputs(case_dir)
    requirements = json.loads(args.submission.read_text(encoding="utf-8"))["requirements"]
    selected = list(dict.fromkeys(item["source"]["regulation"] for item in requirements))
    rows = {regulation: paragraphs(regulation, requirements) for regulation in selected}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        added = dict(zip(selected, executor.map(lambda r: complete(r, rows[r], spec, images), selected)))

    additions = []
    for regulation in selected:
        pages = {row["paragraph"]: row["page"] for row in rows[regulation]}
        for item in added[regulation]:
            additions.append({"text": item["text"][:run.MAX_TEXT], "source": {
                "regulation": regulation, "version": regs.version_label(regulation),
                "page": pages[item["paragraph"]], "paragraph": item["paragraph"]}})
        print(f"[complete] {regulation:9s} +{len(added[regulation]):3d} obligations over {len(rows[regulation]):3d} paragraphs")
    out_dir = run.RUNS_DIR / case_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "complete.json").write_text(json.dumps(additions, indent=2, ensure_ascii=False), encoding="utf-8")

    combined = [dict(item, id=f"R-{number:04d}") for number, item in enumerate(requirements + additions, 1)]
    combined, findings, examples = citations.check_all(combined)
    print(citations.report(combined, findings, examples))
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.complete.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                                "requirements": combined}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(requirements)} + {len(additions)} requirements -> {path.relative_to(run.REPO_ROOT)}")
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)
    expected = case_dir / "expected.json"
    if expected.exists():
        subprocess.run([sys.executable, str(run.TOOLS_DIR / "score_local.py"), str(path), "--expected", str(expected)],
                       check=False)


if __name__ == "__main__":
    main()
