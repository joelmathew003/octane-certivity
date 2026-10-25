"""Ensemble of independent runs: keep the obligations that at least MIN_RUNS runs state (free, no model).

    .venv/bin/python -m src.pipeline.ensemble cases/heldout-front-bumper --runs submissions/<case>.<time>.final.json ... \
        --min-runs 2

Each run of make_clean_submission.sh is a panel of five readers (full read, review agent, lenient review, paragraph
judge, product facts) whose model calls differ from run to run, so two runs agree on most requirements and each adds
some the other misses (held-out: two runs scored 74.7 and 74.9 with 310 identical requirements). Requirements of all
runs are grouped per paragraph, one to one: a requirement joins the most similar group (text similarity >= SAME) that
holds no requirement of its own run yet, so distinct obligations of one run are never merged. A group is kept when
requirements from at least --min-runs runs fall in it; its text is the one most runs wrote (the expert memory's
wording is identical across runs). Writes submissions/<case>.<name>.json.
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
    from src.pipeline import citations, llm, run, vote
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, llm, run, vote
    else:
        raise

SAME = 0.5


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--runs", type=Path, nargs="+", required=True, help="final.json of independent runs")
    parser.add_argument("--min-runs", type=int, default=2)
    parser.add_argument("--name", default="ensemble", help="output variant: submissions/<case>.<name>.json")
    args = parser.parse_args()

    llm.load_env()
    case_id = args.case_dir.name
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)   # paragraph -> [{"items": [(run, item)], ...}]
    order: list[tuple[tuple[str, str], int]] = []
    for r, path in enumerate(args.runs):
        for item in vote.load(path):
            key = vote.paragraph_key(item)
            # one to one: join the most similar group that has no requirement of this run yet
            scored = [(max(vote.text_similarity(item["text"], other["text"]) for _, other in group["items"]), g)
                      for g, group in enumerate(groups[key]) if all(rr != r for rr, _ in group["items"])]
            best = max(scored, default=(0.0, -1))
            if best[0] >= SAME:
                groups[key][best[1]]["items"].append((r, item))
            else:
                groups[key].append({"items": [(r, item)]})
                order.append((key, len(groups[key]) - 1))
    kept, support = [], Counter()
    for key, g in order:
        items = groups[key][g]["items"]
        runs = len({r for r, _ in items})
        support[runs] += 1
        if runs >= args.min_runs:
            text = Counter(item["text"] for _, item in items).most_common(1)[0][0]
            kept.append(next(item for _, item in items if item["text"] == text))
    print(f"[ensemble] {len(args.runs)} runs, {sum(support.values())} obligations; by number of runs stating them: "
          f"{dict(sorted(support.items()))}; kept {len(kept)} stated by >= {args.min_runs}")

    kept = [dict(item, id=f"R-{n:04d}") for n, item in enumerate(kept, 1)]
    kept, findings, examples = citations.check_all(kept)
    print(citations.report(kept, findings, examples))
    path = run.SUBMISSIONS_DIR / f"{case_id}.{args.name}.json"
    path.write_text(json.dumps({"team_id": os.environ.get("TEAM_ID") or "team-00", "case_id": case_id,
                                "requirements": kept}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(kept)} requirements -> {path.relative_to(run.REPO_ROOT)}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)


if __name__ == "__main__":
    main()
