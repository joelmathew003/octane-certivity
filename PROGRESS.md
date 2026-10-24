# Progress report: Octane × Certivity

Date: 2026-10-24 (Saturday)

Status: The pipeline operates from start to end on the dev case. The first live run gave a page-level F1 of 0.909.

## 1. Scope

This file tells the team which work is complete and which work is not complete.
It also gives the procedures to set up the pipeline and to run it.

## 2. Summary

- The pipeline reads a product specification. It writes the requirements that apply to the product under UN Regulations.
- The pipeline uses the Claude API for two tasks only: to select the regulations and to write the requirements.
- All other steps do not use a large language model (LLM). They are deterministic and free.
- The first live run on `dev-rear-lamp` cost $2.51.

## 3. Repository layout

| Path | Contents | In git |
|---|---|---|
| `data/` | Certivity kit: cases, schemas, tools, `regulations/index.json` | Yes |
| `data/regulations/pdf/` | Regulation PDFs | No |
| `data/subgoal/dev/*.pdf` | Old and new PDF for the sub-goal | No |
| `src/pipeline/` | Our code | Yes |
| `work/index/` | Paragraph index, one JSONL file for each regulation | No |
| `work/regulations.db` | SQLite database | Yes |
| `work/runs/` | LLM answers for each run | No |
| `submissions/` | Submission files | No |
| `.env` | API key and team ID (secret) | No |
| `architecture.excalidraw` | Design diagram | Yes |

## 4. Work that is complete

### 4.1 Regulation data

- We downloaded all 94 PDFs: 56 base versions, 36 latest versions and 2 sub-goal PDFs.
- The SHA-256 values of all PDFs are correct.

### 4.2 Paragraph index (`src/pipeline/index_pdfs.py`)

1. The script reads each PDF with PyMuPDF. It does not use an LLM.
2. The script removes the page headers.
3. The script starts a new paragraph at each paragraph number, annex heading and part heading.
4. The script writes one JSON line for each paragraph: label, start page, end page and text.

- Annex labels have the same format as the expected files, for example `Annex 6 Part 4 1`.
- The index has 28,185 paragraphs for the 56 base versions.
- Verification: All 190 citations in `data/cases/dev-rear-lamp/expected.json` go to the correct paragraph and page.

NOTE: The latest versions are not in the index.

### 4.3 Regulation database (`src/pipeline/db.py`)

- The database is `work/regulations.db` (approximately 20 MB). Git has a copy of it.
- The build does not use an LLM. It takes less than 1 second.
- The build always starts from zero and reads only files. Thus, you can delete the database and make it again.
- The build also reads the output of the obligation builder (`work/obligations/*.jsonl`). Thus, a new build does not delete paid LLM output.

| Table | Rows | Contents |
|---|---|---|
| `regulations` | 56 | Name and title |
| `versions` | 92 | Version label of the base and latest versions |
| `paragraphs` | 28,185 | Label, scorer key, section, section title, pages, text, "shall/must" flag |
| `paragraphs_fts` | 28,185 | Full-text index of the paragraphs (SQLite FTS5) |
| `expected` | 190 | Expected requirements of each case, with the paragraph that they cite |
| `obligations`, `obligation_tags` | 0 | Output of the obligation builder (not complete) |

- The functions `get_paragraph()` and `search()` are ready for the review agent.

### 4.4 Pipeline (`src/pipeline/run.py`, `src/pipeline/llm.py`)

1. Claude reads the regulation catalogue and the specification. Claude selects the applicable regulations.
2. Claude reads each selected regulation in full. These calls run in parallel.
3. Claude writes one requirement for each obligation.
4. The code sets the page of each citation from the paragraph index.
5. The code writes `submissions/<case>.json`.
6. The code runs `validate.py`. If the case has an `expected.json` file, the code also runs `score_local.py`.

- `llm.py` uses the model `claude-opus-5-5` with structured JSON output.
- `llm.py` reads the API key from `.env` in the repository root.

### 4.5 First live run (dev-rear-lamp)

- Claude selected 4 regulations: UN R148, UN R150, UN R48 and UN R10. The expected file uses the same 4 regulations.
- The run wrote 182 requirements. The expected file has 190 requirements.
- The submission file is valid.

| Level | Precision | Recall | F1 |
|---|---|---|---|
| Regulation | 1.000 | 1.000 | 1.000 |
| Page | 0.877 | 0.943 | 0.909 |
| Paragraph (our calculation) | 0.653 (94/144) | 0.790 (94/119) | 0.715 |

- Only the platform calculates the requirement-level score.
- Cost: $2.51. Cache writes caused $1.82 of this cost. Each regulation is read one time only, so the cache gives no benefit.

### 4.6 Findings from the expected answers

1. The experts cite a small number of sections in each regulation. Examples: UN R48 sections 5 and 6, UN R148 sections 3 to 5.
2. The experts almost never cite these sections: definitions, application for approval, approval, conformity of production, transitional provisions and penalties.
3. 19 cited paragraphs do not contain "shall" or "must". Thus, a filter on "shall" alone decreases recall.
4. Examples of item 3: "may ... provided" paragraphs, and sub-items such as "In height: ..." below a parent paragraph that contains "shall".
5. Most extra paragraphs in our run are near the correct paragraph. Example: We cited UN R48 5.5.1 to 5.5.3, but the experts cite 5.5.5.
6. The paragraph index has an error in UN R10. Lines such as "12 V system" and "75 MHz" start false paragraphs. This error has no effect on the dev case.

