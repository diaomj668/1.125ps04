#!/usr/bin/env bash
# Same-day recovery only; preserves previous artifacts before retrying.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/../lib/env.sh"
[[ $# -eq 1 ]] || exit 2
RUN_DIR="$1"
"$PYTHON" tools/backup_attempt.py "$RUN_DIR" || exit $?
result=0
bash workflows/collect_sources.sh "$RUN_DIR" || result=1
bash workflows/create_series.sh "$RUN_DIR" || result=1
status=completed; [[ $result -eq 0 ]] || status=incomplete
"$PYTHON" lib/receipt.py "$RUN_DIR" run "$status" 0 0
bash reporting/summarize_run.sh "$RUN_DIR" > "$RUN_DIR/summary.json"
cat "$RUN_DIR/summary.json"
exit "$result"
