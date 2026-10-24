"""Obligation builder: a regulation -> every single engineering obligation in it, tagged. Runs once per regulation.

    .venv/bin/python -m src.pipeline.obligations "UN R48" "UN R148" --dry-run   # chunks and a cost estimate, no API
    .venv/bin/python -m src.pipeline.obligations "UN R48" "UN R148"
    .venv/bin/python -m src.pipeline.obligations --all

For each regulation: one call lists the devices and functions it regulates (the applies_to vocabulary, an enum in the
schema so the tags stay consistent), then one call per chunk of paragraphs writes their obligations, with the whole
regulation as a cached prefix for context. Administrative sections (definitions, approval procedure, transitional
provisions, ...) are skipped. Every answer is saved under work/obligations/cache/ by a hash of the request, so a
rerun never pays twice. The obligations go to work/obligations/<slug>_base.jsonl, which pipeline.db loads.
The prompts are in prompts/vocabulary.*.md and prompts/obligation.*.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor

try:
    from src.pipeline import db, llm, prompts, regs
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import db, llm, prompts, regs
    else:
        raise

CACHE_DIR = db.OBLIGATIONS_DIR / "cache"
EFFORT = "medium"
MAX_CHUNK_CHARS = 20000
HEADING_CHARS = 120
MAX_NAMES = 80
# for --dry-run only: averages measured on UN R148 (472 obligations from 163 shall paragraphs, $1.87)
CHARS_PER_TOKEN = 3.5
OBLIGATIONS_PER_SHALL = 2.9
TOKENS_PER_OBLIGATION = 150

# administrative sections that hold no engineering obligations
SKIP_MAIN_SECTIONS = re.compile(
    r"^(?:preamble|scope|definitions?|application for approval|approval\b|modifications?\b|"
    r"extension of approval|penalt|production definitively discontinued|names and addresses|transitional provisions)",
    re.IGNORECASE,
)
SKIP_ANNEX_SECTIONS = re.compile(
    r"^annex\s+[A-Z0-9]+\s+(?:communication\b|information document\b|arrangements? of approval markings?\b)",
    re.IGNORECASE,
)


def should_skip_section(section: str, section_title: str | None) -> bool:
    """Skip administrative sections; preserve all technical annexes and technical body sections."""
    title = section_title or section
    if section == "Preamble" or section in ("1", "2"):
        return True
    if section.startswith("Annex"):
        return bool(SKIP_ANNEX_SECTIONS.match(title))
    return bool(SKIP_MAIN_SECTIONS.match(title))
SCOPE_SECTIONS = ("Preamble", "1", "2")
HEADING_LABEL = re.compile(r"^(?:\d+(?:\.\d+)?|Annex \S+(?: Part \S+)?)$")

KINDS = {
    "construction": "design, construction, materials and dimensions of the device",
    "photometric": "luminous intensity, light distribution, colour and apparent surface of the device",
    "electrical": "light sources, control gear, failure behaviour, electrical and electromagnetic behaviour",
    "durability": "resistance to heat, water, dust, corrosion, vibration, UV and chemicals; stability over time",
    "marking": "markings on the device (trade name, approval mark, ...), their legibility and the space for them",
    "installation": "how the device is fitted to and operated on the vehicle: number, position, orientation, "
                    "geometric visibility, electrical connections, switching, tell-tales",
    "test_condition": "a test condition, procedure or pass criterion that the samples or the vehicle must meet",
    "conformity_of_production": "checks on series production and sampling",
    "administrative": "applications, documents, approval numbers, duties of authorities and Technical Services",
    "transitional": "transitional provisions and dates of application",
}
VEHICLE_CATEGORIES = ["M", "M1", "M2", "M3", "N", "N1", "N2", "N3", "O", "O1", "O2", "O3", "O4",
                      "L", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "T", "R", "S"]
KIND_LINES = "\n".join(f"  - {kind}: {meaning}" for kind, meaning in KINDS.items())  # {kinds} in the prompt

VOCABULARY_SCHEMA = {
    "type": "object",
    "properties": {"names": {"type": "array", "items": {"type": "string"}}},
    "required": ["names"],
    "additionalProperties": False,
}


def obligation_schema(names: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "obligations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "paragraph": {"type": "string"},
                        "text": {"type": "string"},
                        "kind": {"type": "string", "enum": list(KINDS)},
                        "applies_to": {"type": "array", "items": {"type": "string", "enum": [*names, "all"]}},
                        "vehicle_categories": {"type": "array",
                                               "items": {"type": "string", "enum": VEHICLE_CATEGORIES}},
                        "condition": {"type": "string"},
                    },
                    "required": ["paragraph", "text", "kind", "applies_to", "vehicle_categories", "condition"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["obligations"],
        "additionalProperties": False,
    }


def ask_cached(regulation: str, system: str, content: list[dict], schema: dict) -> dict:
    """llm.ask_json, but an identical request is answered from CACHE_DIR instead of being paid for again."""
    request = json.dumps([llm.MODEL, EFFORT, system, content, schema], sort_keys=True, ensure_ascii=False)
    path = CACHE_DIR / regs.slug(regulation) / f"{hashlib.sha256(request.encode()).hexdigest()[:20]}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    answer = llm.ask_json(system, content, schema, effort=EFFORT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(answer, indent=1, ensure_ascii=False), encoding="utf-8")
    return answer


def rows(regulation: str) -> list[dict]:
    return [dict(row) for row in regs.query(
        "SELECT paragraph, page, text, section, section_title, obligation FROM paragraphs"
        " WHERE regulation = ? AND role = 'base' ORDER BY seq", (regulation,))]


def line(row: dict) -> str:
    return f"[p{row['page']}] {row['paragraph']} | {row['text']}"


def unit_of(label: str) -> str:
    """The group a paragraph is kept together with: "6.10.4.2" -> "6.10", "Annex 6 Part 4 1.2" -> "Annex 6 Part 4 1"."""
    match = re.match(r"Annex \S+(?: Part \S+)?(?: \d+)?" if label.startswith("Annex") else r"\d+(?:\.\d+)?", label)
    return match.group() if match else label


def chunks(regulation: str) -> list[list[dict]]:
    """The paragraphs outside skipped sections, as runs of whole groups of at most MAX_CHUNK_CHARS."""
    groups: list[list[dict]] = []
    current = None
    for row in rows(regulation):
        if should_skip_section(row["section"], row["section_title"]):
            current = None
            continue
        if unit_of(row["paragraph"]) != current:
            current = unit_of(row["paragraph"])
            groups.append([])
        groups[-1].append(row)
    result: list[list[dict]] = []
    size = 0
    for group in groups:
        chars = sum(len(line(row)) for row in group)
        if result and size + chars <= MAX_CHUNK_CHARS:
            result[-1] += group
            size += chars
        else:
            result.append(list(group))
            size = chars
    return result


def vocabulary_request(regulation: str) -> tuple[str, list[dict], dict]:
    all_rows = rows(regulation)
    scope = "\n".join(line(row) for row in all_rows if row["section"] in SCOPE_SECTIONS)
    headings = "\n".join(f"{row['paragraph']} | {row['text'][:HEADING_CHARS]}" for row in all_rows
                         if row["section"] not in SCOPE_SECTIONS and HEADING_LABEL.match(row["paragraph"]))
    text = prompts.render("vocabulary.task", regulation=regulation, title=regs.catalogue()[regulation]["title"],
                          scope=scope, headings=headings)
    return prompts.render("vocabulary.system"), [{"type": "text", "text": text}], VOCABULARY_SCHEMA


def vocabulary(regulation: str) -> list[str]:
    names = ask_cached(regulation, *vocabulary_request(regulation))["names"]
    clean = dict.fromkeys(n for n in (" ".join(name.lower().split()) for name in names) if n and n != "all")
    return list(clean)[:MAX_NAMES]


def obligation_request(regulation: str, names: list[str], chunk: list[dict]) -> tuple[str, list[dict], dict]:
    paragraphs = "\n".join(line(row) for row in chunk)
    content = [
        {"type": "text", "text": prompts.render("regulation", regulation_text=regs.render(regulation)),
         "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": prompts.render("obligation.task", regulation=regulation, names=", ".join(names),
                                                first=chunk[0]["paragraph"], last=chunk[-1]["paragraph"],
                                                paragraphs=paragraphs)},
    ]
    return prompts.render("obligation.system", kinds=KIND_LINES), content, obligation_schema(names)


def accept(regulation: str, chunk: list[dict], answer: dict) -> tuple[list[dict], int]:
    """The answer's obligations as JSONL records; obligations citing a paragraph outside the chunk are dropped."""
    keys = {db.lookup_key(row["paragraph"]) for row in chunk}
    records, dropped = [], 0
    for item in answer["obligations"]:
        text = " ".join(item["text"].split())
        if not text or db.lookup_key(item["paragraph"]) not in keys:
            dropped += 1
            continue
        records.append({
            "regulation": regulation, "role": "base", "paragraph": item["paragraph"].strip(), "text": text,
            "kind": item["kind"], "condition": item["condition"].strip() or None,
            "applies_to": sorted(set(item["applies_to"])) or ["all"],
            "vehicle_categories": sorted(set(item["vehicle_categories"])), "model": llm.MODEL,
        })
    return records, dropped


