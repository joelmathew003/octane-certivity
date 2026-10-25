"""Relevance judge: per requirement, how likely an expert lists it; cut only the confident tail (Claude, ~$1.50).

    .venv/bin/python -m src.pipeline.relevance cases/heldout-front-bumper --submission submissions/<case>.<file>.json \
        --sources submissions/<case>.vote.json submissions/<case>.fullread-clean.json

F2 = 5·matches / (4·gold + n): a requirement is worth keeping when it has at least about F2/5 (~13%) chance of
matching. The scope filter decides per paragraph; this judge decides per requirement, seeing each paragraph's text and
all of its requirements side by side (so paraphrase duplicates from different sources are visible), plus how many
sources wrote each requirement. It cuts a requirement only when it is a duplicate of a kept one, or below CUT percent;
outside duplicates it never cuts more than half of a paragraph's requirements. Writes submissions/<case>.<name>.json
and work/runs/<case>/<name>.json (every verdict). Prompts: prompts/relevance.*.md.
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
    from src.pipeline import citations, db, llm, paragraph_judge, prompts, regs, run, tables, vote
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, paragraph_judge, prompts, regs, run, tables, vote
    else:
        raise

TEXT_CHARS = 2500
CUT = 10          # percent: below this a requirement is cut (F2/5 is about 13)
SAME = 0.6        # text similarity at which another source counts as having written the same requirement
REASONS = ["binds_product", "duplicate_of", "other_function", "too_generic", "procedure_only"]


def judge(regulation: str, rows: list[dict], members: dict[int, list[int]], requirements: list[dict],
          support: list[int], spec: str, images: list[dict]) -> list[dict]:
    listing = "\n\n".join(
        f"### {row['paragraph']} (p{row['page']})" + (f", under {row['heading']}" if row["heading"] else "")
        + f"\nText: {row['text'][:TEXT_CHARS]}\nRequirements:\n"
        + "\n".join(f"[{i}] ({support[i]} source{'s' if support[i] > 1 else ''}) {requirements[i]['text']}"
                    for i in members[row["id"]]) for row in rows)
    schema = {"type": "object", "properties": {"verdicts": {"type": "array", "items": {"type": "object", "properties": {
        "i": {"type": "integer"}, "probability": {"type": "integer"}, "reason": {"type": "string", "enum": REASONS},
        "keep_instead": {"type": "integer"}},
        "required": ["i", "probability", "reason", "keep_instead"], "additionalProperties": False}}},
        "required": ["verdicts"], "additionalProperties": False}
    task = prompts.render("relevance.task", spec=spec, regulation=regulation, count=str(len(rows)),
                          title=regs.catalogue()[regulation]["title"], paragraphs=listing)
    return llm.ask_json(prompts.render("relevance.system"), [*images, {"type": "text", "text": task}],
                        schema)["verdicts"]


def table_sentences(requirements: list[dict]) -> set[int]:
    """Requirements that restate a paragraph's own sentence before its table: experts list these next to the rows,
    so they are never cut as duplicates of the rows."""
    conn = db.connect()
    found = set()
    for i, item in enumerate(requirements):
        row = db.get_paragraph(conn, item["source"]["regulation"],
                               tables.TABLE_SUFFIX.sub("", item["source"]["paragraph"]))
        own = tables.own_sentences(row["text"]) if row and tables.CAPTION.search(row["text"]) else []
        if any(vote.text_similarity(item["text"], sentence) >= 0.8 for sentence in own):
            found.add(i)
    return found


def cuts(verdicts: dict[int, dict], members: dict[int, list[int]], protected: set[int]) -> set[int]:
    """Duplicates of a kept requirement in the same paragraph, then the confident low tail, at most half a paragraph."""
    dropped: set[int] = set()
    for indices in members.values():
        own = set(indices)
        for i in indices:
            v = verdicts.get(i)
            if v and v["reason"] == "duplicate_of" and i not in protected and v["keep_instead"] in own \
                    and v["keep_instead"] != i and v["keep_instead"] not in dropped:
                dropped.add(i)
        low = sorted((verdicts[i]["probability"], i) for i in indices
                     if i in verdicts and i not in dropped and i not in protected and verdicts[i]["probability"] < CUT)
        budget = len(indices) // 2 if len(indices) > 1 else 1
        dropped |= {i for _, i in low[:budget]}
    return dropped


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--sources", type=Path, nargs="*", default=[], help="files whose agreement is shown as support")
    parser.add_argument("--name", default="relevance", help="output variant: submissions/<case>.<name>.json")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    spec, images = run.case_inputs(case_dir)
    requirements = json.loads(args.submission.read_text(encoding="utf-8"))["requirements"]
    sources = [defaultdict(list) for _ in args.sources]
    for by, path in zip(sources, args.sources):
        for item in json.loads(path.read_text(encoding="utf-8"))["requirements"]:
            by[vote.paragraph_key(item)].append(item["text"])
    support = [max(1, sum(any(vote.text_similarity(item["text"], t) >= SAME for t in by[vote.paragraph_key(item)])
                          for by in sources)) for item in requirements]
    conn = db.connect()
    members: dict[int, list[int]] = defaultdict(list)
    for i, item in enumerate(requirements):
        row = db.get_paragraph(conn, item["source"]["regulation"], item["source"]["paragraph"])
        if row:
            members[row["id"]].append(i)
    selected = list(dict.fromkeys(item["source"]["regulation"] for item in requirements))
    rows = {regulation: paragraph_judge.paragraphs(regulation, requirements) for regulation in selected}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        answers = list(executor.map(lambda r: judge(r, rows[r], members, requirements, support, spec, images), selected))
    verdicts = {v["i"]: v for answer in answers for v in answer if 0 <= v["i"] < len(requirements)}
    dropped = cuts(verdicts, members, table_sentences(requirements))

    for regulation in selected:
        own = [i for i, item in enumerate(requirements) if item["source"]["regulation"] == regulation]
        reasons = defaultdict(int)
        for i in own:
            if i in dropped:
                reasons[verdicts[i]["reason"]] += 1
        print(f"[relevance] {regulation:9s} {len(own):3d} requirements, cut {sum(reasons.values()):3d} "
              + " ".join(f"{k} {v}" for k, v in reasons.items()))
    out_dir = run.RUNS_DIR / case_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{args.name}.json").write_text(json.dumps(
        [dict(requirements[i], verdict=verdicts.get(i), support=support[i], cut=i in dropped)
         for i in range(len(requirements))], indent=1, ensure_ascii=False), encoding="utf-8")

    kept = [dict(item, id=f"R-{n:04d}") for n, item in
            enumerate((item for i, item in enumerate(requirements) if i not in dropped), 1)]
    kept, findings, examples = citations.check_all(kept)
    print(citations.report(kept, findings, examples))
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.{args.name}.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                                "requirements": kept}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"kept {len(kept)} of {len(requirements)} requirements -> {path.relative_to(run.REPO_ROOT)}")
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)


if __name__ == "__main__":
    main()
