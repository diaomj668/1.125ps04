#!/usr/bin/env bash
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/env.sh"
if [[ $# -eq 2 && "$1" == --package ]]; then
 RUN_DIR="$2"
 bash review/check_content.sh "$RUN_DIR" > "$RUN_DIR/review.json" || exit $?
 bash publishing/prepare_package.sh "$RUN_DIR" > "$RUN_DIR/package_result.json"
 result=$?
 bash reporting/summarize_run.sh "$RUN_DIR" > "$RUN_DIR/summary.json"
 cat "$RUN_DIR/summary.json"
 exit "$result"
fi
[[ $# -eq 0 ]] || { echo 'Usage: bash run.sh [--package runs/RUN_ID]' >&2; exit 2; }
RUN_DIR="$("$PYTHON" tools/start_run.py)" || exit $?
echo "Run: $RUN_DIR" >&2
result=0
bash data/store.sh init || result=1
bash workflows/collect_sources.sh "$RUN_DIR" || result=1
bash workflows/create_series.sh "$RUN_DIR" || result=1
status=completed; [[ $result -eq 0 ]] || status=incomplete
"$PYTHON" lib/receipt.py "$RUN_DIR" run "$status" 0 0
bash reporting/summarize_run.sh "$RUN_DIR" > "$RUN_DIR/summary.json" || result=1
cat "$RUN_DIR/summary.json"
exit "$result"
