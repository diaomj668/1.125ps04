# From the Current Project to Final Submission

## Installation and Configuration

Run these commands from the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env  # Only if .env does not already exist.
```

Set `OPENAI_API_KEY` and `PIPELINE_MODEL` in local `.env`. Do not send secrets in chat, commit them, or include them in logs. The model must support Chat Completions JSON mode; components additionally validate fields, source identities, and references. Use a model available to your API account.

When a supported native timestamped transcript is unavailable, audio transcription uses `whisper-1` with ten-minute chunks and preserved timestamps. API calls incur charges. Unknown costs are recorded as `null`, not zero. Optional `PIPELINE_INPUT_USD_PER_MILLION` and `PIPELINE_OUTPUT_USD_PER_MILLION` override token-rate estimates; use the actual rates for your model.

Restricted environments must permit access to the configured sources and model API. Credentials belong in the environment, never in source code.

## First Live Run

```bash
bash run.sh
```

Each invocation creates a new `runs/RUN_ID`. Inspect the summary for failed or incomplete stages rather than treating printed output as success. Verify at least twelve distinct substantive items, six independent publishers, and two items per required input kind. Each piece needs at least three independent sources.

Valid partial results are retained after failures. Explain coverage gaps and repair blocking requirements. A passing content check with three drafts and scripts leads to `awaiting_review`; it does not grant student approval.

For same-day failure recovery, use `bash tools/resume_run.sh runs/RUN_ID`. It backs up prior outputs. Recovery regeneration is prohibited across UTC dates and for approved or packaged material; start a new run instead.

## Student Review and Policy Revision

```bash
PYTHONPATH=lib .venv/bin/python tools/prepare_human_review.py runs/RUN_ID
```

Personally inspect at least three accepted and three rejected or deferred items in `human_review.md`. Record agreement or disagreement, specific evidence, factual corrections, and reasons.

Preserve policy versions, prompts, and separate before/after outputs. Revising `config/editorial_policy.md` before the next live run is one option, but distinguish policy changes from newly collected evidence. To isolate policy effects, use a labeled replay with the same saved evidence and prompts and only a changed policy. Never overwrite the original results.

Automatic checks cannot establish semantic correctness. The student must assess reasoning, original passages, independence, and article/video consistency.

## Second Live Run on Another Day

```bash
bash run.sh
PYTHONPATH=lib .venv/bin/python tools/compare_runs.py runs/FIRST runs/SECOND > docs/run-comparison.json
```

Complete both live runs on different actual UTC dates during the assignment week. Do not alter dates to simulate a second day.

If no meaningful new material appears, report that result and additionally introduce a previously withheld, eligible real item in a clearly labeled replay. The current workflow does not generate fictional replay material. A replay of real withheld evidence, if required by the assignment, must be clearly labeled and is separate from live runs.

## Review, Packaging, and Publication

Rerun `bash review/check_content.sh runs/RUN_ID > runs/RUN_ID/review.json`. After reviewing the actual material, the student creates `approval.json` with the current `review_id`, `decision` (`approve` or `revise`), `reviewer`, `reviewed_at` in ISO 8601 UTC, and `notes`. Only the student supplies this decision. Editing reviewed inputs requires another check and approval.

```bash
bash run.sh --package runs/RUN_ID
```

Use the English scripts in the package to produce three 3–5 minute videos with Google Vids or HeyGen. Check narration, visuals, references, and disclosure of AI-generated presentation where used.

Publish three approximately 600–900 word articles on freely accessible Substack and the videos on public or unlisted YouTube. Link each article to its video; include the article and understandable timestamped source references in the video description.

Enter actual URLs in `package/publication_links.json` and `SUBMISSION.md`. Verify access while logged out. Record the separate 4–6 minute demonstration using [TECHNICAL_DEMO_OUTLINE.md](TECHNICAL_DEMO_OUTLINE.md).

## Tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -m pytest -p no:capture -q
```

The local Anaconda `readline` initialization crashed with pytest's default capture plugin, so the documented command disables that plugin. Tests do not call real models or create fictional publications presented as real work.

## Storage and Repeatability

The canonical index is `data/evidence/index.sqlite`. Only `data/store.py`, invoked through `store.sh`, directly accesses it. Retain the database, `data/assets`, and run artifacts for inspection.

Stable `item_id` values use native video identities or publisher/canonical-URL identities. A deterministic SHA-256 `version_id` covers substantive content, transcript segments, and evidence-relevant metadata; retrieval time is excluded.

Written sources are retrieved again and compared by content. Saved media transcripts are reused when their native identity, title, and publication metadata are unchanged. This may miss in-place edits under an unchanged media ID; document that limitation.

Original media is retained under `data/media` and excluded from Git by default. Records retain `url` or `media_url` for retrieval. Text and transcript evidence remains in `data/assets`. Document retrieval for any media omitted from the submitted repository.


## Current Model

The student selected `gpt-6.1-sol`, which is configured for the editorial stages. Each run pins its model and reasoning effort in `config/model.json`; exact requests and responses are saved in `model_calls`. Do not silently rewrite a previously pinned model. Start a new run when changing models.

## Comparing a Student-Edited Policy on Saved Evidence

After personally reviewing material and revising the policy, run:

```bash
PYTHONPATH=lib .venv/bin/python tools/policy_replay.py runs/SOURCE_RUN config/editorial_policy.md
```

This creates a labeled replay, retains original prompts and evidence, replaces the specified policy, reapplies the date window using the actual replay date, and calls the selection model. `comparison_context.json` states whether eligible evidence remained identical. If the date window changes the input, do not attribute every decision change to policy alone. This operation incurs API charges and does not replace another day's live collection.

## Current Topic and Draft Entry Point

**Which recent AI coding assistant capabilities and practices help individual developers complete small software projects?**

The audience has basic programming skills and independently builds small projects. Find current drafts through `docs/current_run.json` and [PROGRESS.md](PROGRESS.md). Previous generated runs were deleted at the user's request before this clean restart. The next live run reads the updated root configuration.

## Repository Language

All project-authored code, comments, configuration prose, prompts, documentation, and filenames use English. Original source passages, proper names, transcripts, and actual model responses remain exact evidence rather than silently translated records.

## Offline Duplicate-Free Replay of Retained Real Evidence

The completed demonstration is linked from [duplicate_replay.json](duplicate_replay.json). To reproduce it from the project root without network collection or model calls:

```bash
PYTHONPATH=lib .venv/bin/python tools/replay_saved_evidence.py runs/20261014T225746Z-d041cf
```

Each invocation creates a uniquely named `runs/replay-...` directory with its own isolated store, exact retained input, provenance, seed/repeat records, receipts, diagnostics, and verification. It does not modify the source run or formal evidence store and does not count as a new live run. The seed should report three new records; both repeats should report three unchanged records. Distinct items and versions remain three, while audit observations deliberately increase.

The storage owner provides this additional read-only command; required commands and responsibilities are unchanged:

```bash
bash data/store.sh stats
PIPELINE_STORE_DIR="runs/replay-20261016T040737Z-8cfe40/isolated_store" bash data/store.sh stats
```

`stats` returns item/version/observation counts, duplicate counts, and fingerprints for stored evidence records and current mappings. It opens an existing database read-only; a missing database returns failure without creating one. Other components must use this command instead of reading SQLite themselves. Changing retrieval time alone or repeating evidence must not create another version.
