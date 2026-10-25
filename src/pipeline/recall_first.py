"""Recall-first union: the vote plus the full read's sentences the vote has not covered (free, no model).

    .venv/bin/python -m src.pipeline.recall_first cases/heldout-front-bumper --vote submissions/<case>.vote.json \
        --fullread submissions/<case>.fullread-clean.json

On a new product the vote (run at a low threshold, 0.30) still misses requirements that only the full read writes;
those matched at about 25% on the held-out case, well above the F2/5 (~13%) break-even. A full-read requirement is
added when no vote requirement in its paragraph has text similarity >= SAME with it (additions are not compared
with each other: two full-read sentences of one paragraph are usually two obligations). Requirements of regulations
the vote does not cite are left out, so a regulation dropped by selection never comes back through the full read. Writes submissions/<case>.<name>.json.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    from src.pipeline import citations, run, vote
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, run, vote
    else:
        raise

SAME = 0.5   # text similarity at which a full-read sentence counts as already covered


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--vote", type=Path, required=True, help="vote.py output (threshold 0.30)")
    parser.add_argument("--fullread", type=Path, nargs="+", required=True, help="run.py --no-review output(s)")
    parser.add_argument("--regulations", nargs="*", default=None, help="keep only these (default: those the vote cites)")
    parser.add_argument("--name", default="recallfirst", help="output variant: submissions/<case>.<name>.json")
    args = parser.parse_args()

    case_id = args.case_dir.name
    base = [item for item in vote.load(args.vote)
            if args.regulations is None or item["source"]["regulation"] in args.regulations]
    regulations = set(args.regulations or (item["source"]["regulation"] for item in base))
    by = defaultdict(list)
    for item in base:
        by[vote.paragraph_key(item)].append(item["text"])
    added = []
    for path in args.fullread:
        for item in vote.load(path):
            key = vote.paragraph_key(item)
            if item["source"]["regulation"] in regulations and \
                    max((vote.text_similarity(item["text"], t) for t in by[key]), default=0) < SAME:
                added.append(item)
    print(f"[recall_first] vote {len(base)} + full read {len(added)} "
          f"{dict(Counter(a['source']['regulation'] for a in added))}")

    kept = [dict(item, id=f"R-{n:04d}") for n, item in enumerate(base + added, 1)]
    kept, findings, examples = citations.check_all(kept)
    print(citations.report(kept, findings, examples))
    path = run.SUBMISSIONS_DIR / f"{case_id}.{args.name}.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_id,
                                "requirements": kept}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(kept)} requirements -> {path.relative_to(run.REPO_ROOT)}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)


if __name__ == "__main__":
    main()
