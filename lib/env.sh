#!/usr/bin/env bash
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 2
export PYTHONPATH="$ROOT/lib${PYTHONPATH:+:$PYTHONPATH}"
PYTHON="${PIPELINE_PYTHON:-$ROOT/.venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then PYTHON="$(command -v python3)"; fi
# .env is parsed as data by python-dotenv when installed; never execute it as shell code.
