"""Step 3 of the obligation path: a review agent picks, per regulation, the candidates that bind the product.

One conversation per selected regulation. Claude gets the specification, the drawings and the regulation's candidate
requirements from pipeline.retrieve, grouped by paragraph under their parent headings, and answers with the ones to
keep, each with a reason. Before answering it may call three tools that read the database: get_paragraph,
search_db and check_citation. Prompts: prompts/review_agent.*.md and prompts/tool.*.md.
"""

from __future__ import annotations

import re

try:
    from src.pipeline import db, llm, prompts, regs
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import db, llm, prompts, regs
    else:
        raise

EFFORT = "high"
MAX_TURNS = 8
HEADING_CHARS = 70
SEARCH_RESULTS = 8
SUB_PARAGRAPHS = 12
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")

TOOL_INPUTS = {
    "get_paragraph": {"paragraph": {"type": "string"}},
    "search_db": {"query": {"type": "string"}},
    "check_citation": {"candidate": {"type": "integer"}},
}

ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "keep": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"candidate": {"type": "integer"}, "reason": {"type": "string"}},
                "required": ["candidate", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["keep"],
    "additionalProperties": False,
}


def tools() -> list[dict]:
    return [{"name": name, "description": prompts.render(f"tool.{name}"), "strict": True,
             "input_schema": {"type": "object", "properties": properties, "required": list(properties),
                              "additionalProperties": False}}
            for name, properties in TOOL_INPUTS.items()]


class Review:
    """One regulation's candidates, and the tools the agent calls on the database. Build it in the thread that uses it:
    it holds its own database connection."""

    def __init__(self, regulation: str, candidates: list[dict]):
        self.regulation = regulation
        self.candidates = candidates
        self.conn = db.connect()
        self.calls: list[dict] = []

    def heading(self, label: str) -> str:
        found = db.get_paragraph(self.conn, self.regulation, label)
        return f"{label} {found['text'][:HEADING_CHARS]}" if found else label

    def listing(self) -> str:
        """The candidates, numbered, under a header per paragraph that names its two nearest parent headings."""
        lines, current = [], None
        for number, row in enumerate(self.candidates):
            if row["paragraph"] != current:
                current = row["paragraph"]
                parents = " > ".join(self.heading(label) for label in db.ancestors(current)[-2:])
                lines.append(f"\n## {current} (page {row['page']})" + (f", under {parents}" if parents else ""))
            lines.append(f"[{number}] ({row['kind']}) {row['text']}")
        return "\n".join(lines).strip()

    def children(self, found: dict) -> list[dict]:
        return db.children(self.conn, self.regulation, found, SUB_PARAGRAPHS)

    def call(self, name: str, arguments: dict) -> str:
        self.calls.append({"tool": name, **arguments})
        return getattr(self, name)(**arguments)

    def get_paragraph(self, paragraph: str) -> str:
        found = db.get_paragraph(self.conn, self.regulation, paragraph)
        if not found:
            return f"{self.regulation} has no paragraph {paragraph}"
        parents = "; ".join(self.heading(label) for label in db.ancestors(found["paragraph"])) or "none"
        subs = [f"{row['paragraph']} | {row['text'][:150]}" for row in self.children(found)]
        return "\n".join([f"[p{found['page']}] {found['paragraph']} | {found['text']}", f"Parents: {parents}",
                          "Sub-paragraphs:" + ("" if subs else " none"), *subs])

    def search_db(self, query: str) -> str:
        rows = db.search(self.conn, query, self.regulation, limit=SEARCH_RESULTS)
        return "\n".join(f"[p{row['page']}] {row['paragraph']} | {row['text'][:200]}" for row in rows) or "no matches"

    def check_citation(self, candidate: int) -> str:
        if not 0 <= candidate < len(self.candidates):
            return f"there is no candidate {candidate}"
        row = self.candidates[candidate]
        found = db.get_paragraph(self.conn, self.regulation, row["paragraph"])
        if not found:
            return f"candidate {candidate} cites {row['paragraph']}, which is not a paragraph of {self.regulation}"
        source = " ".join([found["text"], *(child["text"] for child in self.children(found))])
        missing = sorted(set(NUMBER.findall(row["text"])) - set(NUMBER.findall(source)))
        return (f"candidate {candidate} cites {found['paragraph']} on page {found['page']}; "
                + (f"numbers not found there or in its sub-paragraphs: {', '.join(missing)}" if missing
                   else "every number in it appears there"))


def select(regulation: str, candidates: list[dict], spec: str, images: list[dict]) -> tuple[list[dict], list[dict]]:
    """The candidates the agent keeps (each with its reason) and the tool calls it made."""
    review = Review(regulation, candidates)
    task = prompts.render("review_agent.task", spec=spec, regulation=regulation, count=str(len(candidates)),
                          title=regs.catalogue()[regulation]["title"], candidates=review.listing())
    answer = llm.ask_json_with_tools(
        prompts.render("review_agent.system"),
        [*images, {"type": "text", "text": task, "cache_control": {"type": "ephemeral"}}],
        ANSWER_SCHEMA, tools(), review.call, effort=EFFORT, max_turns=MAX_TURNS,
        last_turn_note=prompts.render("review_agent.last_turn"),
    )
    reasons = {item["candidate"]: item["reason"] for item in answer["keep"]}
    return [dict(row, reason=reasons[number]) for number, row in enumerate(candidates) if number in reasons], review.calls
