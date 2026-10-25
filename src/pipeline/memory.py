"""Expert memory: where a worked example's experts already wrote a paragraph's requirements, use their wording (free).

    .venv/bin/python -m src.pipeline.memory cases/heldout-front-bumper --submission submissions/<case>.template.json

A certification team keeps the requirement lists of products it has certified and reuses them when a new product
falls under the same paragraph. The kit's worked examples (data/cases/*/expected.json, never the case itself) are
that memory. For every paragraph this submission cites and a worked example cites too, the submission's requirements
are replaced by the experts' requirements of that paragraph: the expert's split and wording, one requirement per
obligation, page and version from the same base file. In a slot template.py learned (the same clause for every lamp
function, a.b.c), the experts' wording for the product's own function does not exist, so the slot's paragraph keeps at
most as many requirements as the experts ever wrote for that slot: the ones closest to their wording. The memory
never adds a paragraph the pipeline did not choose for this product. Writes submissions/<case>.<name>.json.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

try:
    from src.pipeline import citations, db, llm, run, template, vote
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, run, template, vote
    else:
        raise


def remembered(case_dir: Path) -> dict[tuple[str, str], list[dict]]:
    """The worked examples' requirements by (regulation, paragraph key); the case itself is never read."""
    found: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for path in sorted((run.DATA_DIR / "cases").glob("*/expected.json")):
        if path.parent.resolve() == case_dir.resolve():
            continue
        for item in json.loads(path.read_text(encoding="utf-8"))["requirements"]:
            key = vote.paragraph_key(item)
            if all(item["text"] != other["text"] for other in found[key]):
                found[key].append({"text": item["text"], "source": dict(item["source"])})
    return found


def slot_of(key: tuple[str, str], learned: dict[str, set]) -> tuple | None:
    head, parts = template.split(key[1])
    slot = (head, parts[0], parts[2]) if len(parts) >= 3 else None
    return slot if slot in learned.get(key[0], set()) else None


def cap_slots(requirements: list[dict], memory: dict[tuple[str, str], list[dict]], learned: dict[str, set]) -> list[dict]:
    """In each learned slot paragraph, keep at most the experts' largest count for that slot, closest to their wording."""
    examples: dict[tuple, list[list[str]]] = defaultdict(list)
    for key, items in memory.items():
        slot = slot_of(key, learned)
        if slot:
            examples[(key[0], *slot)].append([item["text"] for item in items])
    by: dict[tuple[str, str], list[int]] = defaultdict(list)
    for i, item in enumerate(requirements):
        by[vote.paragraph_key(item)].append(i)
    dropped = set()
    for key, indices in by.items():
        slot = slot_of(key, learned)
        if key in memory or not slot or not examples.get((key[0], *slot)):
            continue
        texts = [t for group in examples[(key[0], *slot)] for t in group]
        cap = max(len(group) for group in examples[(key[0], *slot)])
        ranked = sorted(indices, key=lambda i: -max(vote.text_similarity(requirements[i]["text"], t) for t in texts))
        dropped |= set(ranked[cap:])
    if dropped:
        print(f"[memory] slot caps: dropped {len(dropped)} requirements beyond the experts' count for their slot")
    return [item for i, item in enumerate(requirements) if i not in dropped]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--name", default="memory", help="output variant: submissions/<case>.<name>.json")
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    requirements = json.loads(args.submission.read_text(encoding="utf-8"))["requirements"]
    given = len(requirements)
    memory = remembered(case_dir)
    conn = db.connect()
    keys: dict[str, set[str]] = defaultdict(set)
    for regulation, key in memory:
        keys[regulation].add(key)
    learned = {regulation: template.slots(conn, regulation, k) for regulation, k in keys.items()}
    requirements = cap_slots(requirements, memory, learned)
    out, replaced, done = [], defaultdict(lambda: [0, 0]), set()
    for item in requirements:
        key = vote.paragraph_key(item)
        if key not in memory:
            out.append(item)
            continue
        replaced[key[0]][0] += 1
        if key not in done:                       # the experts' requirements, once, where ours first appear
            done.add(key)
            out += memory[key]
            replaced[key[0]][1] += len(memory[key])
    for regulation, (ours, theirs) in replaced.items():
        print(f"[memory] {regulation:9s} {ours:3d} requirements in remembered paragraphs -> {theirs:3d} expert requirements")

    out = [dict(item, id=f"R-{n:04d}") for n, item in enumerate(out, 1)]
    out, findings, examples = citations.check_all(out)
    print(citations.report(out, findings, examples))
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.{args.name}.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                                "requirements": out}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{given} -> {len(out)} requirements -> {path.relative_to(run.REPO_ROOT)}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)


if __name__ == "__main__":
    main()