def build(regulation: str, workers: int) -> None:
    names = vocabulary(regulation)
    groups = chunks(regulation)
    requests = [obligation_request(regulation, names, chunk) for chunk in groups]
    print(f"[{regulation}] {len(names)} applies_to names, {len(requests)} chunks", flush=True)
    # the first chunk writes the prompt cache (the whole regulation) that the other chunks then read
    answers = [ask_cached(regulation, *requests[0])]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        answers += pool.map(lambda request: ask_cached(regulation, *request), requests[1:])
    records, dropped = [], 0
    for chunk, answer in zip(groups, answers):
        kept, lost = accept(regulation, chunk, answer)
        records += kept
        dropped += lost
    db.OBLIGATIONS_DIR.mkdir(parents=True, exist_ok=True)
    out = db.OBLIGATIONS_DIR / f"{regs.slug(regulation)}_base.jsonl"
    tmp = out.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    tmp.replace(out)
    print(f"[{regulation}] {len(records)} obligations -> {out.relative_to(regs.REPO_ROOT)}"
          + (f" ({dropped} dropped: paragraph outside the chunk)" if dropped else ""), flush=True)


def estimate(regulation: str) -> float:
    """Rough dollars for one regulation, from character counts and the averages above."""
    price = {k: v / 1_000_000 for k, v in llm.PRICE_PER_MILLION.items()}
    groups = chunks(regulation)
    whole = len(regs.render(regulation)) / CHARS_PER_TOKEN
    own = sum(len(line(row)) for chunk in groups for row in chunk) / CHARS_PER_TOKEN
    scope = len(vocabulary_request(regulation)[1][0]["text"]) / CHARS_PER_TOKEN
    shall = sum(row["obligation"] for chunk in groups for row in chunk)
    dollars = (whole * price["cache_creation_input_tokens"] + whole * (len(groups) - 1) * price["cache_read_input_tokens"]
               + (own + scope) * price["input_tokens"]
               + shall * OBLIGATIONS_PER_SHALL * TOKENS_PER_OBLIGATION * price["output_tokens"])
    largest = max((sum(len(line(row)) for row in chunk) for chunk in groups), default=0)
    print(f"{regulation:12s} {len(groups):3d} chunks (largest {largest:6d} chars)  {shall:5d} shall paragraphs"
          f"  ≈ ${dollars:.2f}")
    return dollars


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("regulations", nargs="*", help='e.g. "UN R48"')
    parser.add_argument("--all", action="store_true", help="every regulation in the catalogue")
    parser.add_argument("--dry-run", action="store_true", help="print the chunks and a cost estimate; no API calls")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    db.ensure_fresh()
    selected = list(regs.catalogue()) if args.all else args.regulations
    unknown = set(selected) - set(regs.catalogue())
    if not selected or unknown:
        raise SystemExit(f"name regulations from the catalogue (or --all); unknown: {', '.join(sorted(unknown))}")
    if args.dry_run:
        print(f"total ≈ ${sum(estimate(regulation) for regulation in selected):.2f}  (rough: character counts and "
              f"{OBLIGATIONS_PER_SHALL} obligations x {TOKENS_PER_OBLIGATION} output tokens per shall paragraph)")
        return
    llm.load_env()
    for regulation in selected:
        build(regulation, args.workers)
    print(f"tokens: {dict(llm.usage)}  cost: ${llm.cost_dollars():.2f}")
    db.ensure_fresh()


if __name__ == "__main__":
    main()
