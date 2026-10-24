"""Product specification -> the UN Regulation requirements it must fulfil, as a submission file.

    .venv/bin/python -m src.pipeline.run cases/dev-rear-lamp --team-id team-07
    .venv/bin/python -m src.pipeline.run cases/dev-rear-lamp --regulations "UN R48" "UN R148"   # skip selection

Steps: pick the applicable regulations from the catalogue, then for each one read the whole base version and
write one requirement per engineering obligation, citing paragraph and page. Every LLM answer is saved under
work/runs/<case>/ and the submission goes to submissions/<case>.json, then is validated (and scored offline when
the case has an expected.json).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from src.pipeline import citations, db, llm, prompts, regs, review
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, llm, prompts, regs, review
    else:
        raise

REPO_ROOT = regs.REPO_ROOT
DATA_DIR = regs.DATA_DIR
RUNS_DIR = REPO_ROOT / "work" / "runs"
SUBMISSIONS_DIR = REPO_ROOT / "submissions"
TOOLS_DIR = DATA_DIR / "tools"
MAX_TEXT = 2000
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def select_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "regulations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "regulation": {"type": "string", "enum": sorted(regs.catalogue())},
                        "role": {"type": "string", "enum": ["component", "installation", "horizontal"]},
                        "reason": {"type": "string"},
                    },
                    "required": ["regulation", "role", "reason"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["regulations"],
        "additionalProperties": False,
    }


EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "requirements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "paragraph": {"type": "string"},
                    "page": {"type": "integer"},
                    "text": {"type": "string"},
                    "test_case": {"type": "string"},
                },
                "required": ["paragraph", "page", "text", "test_case"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["requirements"],
    "additionalProperties": False,
}


def case_inputs(case_dir: Path) -> tuple[str, list[dict]]:
    """The specification text and any drawings, as content blocks."""
    texts = [p.read_text(encoding="utf-8") for p in sorted(case_dir.glob("*")) if p.suffix in (".md", ".txt")]
    images = [
        {"type": "image", "source": {"type": "base64", "media_type": IMAGE_TYPES[p.suffix.lower()],
                                     "data": base64.b64encode(p.read_bytes()).decode()}}
        for p in sorted(case_dir.glob("*")) if p.suffix.lower() in IMAGE_TYPES
    ]
    if not texts and not images:
        raise SystemExit(f"{case_dir} has no specification (.md/.txt) or drawing")
    return "\n\n".join(texts), images


def select_regulations(spec: str, images: list[dict]) -> list[dict]:
    catalogue = "\n\n".join(regs.overview(name) for name in regs.catalogue())
    content = [
        {"type": "text", "text": prompts.render("select.catalogue", catalogue=catalogue),
         "cache_control": {"type": "ephemeral"}},
        *images,
        {"type": "text", "text": prompts.render("select.task", spec=spec)},
    ]
    return llm.ask_json(prompts.render("select.system"), content, select_schema())["regulations"]


def extract(regulation: str, reason: str, spec: str, images: list[dict] | None = None) -> list[dict]:
    content = [
        {"type": "text", "text": prompts.render("regulation", regulation_text=regs.render(regulation)),
         "cache_control": {"type": "ephemeral"}},
        *(images or []),
        {"type": "text", "text": prompts.render("extract.task", spec=spec, regulation=regulation, reason=reason)},
    ]
    return llm.ask_json(prompts.render("extract.system"), content, EXTRACT_SCHEMA)["requirements"]


def cited_page(regulation: str, paragraph: str, model_page: int) -> int:
    """The page the paragraph starts on in the index; the model's page only when the label is unknown."""
    pages = regs.pages_by_paragraph(regulation)
    key = regs.paragraph_key(re.sub(r"\.?\s*Table\s+\S+$", "", paragraph, flags=re.IGNORECASE))
    return pages.get(key or "", max(1, model_page))


