"""The obligation path: product profile (step 1), SQL filter over the obligations (step 2) and review (step 3).

    .venv/bin/python -m src.pipeline.retrieve cases/dev-rear-lamp --regulations "UN R148" "UN R150" "UN R48" "UN R10"
    .venv/bin/python -m src.pipeline.retrieve cases/dev-rear-lamp      # selects the regulations first, as run.py does

1. For each selected regulation, Claude picks the applies_to names (the regulation's own, from the obligations table)
   whose requirements bind the product, and the product's vehicle categories (prompts/profile.*.md).
2. SQL takes every obligation of the regulation that carries one of those names or "all" and fits those vehicle
   categories, except transitional and administrative ones; administrative ones that require type approval stay.
3. The review agent (pipeline.review_agent) keeps, per regulation, what binds the product; it sees the drawings too
   and can look paragraphs up in the database.

The submission goes to submissions/<case>.obligations.json (with --no-review: <case>.obligations-no-review.json),
next to run.py's, and is validated and scored the same way. Each step's output is saved under
work/runs/<case>/obligations/ (or obligations-no-review/). The selected regulations need obligations first:
`.venv/bin/python -m src.pipeline.obligations "UN R48"`.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from src.pipeline import db, llm, obligations, prompts, regs, review_agent, run
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import db, llm, obligations, prompts, regs, review_agent, run
    else:
        raise

CANDIDATES_SQL = """
SELECT o.paragraph, o.text, o.kind, p.page FROM obligations o JOIN paragraphs p ON p.id = o.paragraph_id
WHERE o.regulation = ? AND o.role = 'base'
  AND o.kind != 'transitional'
  AND (o.kind != 'administrative' OR o.text LIKE '%type approved%' OR o.text LIKE '%type-approved%')
  AND EXISTS (SELECT 1 FROM obligation_tags t, json_each(?) name
              WHERE t.obligation_id = o.id AND t.facet = 'applies_to' AND t.value = name.value)
  AND (NOT EXISTS (SELECT 1 FROM obligation_tags t WHERE t.obligation_id = o.id AND t.facet = 'vehicle_category')
       OR EXISTS (SELECT 1 FROM obligation_tags t, json_each(?) category
                  WHERE t.obligation_id = o.id AND t.facet = 'vehicle_category' AND t.value = category.value))
ORDER BY p.seq, o.id
"""


def names(regulation: str) -> list[str]:
    """The applies_to names the regulation's obligations use, most used first; "all" is always added by the filter."""
    rows = regs.query("SELECT t.value FROM obligation_tags t JOIN obligations o ON o.id = t.obligation_id"
                      " WHERE o.regulation = ? AND t.facet = 'applies_to' AND t.value != 'all'"
                      " GROUP BY t.value ORDER BY count(*) DESC, t.value", (regulation,))
    return [row["value"] for row in rows]


def profile_schema(options: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "applies_to": {"type": "array", "items": {"type": "string", "enum": options}},
            "vehicle_categories": {"type": "array", "items": {"type": "string", "enum": obligations.VEHICLE_CATEGORIES}},
            "reason": {"type": "string"},
        },
        "required": ["applies_to", "vehicle_categories", "reason"],
        "additionalProperties": False,
    }


def profile(regulation: str, spec: str, images: list[dict]) -> dict:
    """Step 1: the regulation's names that bind the product, and the product's vehicle categories."""
    options = names(regulation)
    task = prompts.render("profile.task", spec=spec, regulation=regulation, names="\n".join(options),
                          title=regs.catalogue()[regulation]["title"])
    return llm.ask_json(prompts.render("profile.system"), [*images, {"type": "text", "text": task}],
                        profile_schema(options))


def category_tags(categories: list[str]) -> list[str]:
    """Category tags an obligation may carry and still bind these vehicles: M1 -> M1, M; M -> M, M1, M2, M3."""
    if not categories:
        return obligations.VEHICLE_CATEGORIES  # the specification names none: do not filter on categories
    tags = set()
    for category in categories:
        tags |= {category, category[0], *(c for c in obligations.VEHICLE_CATEGORIES if c.startswith(category))}
    return sorted(tags)


