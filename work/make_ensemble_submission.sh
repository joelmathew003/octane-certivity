#!/usr/bin/env bash
# Majority of N independent runs of make_clean_submission.sh for one case.
#
# Usage:
#   work/make_ensemble_submission.sh cases/heldout-front-bumper        # 9 runs
#   work/make_ensemble_submission.sh cases/heldout-front-bumper 5
#
# The model calls differ from run to run, so each run writes a few requirements the others do not. Those one-offs
# are mostly wrong (dev, 3 runs: written by 1 run ≈10% match, by all 3 ≈46%), so the majority keeps recall and drops
# them (held-out: 1 run F2 74.9, majority of 5 76.2, majority of 9 77.1). A run that leaves out a regulation at
# selection is outvoted. Each run gets its own copy of the case (spec and drawings, never expected.json) so the runs
# write separate files and go in parallel. About $7 and 8 minutes per run; the runs overlap.
# -> submissions/<case_id>.<YYYYMMDD-HHMM>.ensemble<N>.json
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/bin/python
CASE=${1:?usage: work/make_ensemble_submission.sh cases/<case> [runs]}
N=${2:-9}
CASE_ID=$(basename "$CASE")

$PY -m src.pipeline.index_pdfs > "work/runs/${CASE_ID}-index.log" 2>&1
# a copy of the script without the index step (done once above), so the parallel runs never rebuild it together
grep -v 'src.pipeline.index_pdfs' work/make_clean_submission.sh > work/.run_member.sh

pids=()
for i in $(seq 1 "$N"); do
    member="data/${CASE}-run$i"
    mkdir -p "$member"
    find "data/$CASE" -maxdepth 1 -type f ! -name expected.json -exec cp {} "$member/" \;
    bash work/.run_member.sh "${CASE}-run$i" > "work/runs/${CASE_ID}-run$i.log" 2>&1 &
    pids+=($!)
done
for pid in "${pids[@]}"; do wait "$pid" || echo "a run failed (see work/runs/${CASE_ID}-run*.log); it is left out"; done
echo "[$SECONDS s] $N runs done"

runs=()
for i in $(seq 1 "$N"); do
    final=$(ls -t submissions/"${CASE_ID}-run$i".2*.final.json 2>/dev/null | head -1 || true)
    [ -n "$final" ] && runs+=("$final")
done
$PY -m src.pipeline.ensemble "$CASE" --runs "${runs[@]}" --min-runs $(( ${#runs[@]} / 2 + 1 )) --name "ensemble$N" \
    > "work/runs/${CASE_ID}-ensemble.log" 2>&1
OUT="submissions/${CASE_ID}.$(date +%Y%m%d-%H%M).ensemble$N.json"
cp "submissions/${CASE_ID}.ensemble$N.json" "$OUT"
echo "[$SECONDS s] DONE -> $OUT (majority of ${#runs[@]} runs; upload this)"
