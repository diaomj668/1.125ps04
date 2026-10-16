# PS04 Progress

Current actual run: [20261014T225746Z-d041cf](../runs/20261014T225746Z-d041cf/run.json). As-of: **2026-10-14 UTC**. Status: **awaiting student review**.

Previous generated runs, drafts, evidence index, media caches, and fictional replay outputs were deleted at the user's request. Implementation, configuration, credentials, dependencies, and instructor originals were retained. Only one actual run directory exists after the restart.

## Generated Drafts

| Piece | Article | Article words | Video script | Narration words |
| --- | --- | ---: | --- | ---: |
| 01 | [New ways to supervise, inspect, and constrain coding agents](../runs/20261014T225746Z-d041cf/articles/01.md) | 854 | [Script 01](../runs/20261014T225746Z-d041cf/video_scripts/01.md) | 468 |
| 02 | [A successful signal is not necessarily successful software](../runs/20261014T225746Z-d041cf/articles/02.md) | 859 | [Script 02](../runs/20261014T225746Z-d041cf/video_scripts/02.md) | 496 |
| 03 | [Make the next agent task bounded, inspectable, and affordable](../runs/20261014T225746Z-d041cf/articles/03.md) | 847 | [Script 03](../runs/20261014T225746Z-d041cf/video_scripts/03.md) | 520 |

Article counts exclude references. Narration counts exclude visual directions and nonspoken evidence annotations. At 130 spoken words per minute, the scripts estimate 3.6–4.0 minutes; verify the actual rendered video duration. All three videos have since been produced in Google Vids and uploaded to YouTube as Unlisted; observed YouTube durations are 3:48, 4:04, and 4:04. Caption and full audiovisual review remain pending.

## Actual Evidence and Checks

- Discovered: 42 candidates. Extracted: 40 substantive items. Seven were outside the date window.
- Date-eligible: 33 distinct items from seven publishers: 22 written RSS items, six YouTube videos, and five podcasts.
- Revised AI decisions: 22 accepted, three rejected, eight deferred; initial decisions are preserved. The series uses substantive evidence from all three input kinds.
- Three different arguments, at least three publishers per piece, references, exact source passages, timestamp locators, claim markers, and dates passed mechanical checks.
- All three articles meet 600–900 words; all scripts meet 390–650 narration words. Eight local implementation tests passed.
- Independent controlled research and representative novice, unsuccessful-project, budget-constrained, and accessibility-user perspectives remain limited or missing. Mechanical checks do not establish semantic support or independence.

## Actual Failure and Recovery

The first attempt encountered exhausted API credit and YouTube Atom HTTP 404 errors. The user restored API credit. Direct channel discovery recovered video metadata; the same run was resumed with prior outputs preserved under attempts/. This is one live run with real recovery, not a second-day run or fictional replay.

Two sources remained unavailable: one written candidate lacked substantive text, and one video returned HTTP 403. Their errors remain recorded. Consequently the shell exit status remains nonzero for partial collection, while the content assessment passes and the summary reports awaiting_review. No unavailable source was used as evidence.

The first script-length check incorrectly counted nonspoken evidence annotations. The metric parser was fixed, tests passed, and the assessment was rerun. Generated prose was unchanged. The original assessment is retained under edits/metrics-correction/.

See [summary](../runs/20261014T225746Z-d041cf/summary.json), [review](../runs/20261014T225746Z-d041cf/review.json), [recovery](../runs/20261014T225746Z-d041cf/recovery_status.json), and [student review worksheet](../runs/20261014T225746Z-d041cf/human_review.md).

Known or estimated model cost: **$1.9788**, plus unpriced transcription and failed-call stages. This is not a total invoice. Run receipts retain exact usage and durations. Wall time includes the initial failure, waiting for credit restoration, and recovery.

Store change counts include observations from the first failed attempt and same-day retry. They do not demonstrate a second day.

## Tomorrow's Real Run

Preserve this run, the evidence index, and retained assets. From the repository root run:

```bash
bash run.sh
PYTHONPATH=lib .venv/bin/python tools/compare_runs.py runs/20261014T225746Z-d041cf runs/SECOND_RUN_ID > docs/run-comparison.json
```

Replace SECOND_RUN_ID with tomorrow's actual run ID. Do not invent a date or create fictional replay data. Both runs must occur during the assignment week.

## Remaining Submission Work

The six-item student source-review sample and actual policy selection rerun are recorded below. The student completed the comparison interpretation. The revised articles and scripts now require final student review and approval. Three matching videos are produced and uploaded to YouTube as Unlisted. Publish the three Substack articles, add cross-links, verify logged-out access, record the separate technical demonstration, and complete SUBMISSION.md. Final editorial approval remains pending.

## Student Policy Revision Update

The student supplied judgments for three accepted and three rejected/deferred sources. The access/setup/relevance policy clarification was implemented, with before/after versions and a real selection rerun on identical saved evidence. [Actual comparison](../runs/20261014T225746Z-d041cf/policy_revision/comparison.md) records four changed decisions and model-variation limits. Initial articles and scripts are preserved in editorial_revision/before/. The student completed the comparison interpretation and authorized focused edits. Current drafts incorporate the approved narrow Cursor use; final draft approval, Substack publication, and the second live collection remain pending.

