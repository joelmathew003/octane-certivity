"""Editor: rewrite each cited paragraph's requirements from two drafts, split the way experts split (Claude, ~$1).

    .venv/bin/python -m src.pipeline.editor cases/dev-rear-lamp --submission submissions/dev-rear-lamp.final.json \
        --drafts submissions/dev-rear-lamp.fullread-clean.json

On the dev case the obligation builder's texts can match at most ~139 of the 190 expected requirements, whatever
we select: every expected paragraph has obligations, but they are split differently (one per table row where the
expert writes the paragraph's own sentence, two obligations merged into one, an exception without its rule). The
full read covers many of those (obligations + full read: ~153). Per regulation, Claude sees every paragraph the
submission cites, its text, draft A (the submission's requirements) and draft B (the full read's requirements for
that paragraph) and writes the final list. The submission decides which paragraphs are cited; the editor decides
how each is written. Writes submissions/<case>.<name>.json. Prompts: prompts/editor.*.md.
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
    from src.pipeline import citations, db, llm, paragraph_judge, prompts, regs, run
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, paragraph_judge, prompts, regs, run
    else:
        raise

TEXT_CHARS = 4000


def edit(regulation: str, rows: list[dict], drafts: dict[int, tuple[list[str], list[str]]], spec: str,
         images: list[dict]) -> list[dict]:
    def block(row: dict) -> str:
        a, b = drafts[row["id"]]
        return (f"### {row['paragraph']} (p{row['page']})" + (f", under {row['heading']}" if row["heading"] else "")
                + f"\nText: {row['text'][:TEXT_CHARS]}\nDraft A:\n" + ("\n".join(f"- {t}" for t in a) or "(none)")
                + "\nDraft B:\n" + ("\n".join(f"- {t}" for t in b) or "(none)"))
    labels = [row["paragraph"] for row in rows]
    schema = {"type": "object", "properties": {"requirements": {"type": "array", "items": {
        "type": "object", "properties": {"paragraph": {"type": "string", "enum": labels}, "text": {"type": "string"}},
        "required": ["paragraph", "text"], "additionalProperties": False}}},
        "required": ["requirements"], "additionalProperties": False}
    task = prompts.render("editor.task", spec=spec, regulation=regulation, count=str(len(rows)),
                          title=regs.catalogue()[regulation]["title"], paragraphs="\n\n".join(block(r) for r in rows))
    return llm.ask_json(prompts.render("editor.system"), [*images, {"type": "text", "text": task}],
                        schema)["requirements"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--submission", type=Path, required=True, help="draft A; also decides the cited paragraphs")
    parser.add_argument("--drafts", type=Path, required=True, help="draft B, e.g. the full read")
    parser.add_argument("--name", default="edited", help="output variant: submissions/<case>.<name>.json")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    spec, images = run.case_inputs(case_dir)
    requirements = json.loads(args.submission.read_text(encoding="utf-8"))["requirements"]
    others = json.loads(args.drafts.read_text(encoding="utf-8"))["requirements"]
    conn = db.connect()
    drafts: dict[int, tuple[list[str], list[str]]] = defaultdict(lambda: ([], []))
    unresolved = []
    for item in requirements:
        row = db.get_paragraph(conn, item["source"]["regulation"], item["source"]["paragraph"])
        if row:
            drafts[row["id"]][0].append(item["text"])
        else:
            unresolved.append(item)
    for item in others:
        row = db.get_paragraph(conn, item["source"]["regulation"], item["source"]["paragraph"])
        if row and row["id"] in drafts:
            drafts[row["id"]][1].append(item["text"])
    selected = list(dict.fromkeys(item["source"]["regulation"] for item in requirements))
    rows = {regulation: paragraph_judge.paragraphs(regulation, requirements) for regulation in selected}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        written = dict(zip(selected, executor.map(lambda r: edit(r, rows[r], drafts, spec, images), selected)))

    result = []
    for regulation in selected:
        pages = {row["paragraph"]: row["page"] for row in rows[regulation]}
        result += [{"text": item["text"][:run.MAX_TEXT], "source": {
            "regulation": regulation, "version": regs.version_label(regulation),
            "page": pages[item["paragraph"]], "paragraph": item["paragraph"]}} for item in written[regulation]]
        before = sum(len(drafts[row["id"]][0]) for row in rows[regulation])
        print(f"[editor] {regulation:9s} {len(rows[regulation]):3d} paragraphs: {before:3d} requirements -> "
              f"{len(written[regulation]):3d}")
    result = [dict(item, id=f"R-{number:04d}") for number, item in enumerate(result + unresolved, 1)]
    result, findings, examples = citations.check_all(result)
    print(citations.report(result, findings, examples))
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.{args.name}.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                                "requirements": result}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(requirements)} -> {len(result)} requirements -> {path.relative_to(run.REPO_ROOT)}")
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)
    expected = case_dir / "expected.json"
    if expected.exists():
        subprocess.run([sys.executable, str(run.TOOLS_DIR / "score_local.py"), str(path), "--expected", str(expected)],
                       check=False)


if __name__ == "__main__":
    main()
