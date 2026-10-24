# Context for AI assistants (Octane × Certivity hackathon)

Read `PROGRESS.md` first: it has the pipeline, every score, the change log and the procedures.

## Task
Product spec + drawing → every engineering requirement it must fulfil under UN Regulations (regulation + base
version + page + paragraph). Scored per level; the **leaderboard ranks by requirement-level F2** (recall counts
more than precision). Held-out case: released Sunday morning; only the **last** valid upload counts.

## Rules of this repo
- Run everything from the repo root with `.venv/bin/python -m src.pipeline.<module>`.
- Prompts live in `src/pipeline/prompts/*.md`, never inline in Python. Do not put examples from the dev answer
  keys (`data/cases/*/expected.json`, `data/subgoal/*/expected.json`) into prompts.
- Editing `obligation.*.md`, `vocabulary.*.md` or `regulation.md` makes the obligation builder pay again.
- Do not edit `architecture.excalidraw` unless asked (the user tuned its fonts).
- Shared repo: ask before committing or pushing. Keep PDFs, `.env` and `work/index/` out of git.
- `.env` holds `ANTHROPIC_API_KEY` (hackathon credits) and `TEAM_ID=team-16`.

## Best method so far (dev: platform F2 72.2, F1 63.1, Page F1 87.2)
4-voter probability score (`threshold=0.60`): review agent (`retrieve.py`), lenient review (`retrieve.py --reviewer lenient`), full read without review (`run.py --no-review`), and paragraph judge (`paragraph_judge.py`); then `vote.py --facts --threshold 0.60` (facts filter, table step, citation check). The whole chain for any case: `work/make_clean_submission.sh` (`submissions/<case>.vote.json`).
For a new case: build missing obligations with `retrieve.py --build-missing`.
Sub-challenge (`subgoal.py`): `.venv/bin/python -m src.pipeline.subgoal data/subgoal/<case> --team-id team-16` (dev: flag recall 83.3 / precision 90.9 / accuracy 89.5 in `submissions/subgoal-dev.json`).
