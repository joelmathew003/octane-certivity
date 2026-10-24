"""Vote: keep the candidates that enough independent signals agree on. No LLM, free to rerun.

    .venv/bin/python -m src.pipeline.vote cases/dev-rear-lamp \
        --pool submissions/dev-rear-lamp.obligations-no-review.json \
        --voters submissions/dev-rear-lamp.obligations.json submissions/dev-rear-lamp.obligations-lenient.json \
        --paragraph-voters submissions/dev-rear-lamp.json --min-votes 2

Every file is a submission. A requirement voter votes for each requirement it contains (same regulation, paragraph
and text as in the pool); a paragraph voter votes for every pool requirement on a paragraph it cites (e.g. the
full-read run, whose texts differ from the obligations'). A pool requirement with at least --min-votes votes is
kept. Then table paragraphs are restated (tables.py, --no-tables skips it) and the citations checked.
Writes submissions/<case>.vote.json, then validates and scores it like run.py.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from difflib import SequenceMatcher
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    from src.pipeline import citations, db, facts, llm, run, tables
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import citations, db, facts, llm, run, tables
    else:
        raise

WORD = re.compile(r"[a-z0-9]+")


def requirement_key(item: dict) -> tuple[str, str, str]:
    return item["source"]["regulation"], db.lookup_key(item["source"]["paragraph"]), " ".join(item["text"].split())


def paragraph_key(item: dict) -> tuple[str, str]:
    return item["source"]["regulation"], db.lookup_key(item["source"]["paragraph"])


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["requirements"]


def text_similarity(a: str, b: str) -> float:
    wa, wb = set(WORD.findall(a.lower())), set(WORD.findall(b.lower()))
    jaccard = len(wa & wb) / len(wa | wb) if (wa and wb) else 0.0
    seq = SequenceMatcher(None, a.lower(), b.lower()).ratio()
    return max(jaccard, seq)


def paragraph_voter_score(item: dict, by_para: dict[tuple[str, str], list[str]], is_fullread: bool) -> float:
    """Continuous [0, 1] support from a paragraph/extraction voter for a specific candidate."""
    texts = by_para.get(paragraph_key(item), [])
    if not texts:
        return 0.0
    if not is_fullread:
        return 1.0
    best_sim = max(text_similarity(item["text"], t) for t in texts)
    return 1.0 if best_sim >= 0.30 else 0.70


def probability_scores(
    pool: list[dict],
    voters: list[list[dict]],
    paragraph_voters: list[list[dict]],
) -> list[tuple[dict, float]]:
    """Compute calibrated probability score P(keep | candidate) in [0, 1] across all requirement and paragraph voters."""
    requirement_sets = [{requirement_key(item) for item in voter} for voter in voters]
    para_maps: list[tuple[dict[tuple[str, str], list[str]], bool]] = []
    for pv in paragraph_voters:
        by_para: dict[tuple[str, str], list[str]] = defaultdict(list)
        for r in pv:
            by_para[paragraph_key(r)].append(r["text"])
        is_fullread = any(not str(r.get("id", "")).startswith("P-") for r in pv)
        para_maps.append((by_para, is_fullread))

    if len(requirement_sets) == 2 and len(para_maps) == 2:
        req_weights = [0.20, 0.25]
        para_weights = [0.35, 0.20]
    elif len(requirement_sets) == 2 and len(para_maps) == 1:
        req_weights = [0.28, 0.32]
        para_weights = [0.40]
    else:
        n_total = max(1, len(requirement_sets) + len(para_maps))
        req_weights = [1.0 / n_total] * len(requirement_sets)
        para_weights = [1.0 / n_total] * len(para_maps)

    scored = []
    for item in pool:
        rk = requirement_key(item)
        prob = sum(w * (1.0 if rk in s else 0.0) for w, s in zip(req_weights, requirement_sets))
        prob += sum(w * paragraph_voter_score(item, by_para, is_fl)
                    for w, (by_para, is_fl) in zip(para_weights, para_maps))
        scored.append((item, prob))
    return scored


def vote(
    pool: list[dict],
    voters: list[list[dict]],
    paragraph_voters: list[list[dict]],
    min_votes: int = 2,
    threshold: float | None = 0.60,
) -> list[dict]:
    if threshold is not None:
        scored = probability_scores(pool, voters, paragraph_voters)
        kept = [dict(item, id=f"R-{i:04d}") for i, (item, prob) in enumerate(
            ((it, p) for it, p in scored if p >= threshold - 1e-9), 1
        )]
        return kept
    requirement_sets = [{requirement_key(item) for item in voter} for voter in voters]
    paragraph_sets = [{paragraph_key(item) for item in voter} for voter in paragraph_voters]
    kept = []
    for item in pool:
        votes = sum(requirement_key(item) in s for s in requirement_sets) + sum(paragraph_key(item) in s for s in paragraph_sets)
        if votes >= min_votes:
            kept.append(dict(item, id=f"R-{len(kept) + 1:04d}"))
    return kept


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--pool", type=Path, required=True, help="submission with every candidate")
    parser.add_argument("--voters", type=Path, nargs="*", default=[], help="submissions that vote per requirement")
    parser.add_argument("--paragraph-voters", type=Path, nargs="*", default=[], help="submissions that vote per paragraph")
    parser.add_argument("--min-votes", type=int, default=None, help="use hard integer vote threshold instead of probability")
    parser.add_argument("--threshold", type=float, default=0.60, help="probability threshold in [0, 1] (default: 0.60)")
    parser.add_argument("--no-tables", action="store_true", help="skip restating table paragraphs (tables.py)")
    parser.add_argument("--facts", type=Path, default=None, help="facts.json from pipeline.facts: drop requirements "
                                                                 "for categories the product does not have")
    parser.add_argument("--team-id", default=None, help="default: TEAM_ID from .env")
    args = parser.parse_args()

    llm.load_env()
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    use_threshold = None if args.min_votes is not None else args.threshold
    kept = vote(
        load(args.pool),
        [load(p) for p in args.voters],
        [load(p) for p in args.paragraph_voters],
        min_votes=args.min_votes or 2,
        threshold=use_threshold,
    )
    if args.facts:
        kept, dropped = facts.filter(kept, json.loads(args.facts.read_text(encoding="utf-8")))
        print(f"[facts] dropped {dropped} requirements for categories the product does not have")
    if not args.no_tables:
        kept, change = tables.restate(kept)
        print(f"[tables] restated table paragraphs: {change:+d} requirements")
    kept = [dict(item, id=f"R-{number:04d}") for number, item in enumerate(kept, 1)]
    kept, findings, examples = citations.check_all(kept)
    print(citations.report(kept, findings, examples))
    submission = {"team_id": args.team_id or os.environ.get("TEAM_ID") or "team-00", "case_id": case_dir.name,
                  "requirements": kept}
    path = run.SUBMISSIONS_DIR / f"{case_dir.name}.vote.json"
    path.write_text(json.dumps(submission, indent=2, ensure_ascii=False), encoding="utf-8")
    mode_desc = f"prob >= {use_threshold:.2f}" if use_threshold is not None else f">= {args.min_votes} votes"
    print(f"{len(kept)} of {len(load(args.pool))} candidates have {mode_desc} -> "
          f"{path.relative_to(run.REPO_ROOT)}\n")
    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)
    expected = case_dir / "expected.json"
    if expected.exists():
        subprocess.run([sys.executable, str(run.TOOLS_DIR / "score_local.py"), str(path), "--expected", str(expected)],
                       check=False)


if __name__ == "__main__":
    main()