## Current Revised Drafts

The six linked drafts above are the current revisions. See [revision record](../runs/20261014T225746Z-d041cf/editorial_revision/README.md), [full diff](../runs/20261014T225746Z-d041cf/editorial_revision/draft_changes.diff), and [current content assessment](../runs/20261014T225746Z-d041cf/review.json). Exact source passages, claim manifests, and canonical references were updated together. No further paid pipeline generation or collection was performed.

The evidence as-of date remains 2026-10-14, when the evidence was actually collected. Later human-review and editorial-edit times are recorded separately. The current summary wall time includes those pauses and revisions; it is not uninterrupted machine processing time.

## Current-Version Video Production Request

The student requested drafting videos from the current three articles and scripts. [Production inputs](../runs/20261014T225746Z-d041cf/video_production/README.md) retain frozen article/script snapshots, clean narration, scene plans, and HeyGen instructions. Estimated durations at 125 words per minute are 221.8, 235.2, and 246.7 seconds; these are not rendered measurements.

HeyGen is installed and connected. The user subsequently declined all digital presenters. Three HeyGen Video Agent jobs were submitted with narration, diagrams, and subtitles, but all subsequently failed with free_tier_quota_exceeded. Real session links, video IDs, and actual failure records are saved in video_production/. Those HeyGen attempts produced no completed video. Google Vids outputs and subsequent YouTube uploads are recorded below. Final editorial approval remains pending.

### HeyGen Generation Jobs

- Piece 01: [generation session](https://app.heygen.com/video-agent/0d447429a4194245a438cdd25cced156); video ID `39d7c1bf26564b14af5a167758364a44`; confirmed failed: free_tier_quota_exceeded.
- Piece 02: [generation session](https://app.heygen.com/video-agent/c24dbb37dc3f4995a7cf24c65b915503); video ID `b84dc80722bd4f9295de0473b01d48d5`; confirmed failed: free_tier_quota_exceeded.
- Piece 03: [generation session](https://app.heygen.com/video-agent/942bde9e8d1242eeb02ba40b90c84806); video ID `d18dc39f1e4043bb940addac6ccdfe6b`; confirmed failed: free_tier_quota_exceeded.

The user-requested status check confirmed terminal quota failures for all three HeyGen attempts. No HeyGen retries were submitted; the student chose Google Vids next.

### Switch to Google Vids

Initial Google Vids production: three draft MP4s were exported to Drive before the later opening edits and YouTube uploads recorded below. [Video outputs and actual production method](../runs/20261014T225746Z-d041cf/video_production/google_vids/README.md) link all three editors and exports. Complete source durations are 231.25, 246.89, and 246.91 seconds, confirmed by the Vids timelines; the second Drive export was observed playing at 4:07. Local narration/text-card media were imported, captioned, and exported in Google Vids. Automatic captions and full audiovisual quality still require student review. These initial exports predate the YouTube uploads recorded below; final editorial approval remains pending.

### Video Opening Revision

At the student request, all three Google Vids videos were trimmed to remove the opening spoken AI disclosure sentence. On-screen disclosure is retained. Revised durations observed in Vids are 227.5, 243.2, and 243.3 seconds; all three revised MP4 exports were confirmed completed. [Current links and edit record](../runs/20261014T225746Z-d041cf/video_production/google_vids/README.md) replace prior export links. This is a video edit, not a new source-collection run or final student approval.

## YouTube Upload Completed

At the student request, all three current Google Vids revisions were exported directly to YouTube, given English titles, evidence-source descriptions and AI-narration disclosure, marked not made for kids, and saved as Unlisted. The channel content list confirmed all three visibility states.

- Piece 01: [YouTube](https://youtu.be/pDt5vDDNF7E); observed player duration 3:48.
- Piece 02: [YouTube](https://youtu.be/8lIFBSltIm0); observed player duration 4:04.
- Piece 03: [YouTube](https://youtu.be/xV7t_A6FAcw); observed player duration 4:04.

[Publication records](../runs/20261014T225746Z-d041cf/video_production/youtube/publication.json) retain actual IDs and metadata. Substack article links and logged-out access checks remain pending. YouTube requires one-time account verification to make external description links clickable; source URLs are present as text. This upload authorization does not fabricate an editorial approval file or replace the second live pipeline run.

## Contract and Status Corrections

At 2026-10-15T03:24:19.739263Z, the workflow assessment propagation and extraction invalid-input exit code were repaired. Current profiling terminology is synchronized across the brief and article/script reference notes. Historical production snapshots are retained; current supplementary reference notes are in `video_production/01/references-current.md`. The summary now reads confirmed YouTube uploads and saved review/policy records instead of repeating completed work as pending. The expanded local suite passed all 21 cases; the eight-test count above describes the earlier audit. Current content checks passed with review_id `34ec8312b655940e49d36d259a69994a5dbf3e72fe37ff87da690221a6c44cc1`. No new collection, model calls, or final student approval occurred. [Repair record](../runs/20261014T225746Z-d041cf/edits/contract-and-status-fixes/README.md).
