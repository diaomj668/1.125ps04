# Technical Demonstration Outline: 4–6 Minutes

The required live runs, chosen-series approval, and real-evidence duplicate replay are retained. Recording is still pending. Seven read-only evidence views are available through `tools/show_demo.py`; they do not start another pipeline run.

- **0:00–0:40:** Introduce the audience and central question. Show the architecture diagram in SUBMISSION.md.
- **0:40–1:20:** Show `bash run.sh`, the actual date in run.json, configuration/prompt snapshots, and logs.
- **1:20–2:30:** Trace one published claim from article to brief, decision, item/version, and exact original passage or timestamped transcript segment. Make files readable and open the source.
- **2:30–3:30:** Show the second-day live run and compare new, changed, and unchanged evidence and editorial decisions. If there was no meaningful new material, state that honestly and separately show a clearly labeled withheld-item replay.
- **3:30–4:15:** Demonstrate duplicate handling, date exclusion, and a real collection failure or recovery. Explicitly identify simulated failures.
- **4:15–5:15:** Personally explain at least one policy revision or factual correction and show its before/after evidence.
- **5:15–5:45:** Explain a concrete architectural tradeoff, such as SQLite ownership or media caching/change detection, and show actual publication links.

This is a recording outline, not an assertion that the demonstration is complete or a substitute for the student's own explanation. Do not narrate unfinished steps as completed work.

## Ready-to-Show Duplicate Replay Evidence

Open [the actual replay](../runs/replay-20261016T040737Z-8cfe40/README.md) for the 3:30–4:15 section. Show `seed/changes.jsonl` (three new), `replay_1/changes.jsonl` and `replay_2/changes.jsonl` (three unchanged each), and `verification.json`. Item/version counts remain 3/3; observation counts rise 3/6/9 because processing observations are audit logs. Then show the equal formal-store fingerprints. Explain that the source records are genuine saved material, replay uses an isolated store, and this offline demonstration is not another day's live collection. No fictional fixture, paid model call, or simulated failure is involved.
