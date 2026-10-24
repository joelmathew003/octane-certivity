# Progress report: Octane × Certivity

Updated: 2026-10-24, 19:30 (Saturday)

Status: The vote of three methods with the table step is the best result: requirement F2 67.8 and F1 62.3 on the platform (number 3 on the leaderboard). The best result before the vote was F1 52.8.

## 1. Scores

### 1.1 Platform scores (dev case "Worked example: vehicle rear lamp")

Only the platform measures the requirement level. The platform accepts 5 uploads in each hour.

IMPORTANT: The leaderboard ranks the teams by requirement F2. F2 counts recall more than precision. At 19:30 we were number 5 of 9 (F2 64.9). Number 1 had F2 76.2 at recall 89.5.

| Upload | Method | Reqs | Req P | Req R | Req F1 | Req F2 | Page F1 | Regulation F1 |
|---|---|---|---|---|---|---|---|---|
| 17:49 | Full read + lenient review (`run.py`, from Joel's computer) | 185 | 53.5 | 52.1 | 52.8 | 52.4 | **92.6** | 100 |
| 18:10 | Full read, other run (from Joel's computer) | 208 | 50.0 | 54.7 | 52.3 | 53.7 | 89.1 | 100 |
| 18:23 | Obligation path + lenient review (`review.py`) | 399 | 37.6 | **78.9** | 50.9 | 64.7 | 77.9 | 100 |
| 18:49 | Obligation path + review agent v1 | 172 | 54.7 | 49.5 | 51.9 | 50.4 | 84.6 | 100 |
| 19:21 | Vote: 2 of 3 (agent v1, lenient review, full read) | 250 | 52.0 | 68.4 | 59.1 | 64.4 | 90.9 | 100 |
| 19:21 | Vote: 2 of 3 (agent v2, lenient review, full read) | 280 | 48.2 | 71.1 | 57.4 | 64.9 | 87.0 | 100 |
| 19:47 | Vote (agent v1) + table paragraphs restated (`vote-agent1-tables`) | 250 | **54.8** | 72.1 | **62.3** | **67.8** | 90.9 | 100 |
| 19:54 | Vote (agent v2) + table paragraphs restated (`vote-agent2-tables`) | 280 | 50.0 | 73.7 | 59.6 | 67.3 | 87.0 | 100 |

- The table step (`tables.py`) adds 3.4 points of F2 and 3.2 points of F1 on the platform.
- The strict agent v1 is the better voter, also for F2 (67.8 against 67.3). The proxy ranked these two files the wrong way: do not use it for differences of approximately 1 point.
- With F2 67.8 we are number 3 on the leaderboard.
- A stricter agent makes a better vote: the lenient review gives the recall, so the agent must give the precision.

### 1.2 Offline scores (every file in `submissions/`)

| File `dev-rear-lamp.<name>.json` | Method | Reqs | Proxy P | Proxy R | Proxy F1 | Page F1 | Cost |
|---|---|---|---|---|---|---|---|
| `dev-rear-lamp.json` | Full read (`run.py`, before the lenient review existed) | 182 | 42.9 | 41.1 | 41.9 | 0.909 | $2.51 |
| `obligations-joel-review` | Obligation path + lenient review | 399 | 38.8 | 81.6 | 52.6 | 0.779 | $1.74 |
| `obligations-no-review` | Obligation path, all candidates | 1,137 | 14.3 | 85.8 | 24.6 | 0.510 | $0.17 |
| `obligations-agent-v1` | Obligation path + review agent v1 | 172 | 52.3 | 47.4 | 49.7 | 0.846 | $1.16 |
| `obligations-agent-v2` | Obligation path + review agent v2 | 242 | 49.2 | 62.6 | 55.1 | 0.814 | $1.26 |
| `vote-agent1-lenient-fullread` | Vote: 2 of 3 (agent v1, lenient review, full read) | 250 | 54.8 | 72.1 | **62.3** | 0.909 | $0 |
| `vote-agent2-lenient-fullread` | Vote: 2 of 3 (agent v2, lenient review, full read) | 280 | 51.4 | 75.8 | 61.3 | 0.870 | $0 |
| `vote-agent1-tables` | Vote (agent v1) + table paragraphs restated (`tables.py`) | 250 | 56.0 | 73.7 | 63.6 | 0.909 | $0 |
| `vote-agent2-tables` | Vote (agent v2) + table paragraphs restated (`tables.py`) | 280 | 52.5 | 77.4 | 62.6 | 0.870 | $0 |

- Proxy F2: `vote-agent2-tables` 70.7 against 69.2 for `vote-agent2-lenient-fullread` (platform 64.9). Upload `vote-agent2-tables` next.

- Proxy: our requirements and the expected ones are paired one to one in each cited paragraph. A pair counts when the text similarity is 0.65 or more. On the three uploads of files that we have (399, 172 and 250 requirements), the proxy is from 2 points below to 4 points above the platform. Use it to compare files, not as a score.
- Page F1: `data/tools/score_local.py`.
- A vote costs $0. It uses the outputs that the other runs made.

NOTE: The proxy, the keep rates in the review prompt and all dev scores use the answer key of the dev case. Expect a lower score on the held-out case.

### 1.3 Cost

- Obligations for the 4 dev regulations (one time): $11.79.
- Total use of the hackathon credits until now: approximately $18.60 of $150.

## 2. Architecture now

The diagram `architecture.excalidraw` shows it. Section 4 is a table of the inputs and outputs of each step. Section 6 shows each module.

1. Data prep (one time, no LLM): `index_pdfs.py` splits the PDFs into paragraphs. `db.py` loads everything into `work/regulations.db`. All steps read the database.
2. Obligation builder (one time for each regulation, Claude): `obligations.py` writes each obligation of a regulation as one requirement, with tags.
3. Path A, full read (`run.py`): Claude selects the regulations, reads each one in full and writes the requirements. The lenient review (`review.py`) prunes them.
4. Path B, obligations (`retrieve.py`): Claude picks the product's tags (step 1). SQL takes the candidates (step 2). The review agent (`review_agent.py`) or the lenient review keeps what binds the product (step 3).
5. Vote (`vote.py`, no LLM): keep a candidate when 2 of 3 voters agree. Then `tables.py` restates table paragraphs: when several requirements cite a paragraph with a table, it adds the paragraph's own sentences, because the experts write one requirement for "shall meet the requirements in Table 4".
6. Citation check (`citations.py`, no LLM): it fixes version and page, and it reports numbers that are not in the cited paragraph. `run.py`, `retrieve.py` and `vote.py` run it before they write a file.

## 3. Review of the architecture

1. The requirement level is the weak point. The regulation level is 100% and the page level is approximately 90%.
2. Each method alone gives a requirement F1 of 51 to 53. The full read writes fewer requirements than the experts on split paragraphs (tables, lists). The obligation path splits like the experts, but its reviews keep too much or too little.
3. The vote is the strongest step that we found. A strict voter, a lenient voter and an independent method together are better than each one alone (platform F1 59.1 against 52.8).
4. The review agent did not call its tools in 3 runs. It decides from the candidate list. The tools are ready, but they add no value now.
5. Step 1 (product profile) is not deterministic. Two runs gave 167 and 188 candidates for UN R150. Thus the voters must use the same pool. Run step 1 one time and keep its output.
6. The full read and the lenient review do not see the drawing. The drawing has the facts that decide categories (for example "60 to 185 cd" = stop lamp S1).
7. The citation check shows that the obligation path is more faithful: approximately 97% of its requirements are clean, against 81% for the full read.
8. On Sunday, a run needs several commands. One command for all steps decreases the risk of an error.

## 4. Proposed next architecture

Section 5 of the diagram (gray box) shows it.

| Idea | Why | Cost | Status |
|---|---|---|---|
| Vote of 3 voters | Platform F1 59.1 against 52.8 | $0 | Built (`vote.py`) |
| Citation check | Fixes pages and versions, flags invented numbers | $0 | Built (`citations.py`) |
| Step 1 one time, kept for all voters | All voters see the same pool | $0 | Not built |
| One command for Sunday (`ensemble`) | Fewer manual steps | $0 | Not built |
| Build missing obligations automatically | The held-out case can need new regulations | ~$2–4 per regulation | Built (`retrieve.py --build-missing`) |
| Offline proxy judge in the repository | Tune without platform uploads | $0 | Script only, not in the repository |
| Product facts from the drawing callouts | Finer tags (S1, R1, class IA) | Small | Not built |
| Recall sweep with `search_db` | Find obligations that the filter missed | ~$1 per run | Not built |

## 5. Change log

| Commit | Author | Change |
|---|---|---|
| `49ff859` | ishwargov | Pipeline: index, catalogue, LLM wrapper, `run.py` |
| `eb0d10e` | Joel Mathew | New layout: `data/` and `src/` |
| `e13b744` | ishwargov | `db.py` and the design diagram |
| `dc46da8` | ishwargov | `work/regulations.db` in git |
| `42226eb` | ishwargov | Diagram fonts and status colours |
| `debd403` | ishwargov | This file, first version |
| `04c1e7c` | ishwargov | All reads go through the database |
| `2b6e692` | Joel Mathew | Lenient review (`review.py`) in `run.py` |
| `2ca19d6` | ishwargov | Obligation builder, prompts in `src/pipeline/prompts/` |
| `4480e3c` | ishwargov | Obligations for UN R148, R150, R48 and R10 |
| `90b21c6` | Joel Mathew | Prompts of `review.py` in files |
| `71fed5c` | ishwargov | Obligation path (`retrieve.py`) |
| `3761c46` | ishwargov | Diagram status update |
| `f9c1ffb` | ishwargov | New drawing for the dev case (callouts) |
| `9157e0d` | ishwargov | Review agent (`review_agent.py`) and tool loop in `llm.py` |
| `acb9b6f` | ishwargov | Diagram section 4 |
| not committed | — | Review agent prompt v2 (keeps markings and test parameters) |
| not committed | — | `vote.py`, `citations.py`; `retrieve.py --reviewer` and `--build-missing` |
| not committed | — | `tables.py`: restate table paragraphs after the vote (proxy F2 +1.5) |
| not committed | — | Diagram: sections 4 to 6 rebuilt; steps 3 and 4 marked built |
| not committed | — | This file |

## 6. Work that is not complete

| Item | Description |
|---|---|
| Upload `vote-agent2-tables` | Proxy F2 70.7; expected platform F2 approximately 66 |
| Better selection | 82 of the 136 wrong requirements in the vote cite paragraphs that the experts do not cite. A better selector is the next large gain for F2 |
| Step 1 one time | Keep the profile of the case and give it to all voters |
| One command for Sunday | Run select, full read, obligation path, both reviews, vote and citation check |
| Drawing for all steps | Give the drawing to the full read and the lenient review |
| Sub-goal | Compare old and new regulation versions; not started |
| UN R10 index error | Lines such as "12 V system" start false paragraphs in `index_pdfs.py` |

## 7. Procedures

### 7.1 Set up a computer

1. Pull the repository: `git pull`
2. Make the environment: `uv venv .venv --python 3.12`
3. Install the packages: `uv pip install --python .venv/bin/python -r requirements.txt`
4. Download the PDFs: `.venv/bin/python data/tools/fetch_regulations.py`
5. Write `.env` in the repository root, with `ANTHROPIC_API_KEY=<key>` and `TEAM_ID=team-16`.
6. Make the paragraph index: `.venv/bin/python -m src.pipeline.index_pdfs`

NOTE: The database rebuilds itself when an input is newer. Git has a copy of it.

### 7.2 Make the vote file for a case

CAUTION: STEPS 1 TO 4 USE THE HACKATHON CREDITS (APPROXIMATELY $5 FOR THE DEV CASE).

1. Run the full read without its review: `.venv/bin/python -m src.pipeline.run cases/<case> --no-review`
2. Note the regulations that it selected (`work/runs/<case>/selected.json`).
3. Run the obligation path with the review agent: `.venv/bin/python -m src.pipeline.retrieve cases/<case> --regulations <the same regulations> --build-missing`
4. Run the obligation path with the lenient review: `.venv/bin/python -m src.pipeline.retrieve cases/<case> --regulations <the same regulations> --reviewer lenient`
5. Run the obligation path without a review, to get the pool: `.venv/bin/python -m src.pipeline.retrieve cases/<case> --regulations <the same regulations> --reviewer none`
6. Vote (free):
   ```
   .venv/bin/python -m src.pipeline.vote cases/<case> --pool submissions/<case>.obligations-no-review.json \
       --voters submissions/<case>.obligations.json submissions/<case>.obligations-lenient.json \
       --paragraph-voters submissions/<case>.json --min-votes 2
   ```
7. Upload `submissions/<case>.vote.json`.

NOTE: Steps 3 to 5 run step 1 again each time, and step 1 is not deterministic. Until step 1 runs one time only, make the pool from the candidates of all runs.

### 7.3 Check the citations of a file

1. Report: `.venv/bin/python -m src.pipeline.citations submissions/<file>.json`
2. Fix version and page in the file: add `--fix`.

## 8. Important dates

- Sunday 2026-10-25, in the morning: Certivity releases the held-out case. Do `git pull`, then run `fetch_regulations.py` and `index_pdfs` again.
- For the held-out case, only the last valid upload counts. Do not upload a worse file at the end.
- Finalists pitch on Sunday from 15:00.
