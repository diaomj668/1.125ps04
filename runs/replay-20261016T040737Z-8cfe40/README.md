# Real-Evidence Duplicate-Free Replay

Executed at 2026-10-16T04:07:37.726219Z. This is a labeled offline replay, not a third live run. The three records are unchanged real evidence retained by live run `20261014T225746Z-d041cf`. The historical evidence as-of date is 2026-10-14; the replay's actual execution date is recorded separately. No new source-freshness or publication claim is made.

## Actual Results

| Phase | Distinct items | Evidence versions | Audit observations | All input labels |
| --- | ---: | ---: | ---: | --- |
| seed | 3 | 3 | 3 | new |
| replay_1 | 3 | 3 | 6 | unchanged |
| replay_2 | 3 | 3 | 9 | unchanged |

The empty isolated store initially contained zero items and zero versions. Seeding created three of each. Two further ingestions of the identical JSONL input kept both counts at three and marked every record unchanged. The evidence-record and latest-mapping fingerprints stayed identical. Observations increased from three to six to nine because each ingestion is logged; these are not duplicate evidence records.

The formal store's read-only before/after diagnostics are identical, and retained text/transcript hashes are unchanged. Only `data/store.sh` and its owning Python component accessed either index. No model calls, media extraction, network collection, fictional fixtures, fabricated source dates, or publication changes were used.

## Evidence and Reproduction

- `input.jsonl`: the exact three original records, one written source, one YouTube item, and one podcast episode.
- `source_provenance.json`: original URLs, publication/retrieval dates, exact source version IDs, asset paths, and hashes.
- `seed/`, `replay_1/`, `replay_2/`: actual change records, stage receipts, count diagnostics, and stored-item snapshots.
- `commands.jsonl`: actual storage command invocations, isolated/formal store paths, timestamps, exit codes, and output paths.
- `verification.json`: assertions and measured results.
- `formal_store_before.json` and `formal_store_after.json`: read-only evidence that the formal store was untouched.

Reproduce from the project root with `PYTHONPATH=lib .venv/bin/python tools/replay_saved_evidence.py runs/20261014T225746Z-d041cf`. Each execution creates a new uniquely named replay directory and its own isolated store; it never overwrites this record or the live runs. `bash data/store.sh stats` is a read-only diagnostic extension; set `PIPELINE_STORE_DIR` to the isolated store to inspect its counts.

This demonstrates the architecture's duplicate-free replay checkpoint. It is separate from the conditional withheld-item update demonstration, which was not needed because the second live run found meaningful new material. The separate student technical demonstration video is still to be recorded.
