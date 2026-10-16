#!/usr/bin/env bash
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/../lib/env.sh"
[[ $# -eq 1 ]] || exit 2
RUN_DIR="$1"
mkdir -p "$RUN_DIR/candidates"
result=0
for pair in 'fetch_feeds feeds' 'fetch_youtube youtube' 'fetch_podcasts podcasts'; do
  read -r script name <<< "$pair"
  bash "collectors/$script.sh" "$RUN_DIR" > "$RUN_DIR/candidates/$name.jsonl"
  code=$?
  [[ $code -eq 0 ]] || result=1
  "$PYTHON" "$ROOT/tools/record_status.py" "$RUN_DIR" "$script" "$code"
done
# A real Unix pipe joins record streams to their extraction component.
cat "$RUN_DIR/candidates/feeds.jsonl" "$RUN_DIR/candidates/youtube.jsonl" "$RUN_DIR/candidates/podcasts.jsonl" > "$RUN_DIR/candidates.jsonl"
cat "$RUN_DIR/candidates.jsonl" | bash processing/extract_content.sh "$RUN_DIR" > "$RUN_DIR/items.jsonl" || result=1
bash data/store.sh upsert "$RUN_DIR" < "$RUN_DIR/items.jsonl" > "$RUN_DIR/changes.jsonl" || result=1
bash data/store.sh list > "$RUN_DIR/corpus.jsonl" || result=1
bash processing/filter_items.sh "$RUN_DIR" < "$RUN_DIR/corpus.jsonl" > "$RUN_DIR/eligible.jsonl" || result=1
status=completed; [[ $result -eq 0 ]] || status=incomplete
"$PYTHON" lib/receipt.py "$RUN_DIR" collect_sources "$status" 0 0
exit "$result"
