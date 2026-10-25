"""Split every regulation PDF into paragraphs: (regulation, version, page, paragraph, text).

    .venv/bin/python -m src.pipeline.index_pdfs                # base versions -> work/index/
    .venv/bin/python -m src.pipeline.index_pdfs --role latest

Paragraph labels follow the expected files: "5.1.4.3" in the main body; annex paragraphs keep their own
numbering behind the annex (and part) prefix: "Annex 5 1.1", "Annex 6 Part 4 4.1".
Each record keeps the page where the paragraph starts and the page where it ends.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pymupdf

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" if (REPO_ROOT / "data").exists() else REPO_ROOT / "industrial-ai-hackathon"
INDEX_JSON = DATA_DIR / "regulations" / "index.json"
PDF_DIR = DATA_DIR / "regulations" / "pdf"
OUT_DIR = REPO_ROOT / "work" / "index"

PAGE_HEADER = re.compile(r"^.+, version .+ \| page \d+ of \d+$")
# "3.3.2.5.1.1. The arrow" / "1. General" / "1 Scope": a number, then a capital, a quote or a bracket
PARAGRAPH = re.compile(r"^((?:\d+\.)*\d+)\.?\s+(?=[A-Z(\"'“‘•])")
ANNEX = re.compile(r"^Annex (\d+[A-Z]?)\s+[A-Z]")
PART = re.compile(r"^Part ([A-Z0-9]+)\s*[:\-–]")


@dataclass
class Paragraph:
    regulation: str
    version: str
    role: str
    file: str
    paragraph: str
    page: int
    end_page: int
    annex: str | None
    lines: list[str] = field(default_factory=list)

    def record(self) -> dict:
        data = asdict(self)
        data["text"] = " ".join(data.pop("lines")).strip()
        return data


def annex_number(label: str) -> tuple[int, str]:
    digits = re.match(r"\d+", label)
    return int(digits.group()) if digits else 0, label


def split_pdf(path: Path, regulation: str, version: str, role: str) -> list[dict]:
    document = pymupdf.open(path)
    paragraphs: list[Paragraph] = []
    annex: str | None = None
    part: str | None = None
    current: Paragraph | None = None

    def start(label: str, page: int, first_line: str) -> None:
        nonlocal current
        prefix = " ".join(x for x in (f"Annex {annex}" if annex else "", f"Part {part}" if part else "") if x)
        current = Paragraph(regulation, version, role, path.name, f"{prefix} {label}".strip(), page, page, annex)
        current.lines.append(first_line)
        paragraphs.append(current)

    for page_number, page in enumerate(document, start=1):
        for line in page.get_text().splitlines():
            line = line.strip()
            if not line or PAGE_HEADER.match(line):
                continue
            if (match := ANNEX.match(line)) and (
                annex is None or annex_number(match.group(1)) > annex_number(annex)
            ) and page_number > 2:
                annex, part = match.group(1), None
                start("", page_number, line)  # the annex heading is its own record
                continue
            if annex and (match := PART.match(line)):
                part = match.group(1)
                start("", page_number, line)
                continue
            if match := PARAGRAPH.match(line):
                start(match.group(1), page_number, line[match.end():])
                continue
            if current is None:
                start("Preamble", page_number, line)
                continue
            current.lines.append(line)
            current.end_page = page_number
    return [p.record() for p in paragraphs]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", default="base", choices=["base", "latest"])
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for entry in json.loads(INDEX_JSON.read_text(encoding="utf-8")):
        slug = "_".join(entry["regulation"].replace("/", " ").split())
        for version in entry["versions"]:
            if version["role"] != args.role:
                continue
            records = []
            for file in version["files"]:
                path = PDF_DIR / slug / args.role / file["name"]
                records += split_pdf(path, entry["regulation"], version["version_label"], args.role)
            out = OUT_DIR / f"{slug}_{args.role}.jsonl"
            with out.open("w", encoding="utf-8") as handle:
                handle.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in records)
            print(f"{entry['regulation']:12s} {version['version_label']:10s} {len(records):5d} paragraphs -> {out.name}")


if __name__ == "__main__":
    main()