def assemble(team_id: str, case_id: str, extracted: dict[str, list[dict]]) -> dict:
    requirements, seen = [], set()
    for regulation, items in extracted.items():
        for item in items:
            text = " ".join(item["text"].split())[:MAX_TEXT]
            if not text or (regulation, text) in seen:
                continue
            seen.add((regulation, text))
            requirements.append({
                "id": f"R-{len(requirements) + 1:04d}",
                "text": text,
                "source": {
                    "regulation": regulation,
                    "version": regs.version_label(regulation),
                    "page": cited_page(regulation, item["paragraph"], item["page"]),
                    "paragraph": item["paragraph"],
                },
                "test_case": item["test_case"],
            })
    return {"team_id": team_id, "case_id": case_id, "requirements": requirements}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--team-id", default=None, help="default: TEAM_ID from .env")
    parser.add_argument("--regulations", nargs="+", default=None, help="skip selection and use these")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--no-review", action="store_true", help="skip the review agent step")
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    team_id = args.team_id or os.environ.get("TEAM_ID") or "team-00"
    raw_case_dir = args.case_dir
    if not raw_case_dir.is_absolute():
        if (DATA_DIR / raw_case_dir).exists():
            case_dir = (DATA_DIR / raw_case_dir).resolve()
        elif (REPO_ROOT / raw_case_dir).exists():
            case_dir = (REPO_ROOT / raw_case_dir).resolve()
        else:
            case_dir = raw_case_dir.resolve()
    else:
        case_dir = raw_case_dir.resolve()
    case_id = case_dir.name
    run_dir = RUNS_DIR / case_id
    run_dir.mkdir(parents=True, exist_ok=True)
    spec, images = case_inputs(case_dir)

    if args.regulations:
        unknown = set(args.regulations) - set(regs.catalogue())
        if unknown:
            raise SystemExit(f"not in regulations/index.json: {', '.join(sorted(unknown))}")
        selected = [{"regulation": r, "role": "given", "reason": "chosen on the command line"} for r in args.regulations]
    else:
        print("[select] reading the catalogue ...", flush=True)
        selected = select_regulations(spec, images)
        (run_dir / "selected.json").write_text(json.dumps(selected, indent=2, ensure_ascii=False), encoding="utf-8")
    for choice in selected:
        print(f"[select] {choice['regulation']:9s} {choice['role']:12s} {choice['reason'][:110]}")

    def work(choice: dict) -> tuple[str, list[dict]]:
        items = extract(choice["regulation"], choice["reason"], spec, images)
        out = run_dir / f"extract_{regs.slug(choice['regulation'])}.json"
        out.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[extract] {choice['regulation']:9s} {len(items):4d} requirements", flush=True)
        return choice["regulation"], items

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        extracted = dict(pool.map(work, selected))

    submission = assemble(team_id, case_id, extracted)
    if not args.no_review:
        print("[review] running review agent to prune non-binding clauses ...", flush=True)
        reviewed_reqs, discarded = review.review_requirements(spec, submission["requirements"], workers=args.workers, images=images)
        print(f"[review] kept {len(reviewed_reqs)} requirements, pruned {len(discarded)} non-binding clauses")
        submission["requirements"] = reviewed_reqs

    submission["requirements"], findings, examples = citations.check_all(submission["requirements"])
    print(citations.report(submission["requirements"], findings, examples))
    SUBMISSIONS_DIR.mkdir(exist_ok=True)
    path = SUBMISSIONS_DIR / f"{case_id}.json"
    path.write_text(json.dumps(submission, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(submission['requirements'])} requirements -> {path.relative_to(REPO_ROOT)}")
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}\n")

    subprocess.run([sys.executable, str(TOOLS_DIR / "validate.py"), str(path)], check=False)
    expected = case_dir / "expected.json"
    if expected.exists():
        subprocess.run([sys.executable, str(TOOLS_DIR / "score_local.py"), str(path), "--expected", str(expected)],
                       check=False)


if __name__ == "__main__":
    main()