### 4.7 Diagram

- `architecture.excalidraw` shows the status of each box.
- A green outline shows that the work is complete.
- A red dotted outline shows that the work is not complete.

## 5. Work that is not complete

| Item | Description | Uses Claude |
|---|---|---|
| Obligation builder | Split each "shall" paragraph into single obligations. Add tags: applies_to, kind, vehicle category. Write the output to `work/obligations/*.jsonl`. | Yes (approximately $15 to $25 for 56 regulations) |
| Product profile (step 1) | Step 1 selects the regulations but does not write the product profile. Step 2 needs the profile. | Yes |
| SQL filter (step 2) | Select the obligations with SQL. Do not use top-k similarity search. | No |
| Review agent (step 3) | Claude with the tools `get_paragraph`, `search_db` and `check_citation`. | Yes |
| Citation check (step 4) | Make sure that each number in a requirement is in the cited paragraph. Reject paragraph labels that are not in the index. | No |
| Upload | Set `TEAM_ID` in `.env`. Upload the submission to the platform. | No |
| Sub-goal tool | Index the old and new PDFs. Align the paragraphs by number. Find the differences. Find the requirements in `requirements_old.json` that cite a changed paragraph. Claude writes only `new_text` and `reason`. | Yes (small) |
| Cache markers | Remove the cache markers in `run.py`. This decreases the cost by approximately $0.35 for each run. | No |
| UN R10 index error | Correct the paragraph pattern in `index_pdfs.py` (refer to 4.6, item 6). | No |

## 6. Procedures

### 6.1 Set up a new computer

CAUTION: DO NOT PUT THE PDFS, `.env` OR `work/index/` IN GIT. THE DATA LICENCE AND THE API KEY DO NOT PERMIT THIS.

1. Pull the latest version of the repository: `git pull`
2. Make the Python environment: `uv venv .venv --python 3.12`
3. Install the packages: `uv pip install --python .venv/bin/python -r requirements.txt`
4. Download the PDFs: `.venv/bin/python data/tools/fetch_regulations.py`
5. Make sure that the PDFs are in `data/regulations/pdf/` and `data/subgoal/dev/`.
6. Make the file `.env` in the repository root. Write these two lines in it:
   ```
   ANTHROPIC_API_KEY=<key>
   TEAM_ID=<team id>
   ```
7. Set the file permissions: `chmod 600 .env`
8. Make the paragraph index: `.venv/bin/python -m src.pipeline.index_pdfs`

NOTE: Step 9 is necessary only if `db.py` or the index changed. Git has a copy of the database.

9. Make the database: `.venv/bin/python -m src.pipeline.db`

### 6.2 Run the pipeline on a case

NOTE: Each run costs approximately $2.50 from the hackathon credits.

1. Run the pipeline: `.venv/bin/python -m src.pipeline.run cases/dev-rear-lamp`
2. Examine the output files:
   - `submissions/<case>.json`: the submission file.
   - `work/runs/<case>/selected.json`: the regulations that Claude selected, with the reasons.
   - `work/runs/<case>/extract_<regulation>.json`: the requirements for each regulation.
3. To skip step 1 and use a fixed set of regulations, add `--regulations "UN R48" "UN R148"` to the command.

### 6.3 Query the database

1. To search the paragraph text: `.venv/bin/python -m src.pipeline.db search "rear fog lamp" --regulation "UN R48"`
2. To open an SQL shell: `.venv/bin/python -m sqlite3 work/regulations.db`

NOTE: You can also open `work/regulations.db` with the VS Code extension "SQLite Viewer" or with DBeaver.

NOTE: In the table `paragraphs_fts`, the columns `paragraphs_fts` and `rank` are internal columns. They do not contain data.

3. After a new build, open the database again. The build replaces the file.

### 6.4 Update the database in git

1. Make the database again: `.venv/bin/python -m src.pipeline.db`
2. Commit `work/regulations.db`.

CAUTION: THIS IS A SHARED REPOSITORY. TELL THE TEAM BEFORE YOU PUSH TO `main`.

## 7. Important dates

- Sunday 2026-10-25, in the morning: Certivity releases the held-out case.
- When Certivity releases the case, do `git pull`. Then run `fetch_regulations.py` again.
- The platform accepts 5 uploads in each hour. For the held-out case, only the last valid upload counts.

## 8. Git history

| Commit | Author | Change |
|---|---|---|
| `49ff859` | ishwargov | Pipeline: index, regulation catalogue, LLM wrapper, run script |
| `eb0d10e` | Joel Mathew | New layout: `data/` and `src/` |
| `e13b744` | ishwargov | Database module and design diagram |
| `dc46da8` | ishwargov | `work/regulations.db` in git |
| `42226eb` | ishwargov | Diagram: status colours (green = complete, red dotted = not complete) and fonts |
