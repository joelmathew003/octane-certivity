"""Product specification -> the UN Regulation requirements it must fulfil, as a submission file.

    .venv/bin/python -m pipeline.run cases/dev-rear-lamp --team-id team-07
    .venv/bin/python -m pipeline.run cases/dev-rear-lamp --regulations "UN R48" "UN R148"   # skip selection

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

from pipeline import llm, regs

ROOT = regs.ROOT
RUNS_DIR = ROOT / "work" / "runs"
SUBMISSIONS_DIR = ROOT / "submissions"
MAX_TEXT = 2000
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}

SELECT_SYSTEM = """You are a vehicle type-approval expert. You get the specification of a vehicle component or system \
and a catalogue of UN Regulations (title, introduction and scope of each). Choose the regulations whose requirements \
the product's engineers must fulfil.

Include a regulation when:
- it approves the product itself, or one of its parts, as a device, component or separate technical unit;
- it governs how the product is installed on the vehicle categories in the specification;
- it applies horizontally to the product's technology (for example electromagnetic compatibility for an \
electrical/electronic sub-assembly).

Exclude regulations about other systems, other vehicle categories, or whole-vehicle performance the product does not \
determine. When a consolidated regulation covers the same devices as older individual regulations (its introduction \
says it combines or replaces them), choose the consolidated one only.

Every regulation you add that does not apply costs precision, and every one you miss costs recall, so decide each \
one deliberately."""

EXTRACT_SYSTEM = """You are a vehicle type-approval engineer. You read one UN Regulation and write the engineering \
requirements that one specific product must fulfil under it.

The regulation is given one paragraph per line: `[p<page>] <paragraph> | <text>`.

Include:
- Obligations (shall, shall not, must, may ... only if) that the product's design, construction, materials, \
photometric, electrical or mechanical performance, markings or durability must meet, and, when the regulation \
governs installation on the vehicle, the installation requirements for this product.
- Only obligations that bind this product's own functions and parts. Skip requirements for devices, functions or \
vehicle categories the product does not have.
- Test-procedure paragraphs only where they set a condition or limit the product must meet (a test level, an \
exposure the samples must withstand, a pass criterion).

Skip: definitions, scope, application documents and information folders, duties of approval authorities and \
Technical Services, communication forms, sampling by inspectors, penalties, transitional provisions, and pure \
descriptions of test equipment.

Write each requirement as follows:
- One engineering obligation per requirement: one scope, one condition, one constraint. When a paragraph sets several \
obligations (a list, a table with a value per function, a limit per test pulse), write one requirement for each that \
applies to the product.
- Stay close to the regulation's wording, but make the text self-contained: name the device or function it applies \
to, and keep numbers, units and tolerances exact.
- paragraph: the label exactly as written after the page tag (e.g. `6.10.4.2` or `Annex 6 Part 4 1`). For an \
obligation that comes from a table, append the table name, e.g. `5.1.4.4.1. Table 3`.
- page: the number in the paragraph's [p] tag.
- test_case: one sentence on how to verify the requirement.

Precision matters as much as recall. Experts typically keep well under a third of a regulation's "shall" paragraphs: \
the ones that actually bind this product.

Examples of the expected style:
- "The rear position lamps shall be at a height above the ground of not less than 350 mm nor more than 1,500 mm \
(2,100 mm if the shape of the bodywork makes it impossible to keep within 1,500 mm and if the optional lamps are not \
installed)." (paragraph 6.10.4.2)
- "For pulse 1, the ESA shall meet immunity test level -75 V (12V system) or -450 V (24V system) for 500 pulses with \
FPSC III for functions related to immunity and FPSC III for functions not related to immunity as specified in Table \
3b." (paragraph 6.9.1)
- "The lamps shall be so designed and constructed that in normal conditions of use, and notwithstanding the \
vibrations to which the lamps may be subjected in such use, the satisfactory operation of the lamps remains assured \
and the lamps retain the characteristics prescribed by this Regulation." (paragraph 4.3)"""


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
        {"type": "text", "text": f"<catalogue>\n{catalogue}\n</catalogue>", "cache_control": {"type": "ephemeral"}},
        *images,
        {"type": "text", "text": f"<specification>\n{spec}\n</specification>\n\nWhich of these UN Regulations apply?"},
    ]
    return llm.ask_json(SELECT_SYSTEM, content, select_schema())["regulations"]


def extract(regulation: str, reason: str, spec: str) -> list[dict]:
    content = [
        {"type": "text", "text": f"<regulation>\n{regs.render(regulation)}\n</regulation>",
         "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": f"<specification>\n{spec}\n</specification>\n\n"
                                 f"Why {regulation} applies to this product: {reason}\n\n"
                                 f"Write every requirement this product must fulfil under {regulation}."},
    ]
    return llm.ask_json(EXTRACT_SYSTEM, content, EXTRACT_SCHEMA)["requirements"]


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
    args = parser.parse_args()

    llm.load_env()
    team_id = args.team_id or os.environ.get("TEAM_ID") or "team-00"
    case_dir = args.case_dir.resolve()
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
        items = extract(choice["regulation"], choice["reason"], spec)
        out = run_dir / f"extract_{regs.slug(choice['regulation'])}.json"
        out.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[extract] {choice['regulation']:9s} {len(items):4d} requirements", flush=True)
        return choice["regulation"], items

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        extracted = dict(pool.map(work, selected))

    submission = assemble(team_id, case_id, extracted)
    SUBMISSIONS_DIR.mkdir(exist_ok=True)
    path = SUBMISSIONS_DIR / f"{case_id}.json"
    path.write_text(json.dumps(submission, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(submission['requirements'])} requirements -> {path.relative_to(ROOT)}")
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}\n")

    subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), str(path)], check=False)
    expected = case_dir / "expected.json"
    if expected.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "score_local.py"), str(path), "--expected", str(expected)],
                       check=False)


if __name__ == "__main__":
    main()
