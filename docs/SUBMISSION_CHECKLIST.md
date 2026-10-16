# PS04 Final Submission Checklist

This checklist is not a completion declaration. Assess the actual artifacts and records.

## Implementation and Interfaces

- [x] All sixteen required Bash files are implemented with separated responsibilities.
- [x] Bash coordinates the pipeline and a real Unix pipe passes records; helpers remain within their owning components.
- [x] Only the store component accesses SQLite; init/upsert/list/get, version history, and observations are implemented.
- [x] The UTC date window is D minus 29 days through D, with recorded exclusion reasons.
- [x] Runs retain configuration, prompts, candidates, evidence, decisions, drafts, logs, and model responses.
- [x] An actual gpt-6.1-sol JSON call passed; secrets are absent from public configuration.
- [x] Packaging checks current review_id and student approval; changed inputs invalidate old approval.
- [x] All 25 current regression cases passed. Test fixtures are not assignment evidence; no fictional replay is included in the clean run.

## Real Evidence and Content: Verify Against the Final Run

- [ ] At least twelve distinct substantive items from six independent publishers.
- [ ] At least two written RSS items, two YouTube items, and two podcast items; reconcile copies of the same recording.
- [ ] Publication dates fall within each run's window and are recorded separately from retrieval dates.
- [ ] Media was actually retrieved and timestamped transcripts identify supporting passages.
- [ ] Each piece has a distinct argument, at least three independent sources, synthesis, and a meaningful limitation.
- [ ] Reported facts, source claims, interpretations, and uncertainty are distinguished.
- [ ] Three English articles are approximately 600–900 words excluding references; scripts support 3–5 minute videos.
- [ ] All three required input types contribute evidence to the series.

## Actions That Must Actually Occur

- [x] The student personally reviews three accepted and three rejected/deferred items and records their judgment.
- [x] At least one student policy revision retains before/after versions, rerun outputs, and comparison.
- [x] Two actual live runs occur on different dates during the assignment week.
- [x] Saved records demonstrate updates, duplicate-free real-evidence replay, date filtering, and collection failure/recovery; the no-meaningful-update withheld-item condition was not triggered.
- [x] The student supplies approval.json for the current assessed material.
- [x] Produce three videos using Google Vids or HeyGen.
- [ ] Publish three free-access Substack articles and three public/unlisted YouTube videos with cross-links.
- [ ] Record the separate 4–6 minute technical demonstration with architecture, evidence tracing, the second run, revision, and tradeoff.
- [ ] Fill SUBMISSION.md with actual links, run comparison, reflection, student identity, and repository URL.
- [ ] Personally verify publisher independence, citation meaning, missing perspectives, and applicability to individual developers.
- [ ] Submitted text_path and segments_path values resolve; document retrieval of omitted media.

The checked approval applies only to the selected October 14 series. Its package exists and contains the actual YouTube links; October 15 drafts remain demonstration outputs. Unchecked publication/access/demo/replay tasks are not implied complete by student approval.

Duplicate-free replay is now complete: [actual record](../runs/replay-20261016T040737Z-8cfe40/README.md). This checkbox refers to saved execution evidence, not completion of the still-unrecorded student technical video.
