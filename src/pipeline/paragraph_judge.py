"""Paragraph judge: per regulation, which paragraphs of the candidate pool would an expert cite? (Claude)

    .venv/bin/python -m src.pipeline.paragraph_judge cases/dev-rear-lamp --pool submissions/dev-rear-lamp.pool.json

A voter for pipeline.vote that judges whole paragraphs instead of single requirements, so its mistakes differ from
the requirement reviewers'. It sees the specification, the drawings, and each paragraph of the pool with its parent
headings and the start of its text. Writes submissions/<case>.paragraphs.json (one entry per cited paragraph, for
--paragraph-voters) and work/runs/<case>/paragraph_judge.json. Prompts: prompts/paragraph_judge.*.md.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from src.pipeline import db, llm, prompts, regs, run
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import db, llm, prompts, regs, run
    else:
        raise

TEXT_CHARS = 400
HEADING_CHARS = 60


def paragraphs(regulation: str, pool: list[dict]) -> list[dict]:
    """The pool's paragraphs of one regulation, in document order, each with its parent headings."""
    conn = db.connect()
    found = {}
    for item in pool:
        if item["source"]["regulation"] == regulation:
            row = db.get_paragraph(conn, regulation, item["source"]["paragraph"])
            if row:
                found[row["id"]] = row
    result = []
    for row in sorted(found.values(), key=lambda r: r["seq"]):
        parents = [db.get_paragraph(conn, regulation, label) for label in db.ancestors(row["paragraph"])[-2:]]
        heading = " > ".join(f"{p['paragraph']} {p['text'][:HEADING_CHARS]}" for p in parents if p)
        result.append(dict(row, heading=heading))
    return result


def judge(regulation: str, rows: list[dict], spec: str, images: list[dict]) -> list[str]:
    listing = "\n".join(f"{row['paragraph']} (p{row['page']})" + (f", under {row['heading']}" if row["heading"] else "")
                        + f": {row['text'][:TEXT_CHARS]}" for row in rows)
    labels = [row["paragraph"] for row in rows]
    schema = {"type": "object", "properties": {"cite": {"type": "array", "items": {"type": "string", "enum": labels}}},
              "required": ["cite"], "additionalProperties": False}
    task = prompts.render("paragraph_judge.task", spec=spec, regulation=regulation, count=str(len(rows)),
                          title=regs.catalogue()[regulation]["title"], paragraphs=listing)
    return llm.ask_json(prompts.render("paragraph_judge.system"),
                        [*images, {"type": "text", "text": task}], schema)["cite"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--pool", type=Path, required=True, help="submission with every candidate")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    spec, images = run.case_inputs(case_dir)
    pool = json.loads(args.pool.read_text(encoding="utf-8"))["requirements"]
    selected = list(dict.fromkeys(item["source"]["regulation"] for item in pool))
    rows = {regulation: paragraphs(regulation, pool) for regulation in selected}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        cited = dict(zip(selected, executor.map(lambda r: judge(r, rows[r], spec, images), selected)))

    entries, report = [], defaultdict(dict)
    for regulation in selected:
        by_label = {row["paragraph"]: row for row in rows[regulation]}
        for label in dict.fromkeys(cited[regulation]):
            row = by_label[label]
            entries.append({"id": f"P-{len(entries) + 1:04d}", "text": row["text"][:run.MAX_TEXT],
                            "source": {"regulation": regulation, "version": regs.version_label(regulation),
                                       "page": row["page"], "paragraph": label}})
        report[regulation] = {"offered": len(rows[regulation]), "cited": cited[regulation]}
        print(f"[paragraphs] {regulation:9s} cites {len(set(cited[regulation])):3d} of {len(rows[regulation]):3d}")
    out_dir = run.RUNS_DIR / case_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "paragraph_judge.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.paragraphs.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                                "requirements": entries}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(entries)} cited paragraphs -> {path.relative_to(run.REPO_ROOT)}")
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}")


if __name__ == "__main__":
    main()
