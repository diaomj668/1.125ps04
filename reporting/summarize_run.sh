#!/usr/bin/env bash
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/../lib/env.sh"
exec "$PYTHON" "$ROOT/reporting/summarize_run.py" "$@"
