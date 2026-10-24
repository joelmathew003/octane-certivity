"""Restate table paragraphs the way the experts write them (no LLM, free).

When a paragraph says "... shall meet the requirements in Table 4", the experts write one requirement that restates the
paragraph's own sentence, while the obligation builder writes one requirement per table row. So for every paragraph
with a table that several selected requirements cite, this step adds the paragraph's own sentences that require
something (verbatim, cut before the table caption). It keeps the rows, since the experts do split some tables (one
requirement per test pulse), unless a paragraph has so many rows that they are almost surely too fine (REPLACE_OVER).

On the dev case, after the vote: proxy F2 69.2 -> 70.7 and F1 61.3 -> 62.6, at the same number of requirements.
"""

from __future__ import annotations

import re
from collections import defaultdict

try:
    from src.pipeline import db
except ModuleNotFoundError as e:
    if e.name in ("src", "src.pipeline"):
        from pipeline import db
    else:
        raise

MIN_GROUP = 1      # add the paragraph's sentences when at least this many requirements cite it
REPLACE_OVER = 10  # and drop the rows when there are at least this many
CAPTION = re.compile(r"\bTable [A-Z]?\d+[a-z]?(?:[-.]\d+)?\s+(?=[A-Z])")
HEADING = re.compile(r"^[^:]{0,80}:\s+")  # "Luminous intensity and standard light distribution: ..."
SENTENCE = re.compile(r"(?<=[.;])\s+(?=[A-Z])")
OBLIGATION = re.compile(r"\b(shall|must)\b", re.IGNORECASE)
TABLE_SUFFIX = re.compile(r"\.?\s*Table\s+\S+$", re.IGNORECASE)


def own_sentences(text: str) -> list[str]:
    """The sentences of a paragraph that come before its table caption and require something."""
    caption = CAPTION.search(text)
    head = HEADING.sub("", text[:caption.start()] if caption else text)
    return [sentence.strip() for sentence in SENTENCE.split(head) if OBLIGATION.search(sentence)]


def restate(requirements: list[dict], min_group: int = MIN_GROUP, replace_over: int = REPLACE_OVER) -> tuple[list[dict], int]:
    """The requirements with the table paragraphs restated; also how many requirements were added (or removed, < 0)."""
    conn = db.connect()
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in requirements:
        source = item["source"]
        groups[(source["regulation"], db.lookup_key(TABLE_SUFFIX.sub("", source.get("paragraph") or "")))].append(item)
    result: list[dict] = []
    for (regulation, key), items in groups.items():
        found = db.get_paragraph(conn, regulation, key)
        sentences = own_sentences(found["text"]) if found and CAPTION.search(found["text"]) else []
        if len(items) < min_group or not sentences:
            result += items
            continue
        have = {" ".join(item["text"].split()) for item in items}
        source = dict(items[0]["source"], paragraph=found["paragraph"], page=found["page"])
        result += [] if len(items) >= replace_over else items
        result += [{"id": "", "text": sentence, "source": source} for sentence in sentences
                   if " ".join(sentence.split()) not in have]
    return result, len(result) - len(requirements)
