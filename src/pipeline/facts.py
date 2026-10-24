"""Product facts: which device categories and classes the product has, to drop requirements for the others.

    .venv/bin/python -m src.pipeline.facts cases/dev-rear-lamp --pool submissions/dev-rear-lamp.pool.json

The regulations set values per category (stop lamp S1, S2, S3; rear position lamp R1, R2; retro-reflector class IA,
IB), and the obligation builder writes one requirement per category. One small Claude call reads the specification
and the drawings and marks each code found in the pool as own, excluded or unclear (prompts/facts.*.md). filter()
then drops a requirement that names an excluded code and none of the product's own codes. Writes
work/runs/<case>/facts.json; pipeline.vote applies it with --facts.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from src.pipeline import llm, prompts, run
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import llm, prompts, run
    else:
        raise

# category and class codes: S1, R2, RM1, F2, MR, MS, AR, IA, IIIB, IVA ...
CODE = re.compile(r"\b(?:[A-Z]{1,2}\d{1,2}[a-z]?|MR|MS|AR|I{1,3}V?[AB]|IV[AB]?)\b")
EXAMPLE_CHARS = 120


def codes(requirements: list[dict]) -> dict[str, str]:
    """Each code in the requirements, with the first requirement text that names it."""
    found: dict[str, str] = {}
    for item in requirements:
        for code in CODE.findall(item["text"]):
            found.setdefault(code, item["text"][:EXAMPLE_CHARS])
    return found


def decide(spec: str, images: list[dict], found: dict[str, str]) -> dict[str, str]:
    schema = {"type": "object", "additionalProperties": False, "required": ["codes"],
              "properties": {"codes": {"type": "array", "items": {
                  "type": "object", "additionalProperties": False, "required": ["code", "status"],
                  "properties": {"code": {"type": "string", "enum": sorted(found)},
                                 "status": {"type": "string", "enum": ["own", "excluded", "unclear"]}}}}}}
    listing = "\n".join(f"{code}: {example}" for code, example in sorted(found.items()))
    task = prompts.render("facts.task", spec=spec, codes=listing)
    answer = llm.ask_json(prompts.render("facts.system"), [*images, {"type": "text", "text": task}], schema)
    return {item["code"]: item["status"] for item in answer["codes"]}


def filter(requirements: list[dict], statuses: dict[str, str]) -> tuple[list[dict], int]:
    """Drop requirements that name an excluded code and none of the product's own codes."""
    kept = []
    for item in requirements:
        named = set(CODE.findall(item["text"]))
        if any(statuses.get(c) == "excluded" for c in named) and not any(statuses.get(c) == "own" for c in named):
            continue
        kept.append(item)
    return kept, len(requirements) - len(kept)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--pool", type=Path, required=True, help="submission with every candidate")
    args = parser.parse_args()

    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    spec, images = run.case_inputs(case_dir)
    found = codes(json.loads(args.pool.read_text(encoding="utf-8"))["requirements"])
    statuses = decide(spec, images, found)
    path = run.RUNS_DIR / case_dir.name / "facts.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(statuses, indent=2, sort_keys=True), encoding="utf-8")
    for status in ("own", "excluded", "unclear"):
        print(f"[facts] {status:8s} {', '.join(sorted(c for c, s in statuses.items() if s == status))}")
    print(f"-> {path.relative_to(run.REPO_ROOT)}  cost: ${llm.cost_dollars():.2f}")


if __name__ == "__main__":
    main()
