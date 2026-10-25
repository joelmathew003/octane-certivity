# Octane × Certivity: product spec → UN Regulation requirements

Given a product specification and its drawing, this pipeline lists every requirement the product must fulfil under
UN Regulations. Each requirement cites its regulation, base version, page and paragraph. The pipeline was built for
the Certivity challenge of the Industrial AI Hackathon (team octane, `team-16`).

| Held-out case (front bumper) | Requirement F2 | Recall | Precision | Pages (P / R) | Regulations (P / R) |
|---|---|---|---|---|---|
| First run, pipeline as it was | 56.1 | 59.6 | 45.4 | 63.0 / 86.8 | 77.8 / 100 |
| **Current pipeline** (verifier, recall-first union, worked-example template) | **71.6** | 83.7 | 45.4 | 67.9 / 100 | 100 / 100 |

The leaderboard ranks by requirement-level F2, which weights recall more than precision. Every upload, and what
each change did to the score, is in [PROGRESS.md](PROGRESS.md), section 0.

## How it works

```
spec.md + drawing
   │
   ├─ 1. Select regulations ─ shortlist from the catalogue, then verify each one on its own   run.py
   │                          (is it about this product, or about the whole vehicle?)
   │
   ├─ 2. Read, three independent ways                                       (Claude, base-version text only)
   │     a. full read: each selected regulation, paragraph by paragraph       run.py --no-review
   │     b. obligation path: a one-time obligation database per regulation    obligations.py, retrieve.py
   │        → SQL filter on the product profile → strict review agent          review_agent.py
   │        → the same pool through a lenient review                          review.py
   │     c. paragraph judge: which paragraphs of the pool would an expert cite paragraph_judge.py
   │
   ├─ 3. Vote ─ probability from the 4 voters, threshold 0.30; product facts drop   vote.py, facts.py,
   │            other device classes; tables restated row by row                    tables.py
   │
   ├─ 4. Recall-first union ─ add full-read sentences the vote has not covered       recall_first.py
   │
   ├─ 5. Worked-example template ─ for regulations a worked example covers, keep     template.py
   │                               only the kinds of paragraph its experts cite
   │
   └─ 6. Citation check ─ every paragraph exists, page and version match the base     citations.py
                          file, every number appears in the cited paragraph
```

Underneath: [index_pdfs.py](src/pipeline/index_pdfs.py) splits every regulation PDF (PyMuPDF) into paragraphs with
page and label, and [db.py](src/pipeline/db.py) loads them into SQLite with FTS5 full-text search.
[obligations.py](src/pipeline/obligations.py) turns each regulation into tagged single obligations once; the result is
cached by paragraph text, so a regulation is paid for only once. The architecture diagram is
[architecture.excalidraw](architecture.excalidraw).

### Design decisions

- **Recall first.** With F2 = 5·matches / (4·gold + n), a requirement is worth adding when at least about F2/5 (≈13%)
  of such requirements match. On a new product, the requirements only one source writes still match at about 25%.
  That is why the vote runs at a low threshold and the full read's extra sentences are added (held-out: recall 60% → 88%).
- **Exhaustive filter, not top-k retrieval.** Step 2b filters the whole obligation database with SQL on the product
  profile. Nothing is lost to a similarity cut-off, and the review then decides what binds the product.
- **Independent voters.** The full read and the obligation path miss different things. The vote keeps what enough of
  them agree on, weighted by how often each voter was right on the worked example.
- **Learn expert style from the worked example, without hand rules.** The kit publishes a worked example with the
  experts' answers. [template.py](src/pipeline/template.py) learns from it which kinds of paragraph experts cite:
  - the paragraphs they cite, and their sub-paragraphs;
  - a clause they cite for at least 3 functions, when those clauses open with the same words (for example "Colour:"
    in every lamp section of R148, or "Number" in R48).

  It applies this only to regulations the worked example covers, and never reads the case's own answers. On the
  held-out bumper it removed 161 requirements, mostly approval-mark layout, annex lab procedures, conformity of
  production, and lamp presence and orientation lines. Precision went from 34% to 45%: F2 66.9 → 71.6.
