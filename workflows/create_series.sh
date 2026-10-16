#!/usr/bin/env bash
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/../lib/env.sh"
[[ $# -eq 1 ]] || exit 2
RUN_DIR="$1"
result=0
bash editorial/select_items.sh "$RUN_DIR" < "$RUN_DIR/eligible.jsonl" > "$RUN_DIR/decisions.jsonl" || result=1
if [[ $result -eq 0 ]]; then
 bash editorial/create_briefs.sh "$RUN_DIR" < "$RUN_DIR/decisions.jsonl" > "$RUN_DIR/briefs.jsonl" || result=1
fi
if [[ $result -eq 0 ]]; then
 bash content/write_articles.sh "$RUN_DIR" < "$RUN_DIR/briefs.jsonl" > "$RUN_DIR/articles.jsonl" || result=1
 bash content/write_video_scripts.sh "$RUN_DIR" < "$RUN_DIR/briefs.jsonl" > "$RUN_DIR/video_scripts.jsonl" || result=1
fi
bash review/check_content.sh "$RUN_DIR" > "$RUN_DIR/review.json" || result=1
"$PYTHON" - "$RUN_DIR/review.json" <<'PY' || result=1
import json, sys
try:
    with open(sys.argv[1]) as stream:
        report = json.load(stream)
    if not isinstance(report, dict) or report.get('passed') is not True:
        raise ValueError('Content checks did not pass')
except (OSError, ValueError) as error:
    print(str(error), file=sys.stderr)
    sys.exit(1)
PY
status=completed; [[ $result -eq 0 ]] || status=incomplete
"$PYTHON" lib/receipt.py "$RUN_DIR" create_series "$status" 0 0
exit "$result"