def candidates(regulation: str, chosen: dict) -> list[dict]:
    """Step 2: every obligation of the regulation that the profile selects."""
    rows = regs.query(CANDIDATES_SQL, (regulation, json.dumps([*chosen["applies_to"], "all"]),
                                       json.dumps(category_tags(chosen["vehicle_categories"]))))
    return [dict(row) for row in rows]


def requirement(regulation: str, row: dict) -> dict:
    source = {"regulation": regulation, "version": regs.version_label(regulation), "page": row["page"],
              "paragraph": row["paragraph"]}
    return {"id": "", "text": row["text"][:run.MAX_TEXT], "source": source}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--team-id", default=None, help="default: TEAM_ID from .env")
    parser.add_argument("--regulations", nargs="+", default=None, help="skip selection and use these")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--no-review", action="store_true", help="submit every candidate (skip step 3)")
    args = parser.parse_args()

    db.ensure_fresh()
    llm.load_env()
    team_id = args.team_id or os.environ.get("TEAM_ID") or "team-00"
    case_dir = next((base / args.case_dir for base in (run.DATA_DIR, run.REPO_ROOT) if (base / args.case_dir).exists()),
                    args.case_dir).resolve()
    case_id = case_dir.name
    variant = "obligations-no-review" if args.no_review else "obligations"
    out_dir = run.RUNS_DIR / case_id / variant
    out_dir.mkdir(parents=True, exist_ok=True)
    save = lambda name, data: (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False),  # noqa: E731
                                                          encoding="utf-8")
    spec, images = run.case_inputs(case_dir)

    selected = args.regulations or [choice["regulation"] for choice in run.select_regulations(spec, images)]
    unknown = set(selected) - set(regs.catalogue())
    if unknown:
        raise SystemExit(f"not in regulations/index.json: {', '.join(sorted(unknown))}")
    missing = [regulation for regulation in selected if not names(regulation)]
    if missing:
        quoted = " ".join(f'"{regulation}"' for regulation in missing)
        raise SystemExit(f"no obligations yet for {', '.join(missing)}: "
                         f"run `.venv/bin/python -m src.pipeline.obligations {quoted}` first")
    save("selected.json", selected)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        profiles = dict(zip(selected, pool.map(lambda regulation: profile(regulation, spec, images), selected)))
    save("profile.json", profiles)
    pools = {}
    for regulation in selected:
        chosen = profiles[regulation]
        pools[regulation] = candidates(regulation, chosen)
        print(f"[profile] {regulation:9s} {len(pools[regulation]):4d} candidates  categories "
              f"{','.join(chosen['vehicle_categories'])}  names: {', '.join(chosen['applies_to'])}", flush=True)
    save("candidates.json", pools)

    if args.no_review:
        kept = pools
    else:
        print(f"[review] one review agent per regulation, {sum(map(len, pools.values()))} candidates ...", flush=True)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            reviews = dict(zip(selected, pool.map(
                lambda regulation: review_agent.select(regulation, pools[regulation], spec, images), selected)))
        kept = {regulation: rows for regulation, (rows, _) in reviews.items()}
        save("review.json", {regulation: {"kept": rows, "tool_calls": calls}
                             for regulation, (rows, calls) in reviews.items()})
        for regulation, (rows, calls) in reviews.items():
            print(f"[review] {regulation:9s} kept {len(rows):4d} of {len(pools[regulation]):4d}"
                  f"  ({len(calls)} tool calls)")

    rows = [(regulation, row) for regulation in selected for row in kept[regulation]]
    requirements = [dict(requirement(regulation, row), id=f"R-{number:04d}")
                    for number, (regulation, row) in enumerate(rows, 1)]
    submission = {"team_id": team_id, "case_id": case_id, "requirements": requirements}
    run.SUBMISSIONS_DIR.mkdir(exist_ok=True)
    path = run.SUBMISSIONS_DIR / f"{case_id}.{variant}.json"
    path.write_text(json.dumps(submission, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(requirements)} requirements -> {path.relative_to(run.REPO_ROOT)}")
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}\n")

    subprocess.run([sys.executable, str(run.TOOLS_DIR / "validate.py"), str(path)], check=False)
    expected = case_dir / "expected.json"
    if expected.exists():
        subprocess.run([sys.executable, str(run.TOOLS_DIR / "score_local.py"), str(path), "--expected", str(expected)],
                       check=False)


if __name__ == "__main__":
    main()
