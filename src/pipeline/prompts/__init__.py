"""The prompts sent to Claude, one Markdown file each in this folder.

    prompts.render("obligation.task", regulation="UN R48", names="stop lamp, ...", ...)

A file holds the exact text sent to the model; its final newline is dropped. {name} marks a placeholder, filled in a
single pass, so text substituted in is never scanned again; braces around anything else are literal text.
<step>.system.md is a system prompt, <step>.task.md the instruction in the user turn, and the other files wrap
context blocks (regulation.md, select.catalogue.md).

NOTE: pipeline.obligations keys its answer cache on the exact request text, so any edit here, even whitespace,
makes the next builder run pay again for every chunk.
"""

from __future__ import annotations

import re
from functools import cache
from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent
PLACEHOLDER = re.compile(r"\{(\w+)\}")


@cache
def template(name: str) -> str:
    return (PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8").removesuffix("\n")


def render(name: str, **values: str) -> str:
    text = template(name)
    unused = sorted(key for key in values if "{" + key + "}" not in text)
    if unused:
        raise KeyError(f"prompts/{name}.md has no placeholder {', '.join(unused)}")
    return PLACEHOLDER.sub(lambda match: values.get(match.group(1), match.group()), text)
