"""Sub-Goal pipeline: Version Change Detection between UN Regulation versions.

    .venv/bin/python -m src.pipeline.subgoal data/subgoal/dev --team-id team-16
    .venv/bin/python -m src.pipeline.subgoal data/subgoal/dev --compare

Steps:
1. Index and align paragraphs between old.pdf and new.pdf.
2. Compute text diffs to identify which paragraphs were modified, added, or removed.
3. Map diffs against requirements_old.json to find affected requirements.
4. Use Claude to write new_text and concise reason only for changed paragraphs.
5. Generate a strictly validated submissions/subgoal-<case>.json and compare against expected.json if available.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import fitz

try:
    from src.pipeline import llm, prompts, regs
    from src.pipeline.index_pdfs import split_pdf
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import llm, prompts, regs
        from pipeline.index_pdfs import split_pdf
    else:
        raise

REPO_ROOT = regs.REPO_ROOT
DATA_DIR = regs.DATA_DIR
SUBMISSIONS_DIR = REPO_ROOT / "submissions"
TOOLS_DIR = DATA_DIR / "tools"
PAGE_HEADER = re.compile(r"^(.+),\s*version\s+(\S+)\s*\|\s*page\s+\d+\s+of\s+\d+", re.IGNORECASE)

EXISTING_SCHEMA = {
    "type": "object",
    "properties": {
        "evaluations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "requirement_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["unchanged", "modified", "removed"]},
                    "new_text": {"type": ["string", "null"]},
                    "new_paragraph": {"type": ["string", "null"]},
                    "new_page": {"type": ["integer", "null"]},
                    "reason": {"type": ["string", "null"]},
                },
                "required": ["requirement_id", "status"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["evaluations"],
    "additionalProperties": False,
}

ADDED_SCHEMA = {
    "type": "object",
    "properties": {
        "added_requirements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "new_text": {"type": "string"},
                    "paragraph": {"type": "string"},
                    "page": {"type": "integer"},
                    "reason": {"type": "string"},
                },
                "required": ["new_text", "paragraph", "page", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["added_requirements"],
    "additionalProperties": False,
}


def extract_header_metadata(pdf_path: Path) -> tuple[str, str]:
    """Extract regulation name and version string from page headers."""
    doc = fitz.open(pdf_path)
    for page in doc:
        for line in page.get_text().splitlines():
            m = PAGE_HEADER.match(line.strip())
            if m:
                return m.group(1).strip(), m.group(2).strip()
    return "UN Regulation", "1.0.0"


def norm(text: str) -> str:
    """Normalize whitespace for text comparisons."""
    return " ".join(text.split())


def index_and_align(old_pdf: Path, new_pdf: Path) -> dict[str, Any]:
    """Parse both PDFs and categorize paragraphs into identical, modified, and added."""
    old_reg, old_ver = extract_header_metadata(old_pdf)
    new_reg, new_ver = extract_header_metadata(new_pdf)
    regulation = new_reg or old_reg

    old_pars = split_pdf(old_pdf, regulation, old_ver, "old")
    new_pars = split_pdf(new_pdf, regulation, new_ver, "new")

    old_map = {p["paragraph"]: p for p in old_pars}
    new_map = {p["paragraph"]: p for p in new_pars}

    identical_labels = set()
    modified_labels = set()

    for lbl, old_p in old_map.items():
        if lbl in new_map:
            if norm(old_p["text"]) == norm(new_map[lbl]["text"]):
                identical_labels.add(lbl)
            else:
                modified_labels.add(lbl)
        else:
            modified_labels.add(lbl)

    added_labels = set(new_map.keys()) - set(old_map.keys())

    return {
        "regulation": regulation,
        "old_ver": old_ver,
        "new_ver": new_ver,
        "old_pars": old_pars,
        "new_pars": new_pars,
        "old_map": old_map,
        "new_map": new_map,
        "identical_labels": identical_labels,
        "modified_labels": modified_labels,
        "added_labels": added_labels,
    }


ADMIN_SECTIONS = {"Preamble", "1", "2", "3"}
ADMIN_HEADINGS = re.compile(
    r"\b(?:application for approval|penalt|production definitively discontinued|names and addresses|"
    r"transitional provisions|communication form|arrangements? of approval marks?)\b",
    re.IGNORECASE,
)


def text_similarity(s1: str, s2: str) -> float:
    """Jaccard word similarity between two texts."""
    w1 = set(s1.lower().split())
    w2 = set(s2.lower().split())
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / len(w1 | w2)


def is_technical_section(label: str, text: str = "") -> bool:
    """True if paragraph is outside purely administrative sections."""
    if label == "Preamble":
        return False
    if label.startswith("Annex 1 ") or label == "Annex 1" or label.startswith("Annex 2 ") or label == "Annex 2":
        return False
    match = re.match(r"^(\d+)", label)
    if match and match.group(1) in ADMIN_SECTIONS:
        return False
    if text and len(text) < 150 and ADMIN_HEADINGS.search(text):
        return False
    return True


def safe_text(text: str, max_chars: int = 1950) -> str:
    """Normalize text and ensure it stays cleanly within max_chars without mid-sentence truncation."""
    cleaned = norm(text)
    if len(cleaned) <= max_chars:
        return cleaned
    truncated = cleaned[:max_chars]
    last_stop = max(truncated.rfind("."), truncated.rfind(";"))
    if last_stop > max_chars - 300:
        return truncated[:last_stop + 1].strip()
    return truncated


def is_heading_only(text: str) -> bool:
    """Heuristic to detect pure headings without obligations."""
    cleaned = norm(text)
    if len(cleaned) < 50 and not any(w in cleaned.lower() for w in ["shall", "must", "may", "test", "procedure"]):
        return True
    return False


def evaluate_existing_requirements(
    candidate_reqs: list[dict],
    alignment: dict[str, Any],
) -> list[dict]:
    """Evaluate candidate existing requirements using Claude Opus."""
    if not candidate_reqs:
        return []

    regulation = alignment["regulation"]
    old_ver = alignment["old_ver"]
    new_ver = alignment["new_ver"]
    old_map = alignment["old_map"]
    new_pars = alignment["new_pars"]

    req_lines = []
    relevant_old_paras = set()
    for r in candidate_reqs:
        p = r["source"]["paragraph"]
        pg = r["source"]["page"]
        relevant_old_paras.add(p)
        req_lines.append(f"- ID: {r['id']} | Old Para: {p} (p.{pg}) | Text: {r['text']}")

    # Collect relevant new paragraphs that might contain the new version of these requirements
    para_lines = []
    for p in new_pars:
        lbl = p["paragraph"]
        # Include technical paragraphs or ones matching relevant old sections
        if is_technical_section(lbl, p["text"]):
            para_lines.append(f"[p{p['page']}] {lbl} | {p['text']}")

    req_context = "\n".join(req_lines)
    para_context = "\n\n".join(para_lines)

    system_prompt = prompts.render(
        "subgoal_existing.system",
        regulation=regulation,
        old_version=old_ver,
        new_version=new_ver,
    )
    task_prompt = prompts.render(
        "subgoal_existing.task",
        regulation=regulation,
        old_version=old_ver,
        new_version=new_ver,
        requirements_context=req_context,
        paragraphs_context=para_context,
    )

    content = [{"type": "text", "text": task_prompt}]
    result = llm.ask_json(system_prompt, content, EXISTING_SCHEMA)
    evaluations = result.get("evaluations", [])

    changes = []
    for ev in evaluations:
        status = ev.get("status")
        rid = ev.get("requirement_id")
        if status == "modified":
            changes.append({
                "requirement_id": rid,
                "change": "modified",
                "new_text": safe_text(ev.get("new_text") or ""),
                "reason": ev.get("reason") or f"Paragraph amended in version {new_ver}.",
                "source": {
                    "page": int(ev.get("new_page") or 1),
                    "paragraph": str(ev.get("new_paragraph") or ""),
                },
            })
        elif status == "removed":
            changes.append({
                "requirement_id": rid,
                "change": "removed",
                "reason": ev.get("reason") or f"Provision removed in version {new_ver}.",
            })

    return changes


def detect_added_requirements(
    candidate_new_pars: list[dict],
    covered_summary: str,
    alignment: dict[str, Any],
) -> list[dict]:
    """Identify newly added requirements using Claude Opus."""
    if not candidate_new_pars:
        return []

    regulation = alignment["regulation"]
    old_ver = alignment["old_ver"]
    new_ver = alignment["new_ver"]

    para_lines = []
    for p in candidate_new_pars:
        para_lines.append(f"[p{p['page']}] {p['paragraph']} | {p['text']}")

    para_context = "\n\n".join(para_lines)

    system_prompt = prompts.render(
        "subgoal_added.system",
        regulation=regulation,
        old_version=old_ver,
        new_version=new_ver,
    )
    task_prompt = prompts.render(
        "subgoal_added.task",
        regulation=regulation,
        old_version=old_ver,
        new_version=new_ver,
        candidate_paragraphs=para_context,
        existing_summary=covered_summary,
    )

    content = [{"type": "text", "text": task_prompt}]
    result = llm.ask_json(system_prompt, content, ADDED_SCHEMA)
    added_list = result.get("added_requirements", [])

    changes = []
    for item in added_list:
        changes.append({
            "requirement_id": None,
            "change": "added",
            "new_text": safe_text(item.get("new_text") or ""),
            "reason": item.get("reason") or f"Paragraph {item.get('paragraph')} of {regulation} is new in version {new_ver}.",
            "source": {
                "page": int(item.get("page") or 1),
                "paragraph": str(item.get("paragraph") or ""),
            },
        })

    return changes


def run_subgoal(
    old_pdf: Path,
    new_pdf: Path,
    requirements_old_path: Path,
    team_id: str = "team-16",
    case_id: str = "subgoal-dev",
) -> dict[str, Any]:
    """Execute the complete Sub-Goal change detection pipeline."""
    llm.load_env()

    # 1. Index and align
    print(f"[subgoal] indexing and aligning {old_pdf.name} and {new_pdf.name} ...")
    alignment = index_and_align(old_pdf, new_pdf)
    regulation = alignment["regulation"]
    print(f"[subgoal] regulation: {regulation} (old: {alignment['old_ver']}, new: {alignment['new_ver']})")
    print(f"[subgoal] identical paragraphs: {len(alignment['identical_labels'])}, "
          f"modified: {len(alignment['modified_labels'])}, added: {len(alignment['added_labels'])}")

    # 2. Load requirements_old
    reqs_old = json.loads(requirements_old_path.read_text(encoding="utf-8"))
    if isinstance(reqs_old, dict) and "requirements" in reqs_old:
        reqs_old = reqs_old["requirements"]

    # 3. Partition requirements into unchanged vs candidates
    identical_labels = alignment["identical_labels"]
    candidate_reqs = []
    for r in reqs_old:
        para = r["source"]["paragraph"]
        if para not in identical_labels:
            candidate_reqs.append(r)

    print(f"[subgoal] {len(reqs_old) - len(candidate_reqs)} requirements in identical paragraphs (unchanged).")
    print(f"[subgoal] {len(candidate_reqs)} candidate requirements in changed paragraphs.")

    # 4. Evaluate existing requirements
    existing_changes = []
    if candidate_reqs:
        print("[subgoal] evaluating candidate existing requirements with Claude ...")
        existing_changes = evaluate_existing_requirements(candidate_reqs, alignment)
        print(f"[subgoal] detected {len(existing_changes)} existing changes "
              f"({sum(1 for c in existing_changes if c['change'] == 'modified')} modified, "
              f"{sum(1 for c in existing_changes if c['change'] == 'removed')} removed).")

    # 5. Filter candidate added paragraphs in technical sections
    old_map = alignment["old_map"]
    new_pars = alignment["new_pars"]
    candidate_new_pars = []
    for p in new_pars:
        lbl = p["paragraph"]
        if not is_technical_section(lbl, p["text"]) or is_heading_only(p["text"]):
            continue
        # If paragraph is new or significantly changed in new version
        if lbl not in old_map:
            candidate_new_pars.append(p)
        else:
            t_old = norm(old_map[lbl]["text"])
            t_new = norm(p["text"])
            if t_old != t_new:
                sim = text_similarity(t_old, t_new)
                if len(t_new) > len(t_old) + 40 or sim < 0.4:
                    candidate_new_pars.append(p)

    print(f"[subgoal] {len(candidate_new_pars)} candidate new paragraphs in technical sections.")

    # Summary of existing and modified obligations to avoid re-extracting covered clauses
    covered_lines = []
    for r in reqs_old:
        p = r["source"]["paragraph"]
        txt = r["text"][:100]
        covered_lines.append(f"- Requirement {r['id']} (Old Para {p}): {txt}")

    if existing_changes:
        covered_lines.append("\nAlready modified in existing requirements:")
        for c in existing_changes:
            if c["change"] == "modified":
                p = c["source"]["paragraph"]
                covered_lines.append(f"- {c['requirement_id']} now covers new paragraph {p}: {c['new_text'][:80]}...")

    covered_lines.append(
        "\nIMPORTANT NOTE: If a paragraph number in the new version was reassigned "
        "to a completely new provision that was not in the older version, treat that provision as ADDED."
    )
    covered_summary = "\n".join(covered_lines)

    # 6. Detect added requirements
    added_changes = []
    if candidate_new_pars:
        print("[subgoal] extracting added requirements from new paragraphs with Claude ...")
        added_changes = detect_added_requirements(candidate_new_pars, covered_summary, alignment)
        print(f"[subgoal] detected {len(added_changes)} added requirements.")

    # 7. Assemble submission document
    all_changes = existing_changes + added_changes
    submission = {
        "team_id": team_id,
        "case_id": case_id,
        "changes": all_changes,
    }

    return submission


def compare_with_expected(submission: dict, expected: dict) -> None:
    """Compare submission against expected answer and print PRF scores."""
    sub_changes = submission.get("changes", [])
    exp_changes = expected.get("changes", [])

    sub_mod = {c["requirement_id"] for c in sub_changes if c.get("change") == "modified"}
    sub_rem = {c["requirement_id"] for c in sub_changes if c.get("change") == "removed"}
    sub_add = [c for c in sub_changes if c.get("change") == "added"]

    exp_mod = {c["requirement_id"] for c in exp_changes if c.get("change") == "modified"}
    exp_rem = {c["requirement_id"] for c in exp_changes if c.get("change") == "removed"}
    exp_add = [c for c in exp_changes if c.get("change") == "added"]

    print("\n" + "=" * 60)
    print("SUB-GOAL EVALUATION VS EXPECTED")
    print("=" * 60)
    print(f"Total Changes: submitted={len(sub_changes)}, expected={len(exp_changes)}")

    # Modified check
    mod_match = sub_mod & exp_mod
    print(f"Modified: submitted={len(sub_mod)}, expected={len(exp_mod)}, matched={len(mod_match)}")
    if sub_mod != exp_mod:
        print(f"  extra modified: {sub_mod - exp_mod}")
        print(f"  missed modified: {exp_mod - sub_mod}")

    # Removed check
    rem_match = sub_rem & exp_rem
    print(f"Removed:  submitted={len(sub_rem)}, expected={len(exp_rem)}, matched={len(rem_match)}")
    if sub_rem != exp_rem:
        print(f"  extra removed: {sub_rem - exp_rem}")
        print(f"  missed removed: {exp_rem - sub_rem}")

    # Added check (by paragraph label)
    sub_add_paras = [c["source"]["paragraph"] for c in sub_add if c.get("source")]
    exp_add_paras = [c["source"]["paragraph"] for c in exp_add if c.get("source")]
    print(f"Added:    submitted={len(sub_add)}, expected={len(exp_add)}")
    print(f"  submitted added paragraphs: {sorted(sub_add_paras)}")
    print(f"  expected added paragraphs:  {sorted(exp_add_paras)}")
    print("=" * 60 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path, nargs="?", default=Path("data/subgoal/dev"))
    parser.add_argument("--old-pdf", type=Path, default=None)
    parser.add_argument("--new-pdf", type=Path, default=None)
    parser.add_argument("--requirements-old", type=Path, default=None)
    parser.add_argument("--expected", type=Path, default=None)
    parser.add_argument("--team-id", default=None)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--compare", action="store_true", help="compare with expected.json")
    args = parser.parse_args()

    llm.load_env()
    team_id = args.team_id or os.environ.get("TEAM_ID") or "team-16"

    case_dir = args.case_dir
    old_pdf = args.old_pdf or (case_dir / "old.pdf")
    new_pdf = args.new_pdf or (case_dir / "new.pdf")
    reqs_old_path = args.requirements_old or (case_dir / "requirements_old.json")
    expected_path = args.expected or (case_dir / "expected.json")

    if not old_pdf.exists() or not new_pdf.exists() or not reqs_old_path.exists():
        raise SystemExit(f"Input files missing in {case_dir}. Expected old.pdf, new.pdf, requirements_old.json.")

    case_id = case_dir.name
    if case_id == "dev" and "subgoal" in str(case_dir):
        case_id = "subgoal-dev"

    submission = run_subgoal(
        old_pdf=old_pdf,
        new_pdf=new_pdf,
        requirements_old_path=reqs_old_path,
        team_id=team_id,
        case_id=case_id,
    )

    out_path = args.out or (SUBMISSIONS_DIR / f"{case_id}.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(submission, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[subgoal] wrote submission with {len(submission['changes'])} changes to {out_path}")
    print(f"[subgoal] tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}")

    # Validate output
    val_script = TOOLS_DIR / "validate.py"
    if val_script.exists():
        print(f"\n[subgoal] validating {out_path} ...")
        cmd = [
            sys.executable,
            str(val_script),
            str(out_path),
            "--requirements-old",
            str(reqs_old_path),
        ]
        res = subprocess.run(cmd, check=False)
        if res.returncode != 0:
            print("[subgoal] WARNING: validation reported problems!")

    # Compare with expected if requested or available
    if (args.compare or expected_path.exists()) and expected_path.exists():
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        compare_with_expected(submission, expected)


if __name__ == "__main__":
    main()
