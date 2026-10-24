"""Review and prune extracted requirements to maximize precision and remove out-of-scope clauses.

Usage:
    .venv/bin/python -m src.pipeline.review submissions/dev-rear-lamp.json --case-dir data/cases/dev-rear-lamp
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from src.pipeline import llm, prompts, regs
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import llm, prompts, regs
    else:
        raise

REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "reviews": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                    "keep": {"type": "boolean"},
                    "reason": {"type": "string"},
                },
                "required": ["index", "keep", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["reviews"],
    "additionalProperties": False,
}

BATCH_SIZE = 50


def review_batch(spec: str, batch: list[dict], offset: int) -> list[dict]:
    """Review a batch of candidate requirements against the product specification."""
    items_text = []
    for i, req in enumerate(batch):
        idx = offset + i
        reg = req["source"]["regulation"]
        para = req["source"].get("paragraph", "")
        text = req["text"]
        items_text.append(f"[{idx}] {reg} §{para}: {text}")

    candidates_block = "\n".join(items_text)
    content = [
        {"type": "text", "text": prompts.render("review.task", spec=spec, candidates=candidates_block)},
    ]

    result = llm.ask_json(prompts.render("review.system"), content, REVIEW_SCHEMA, effort="medium")
    return result.get("reviews", [])


def review_requirements(spec: str, requirements: list[dict], workers: int = 4) -> tuple[list[dict], list[dict]]:
    """Review all requirements in parallel batches. Returns (kept_requirements, discarded_records)."""
    batches = [
        (requirements[i : i + BATCH_SIZE], i)
        for i in range(0, len(requirements), BATCH_SIZE)
    ]

    all_reviews: dict[int, dict] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(review_batch, spec, batch, offset)
            for batch, offset in batches
        ]
        for f in futures:
            for rev in f.result():
                all_reviews[rev["index"]] = rev

    kept = []
    discarded = []
    for idx, req in enumerate(requirements):
        decision = all_reviews.get(idx, {"keep": True, "reason": "default keep"})
        if decision["keep"]:
            kept.append(req)
        else:
            discarded.append({"requirement": req, "reason": decision["reason"]})

    # Renumber IDs cleanly (R-0001, R-0002, ...)
    renumbered = []
    for i, req in enumerate(kept, 1):
        r = dict(req)
        r["id"] = f"R-{i:04d}"
        renumbered.append(r)

    return renumbered, discarded


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path, help="Path to input submission JSON")
    parser.add_argument("--case-dir", type=Path, required=True, help="Directory containing spec.md")
    parser.add_argument("--output", type=Path, default=None, help="Output path (default: overwrite input)")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    llm.load_env()
    sub_data = json.loads(args.submission.read_text(encoding="utf-8"))
    orig_reqs = sub_data.get("requirements", [])
    print(f"Loaded {len(orig_reqs)} requirements from {args.submission}")

    spec_files = [p.read_text(encoding="utf-8") for p in sorted(args.case_dir.glob("*.md"))]
    spec = "\n\n".join(spec_files) if spec_files else "Automotive component specification"

    print("Running Review Agent ...")
    kept, discarded = review_requirements(spec, orig_reqs, workers=args.workers)

    print(f"\n[Review Agent Summary]")
    print(f"Total candidates: {len(orig_reqs)}")
    print(f"Kept:             {len(kept)}")
    print(f"Discarded:        {len(discarded)}")

    if discarded:
        print("\nSample discarded requirements:")
        for d in discarded[:5]:
            req = d["requirement"]
            print(f"  - {req['source']['regulation']} §{req['source'].get('paragraph')}: {d['reason']}")

    out_path = args.output or args.submission
    out_data = dict(sub_data, requirements=kept)
    out_path.write_text(json.dumps(out_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved {len(kept)} requirements to {out_path}")

    # Validate & score locally if expected.json is available
    tools_dir = regs.DATA_DIR / "tools"
    validate_script = tools_dir / "validate.py"
    score_script = tools_dir / "score_local.py"
    expected = args.case_dir / "expected.json"

    if validate_script.exists():
        subprocess.run([sys.executable, str(validate_script), str(out_path)], check=False)
    if expected.exists() and score_script.exists():
        subprocess.run([sys.executable, str(score_script), str(out_path), "--expected", str(expected)], check=False)


if __name__ == "__main__":
    main()
