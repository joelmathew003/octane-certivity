# Octane × Certivity: product spec → UN Regulation requirements

Given a product specification and its drawing, this pipeline lists every requirement the product must fulfil under
UN Regulations. Each requirement cites its regulation, base version, page and paragraph. The pipeline was built for
the Certivity challenge of the Industrial AI Hackathon (team octane, `team-16`).

| Held-out case (front bumper) | Requirement F2 | Recall | Precision | Pages (P / R) | Regulations (P / R) |
|---|---|---|---|---|---|
| First run, pipeline as it was | 56.1 | 59.6 | 45.4 | 63.0 / 86.8 | 77.8 / 100 |
| Verifier, recall-first union, worked-example template | 71.6 | 83.7 | 45.4 | 67.9 / 100 | 100 / 100 |
| One run of the current pipeline (+ expert memory, 3-shortlist selection) | 74.9 | 85.1 | 50.7 | 65.8 / 94.3 | 100 / 100 |
| Majority of 5 independent runs | 76.2 | 86.5 | 51.6 | 67.1 / 96.2 | 100 / 100 |
| **Majority of 9 independent runs** (`work/make_ensemble_submission.sh`) | **77.1** | 86.5 | 53.7 | 70.4 / 94.3 | 100 / 100 |

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
   ├─ 6. Expert memory ─ paragraphs a worked example cites get its experts' own     memory.py
   │                     requirements; lamp-function slots capped at the experts' count
   │
   ├─ 7. Citation check ─ every paragraph exists, page and version match the base     citations.py
   │                      file, every number appears in the cited paragraph
   │
   └─ 8. Majority of N runs ─ steps 1-7 run N times independently; keep what most    ensemble.py
                              runs write (one-offs are mostly wrong)
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
- **Expert memory.** A certification team keeps the requirement lists of products it has certified and reuses them
  when a new product falls under the same paragraph. [memory.py](src/pipeline/memory.py) does the same with the worked
  examples. Where the pipeline cites a paragraph the experts also cited, it uses their requirements (their split and
  wording) instead of its own. In a lamp-function slot that template.py learned, it keeps at most as many requirements
  as the experts wrote for that slot. It never adds a paragraph the pipeline did not choose. On the bumper, the 119
  requirements in remembered paragraphs became the experts' 106, and slot caps removed 12 more (378 → 353).
- **Majority of independent runs.** The model calls differ from run to run, so each run writes a few requirements
  the others do not. On the dev case (3 runs, before the template and memory), a requirement only 1 run writes
  matches the experts about 10% of the time, one all 3 write about 46%. [ensemble.py](src/pipeline/ensemble.py)
  groups the runs' requirements one to one per paragraph and keeps those most runs write. Recall stays the same and
  precision goes up: on the bumper, 1 run 74.9, majority of 5 76.2, majority of 9 77.1. It also covers a bad run:
  one of the 9 left out GTR 9 at selection and was outvoted.
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
| Adding more impact-test conditions from the obligation database | — | Only about 6% matched (F2 71.6 → 69.9); the pipeline's own selection was the right amount |

## Quick start

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python data/tools/fetch_regulations.py        # regulation PDFs (not in git)
printf 'ANTHROPIC_API_KEY=...\nTEAM_ID=team-16\n' > .env
.venv/bin/python -m src.pipeline.index_pdfs             # paragraph index; the SQLite DB rebuilds itself from it

work/make_clean_submission.sh cases/heldout-front-bumper        # one run, steps 1-7
work/make_ensemble_submission.sh cases/heldout-front-bumper 9   # step 8: 9 runs in parallel, then the majority
```

`make_clean_submission.sh` runs steps 1 to 7 and writes `submissions/<case>.<YYYYMMDD-HHMM>.final.json`.
`make_ensemble_submission.sh` runs it N times in parallel on copies of the case and writes
`submissions/<case>.<YYYYMMDD-HHMM>.ensemble<N>.json`, the file we upload. Each step logs to `work/runs/<case>-*.log`; the regulation verifier's decisions, with quotes, are in
`work/runs/<case>/selection_check.json`. A case takes about 15 minutes and about $7 in API calls, plus about $4 for
each selected regulation that has no obligation database yet. Steps 3 to 7 make no model calls, so they can be rerun
for free:

```bash
.venv/bin/python -m src.pipeline.recall_first cases/<case> --vote submissions/<case>.vote-clean.json \
    --fullread submissions/<case>.fullread-clean.json
.venv/bin/python -m src.pipeline.template cases/<case> --submission submissions/<case>.recallfirst.json
.venv/bin/python -m src.pipeline.memory cases/<case> --submission submissions/<case>.template.json --name final
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
| `work/make_clean_submission.sh` | The whole chain for one case (one run). |
| `work/make_ensemble_submission.sh` | N runs in parallel, then the majority (step 8). |
| `work/regulations.db` | SQLite database: catalogue, paragraphs (FTS5), obligations. |
| `data/` | The challenge kit: cases, catalogue, tools. PDFs are downloaded, not committed. |
| `submissions/` | Every submission file, timestamped; nothing is overwritten. |
| `PROGRESS.md` | Scores of every upload, lessons, change log, procedures. |

## Limitations

- The model calls are not deterministic, so two runs of steps 1 and 2 give slightly different files. Steps 3 to 7 are
  deterministic. The current pipeline's steps 4 and 5, run on the held-out case's saved step-3 output, produce 378
  requirements; 377 of them are in the 383-requirement upload that scored 71.6.
- The template helps only for regulations a worked example covers: three of the bumper's seven (R10, R48, R148).
  Each new worked example widens it. The other four regulations keep everything the vote and the full read write.
- The base version is cited throughout, as the challenge asks; the latest versions are used only by the sub-challenge.
