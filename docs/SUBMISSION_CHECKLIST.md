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

- [x] At least twelve distinct substantive items from six independent publishers.
- [x] At least two written RSS items, two YouTube items, and two podcast items; reconcile copies of the same recording.
- [x] Publication dates fall within each run's window and are recorded separately from retrieval dates.
- [x] Media was actually retrieved and timestamped transcripts identify supporting passages.
- [x] Each piece has a distinct argument, at least three independent sources, synthesis, and a meaningful limitation.
- [x] Reported facts, source claims, interpretations, and uncertainty are distinguished.
- [x] Three English articles are approximately 600–900 words excluding references; scripts support 3–5 minute videos.
- [x] All three required input types contribute evidence to the series.

## Actions That Must Actually Occur

- [x] The student personally reviews three accepted and three rejected/deferred items and records their judgment.
- [x] At least one student policy revision retains before/after versions, rerun outputs, and comparison.
- [x] Two actual live runs occur on different dates during the assignment week.
- [x] Saved records demonstrate updates, duplicate-free real-evidence replay, date filtering, and collection failure/recovery; the no-meaningful-update withheld-item condition was not triggered.
- [x] The student supplies approval.json for the current assessed material.
- [x] Produce three videos using Google Vids or HeyGen.
- [x] Publish three free-access Substack articles and three public/unlisted YouTube videos with cross-links.
- [x] Record the separate 4–6 minute technical demonstration with architecture, evidence tracing, the second run, revision, and tradeoff.
- [x] Fill SUBMISSION.md with actual links, run comparison, reflection, student identity, and repository URL.
Publisher independence, citation meaning, and applicability remain matters of human judgment. Source notes document independence and missing perspectives; the student supplied source judgments and approved the selected series. Mechanical checks do not establish semantic correctness.
- [x] Submitted text_path and segments_path values resolve; document retrieval of omitted media.

The approval applies only to the selected October 14 series; October 15 drafts remain demonstration outputs. All six publication URLs and the technical demonstration URL are in SUBMISSION.md. The student confirmed access without login. YouTube external URLs are saved in descriptions, but direct clickability still requires account verification.

Duplicate-free replay is now complete: [actual record](../runs/replay-20261016T040737Z-8cfe40/README.md). The separate technical demonstration has also been recorded and uploaded: [Google Drive](https://drive.google.com/file/d/1rdfxIpth7IE6m-BuPz-ECFLQfDhusCWy/view), duration 4 minutes 31 seconds. Playback without login was confirmed by the student.