- **Every citation checked by code.** Page and version come from the base PDF, never from the model, and a number in
  a requirement that the cited paragraph does not contain is reported.
- **Prompts are files.** Every prompt is in [src/pipeline/prompts/](src/pipeline/prompts/). No prompt contains an
  example from an answer key.

### What did not work

These experiments are measured in PROGRESS.md and left out of the default chain:

| Experiment | Module | What happened |
|---|---|---|
| LLM scope filter (drop paragraphs by category) | `scope.py` | +3 on the dev case, but on the held-out case its cuts lost real matches |
| Per-requirement relevance judge | `relevance.py` | Most wrong requirements look plausible even to a careful reviewer |
| Completion, dedupe and editor passes | `complete.py`, `dedupe.py`, `editor.py` | Neutral |
| Cutting lab procedures in the product's core regulations | — | Lost matches (F2 71.6 → 66.7): for a bumper, the experts list the pedestrian and impact test conditions |

## Quick start

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python data/tools/fetch_regulations.py        # regulation PDFs (not in git)
printf 'ANTHROPIC_API_KEY=...\nTEAM_ID=team-16\n' > .env
.venv/bin/python -m src.pipeline.index_pdfs             # paragraph index; the SQLite DB rebuilds itself from it

work/make_clean_submission.sh cases/heldout-front-bumper
```

The script runs steps 1 to 6 and writes `submissions/<case>.<YYYYMMDD-HHMM>.final.json`, which is the file to
upload. Each step logs to `work/runs/<case>-*.log`; the regulation verifier's decisions, with quotes, are in
`work/runs/<case>/selection_check.json`. A case takes about 15 minutes and about $7 in API calls, plus about $4 for
each selected regulation that has no obligation database yet. Steps 3 to 6 make no model calls, so they can be rerun
for free:

```bash
.venv/bin/python -m src.pipeline.recall_first cases/<case> --vote submissions/<case>.vote-clean.json \
    --fullread submissions/<case>.fullread-clean.json
.venv/bin/python -m src.pipeline.template cases/<case> --submission submissions/<case>.recallfirst.json --name final
.venv/bin/python -m src.pipeline.citations submissions/<case>.final.json      # citation report
.venv/bin/python data/tools/validate.py submissions/<case>.final.json         # kit's format check
```

All modules run from the repository root as `.venv/bin/python -m src.pipeline.<module>`. Each module's docstring
gives its usage, its inputs and outputs, and its cost.

## Repository layout

| Path | What |
|---|---|
| `src/pipeline/` | The main pipeline. Each module is one step; the first line of each docstring says what it does. |
| `src/pipeline/prompts/` | All prompts, as Markdown templates. |
| `src/pipeline/subgoal.py` | Sub-challenge: what changed between two versions of a regulation. |
| `src/api/`, `frontend/`, `run_demo.sh` | Demo UI and its API server (see `frontend/README.md`). |
| `work/make_clean_submission.sh` | The whole chain for one case. |
| `work/regulations.db` | SQLite database: catalogue, paragraphs (FTS5), obligations. |
| `data/` | The challenge kit: cases, catalogue, tools. PDFs are downloaded, not committed. |
| `submissions/` | Every submission file, timestamped; nothing is overwritten. |
| `PROGRESS.md` | Scores of every upload, lessons, change log, procedures. |

## Limitations

- The model calls are not deterministic, so two runs of steps 1 and 2 give slightly different files. Steps 3 to 6 are
  deterministic. The current pipeline's steps 4 and 5, run on the held-out case's saved step-3 output, produce 378
  requirements; 377 of them are in the 383-requirement upload that scored 71.6.
- The template helps only for regulations a worked example covers: three of the bumper's seven (R10, R48, R148).
  Each new worked example widens it. The other four regulations keep everything the vote and the full read write.
- The base version is cited throughout, as the challenge asks; the latest versions are used only by the sub-challenge.
