# PS04 Requirements Audit

Audit date: October 14, 2026, America/New_York. The evidence run is `runs/20261014T225746Z-d041cf`, with evidence as-of date `2026-10-14` UTC.

This is an audit, not student editorial approval. No live collection, paid model call, publication change, or code repair was performed during this audit. Isolated contract probes used disposable temporary directories, not submitted run evidence.

## Initial findings requiring code or document corrections

1. **The series workflow ignores a negative content assessment.** `workflows/create_series.sh:15` checks only the exit code of `check_content.sh`. The architecture explicitly requires that assessment command to exit zero when an assessment successfully completes even if `passed` is false. An isolated test returned `passed: false`, while the workflow exited zero and recorded completion. The workflow must inspect the JSON assessment and propagate blocking content errors. This does not mean the current articles failed assessment: their current assessment passes.

2. **Invalid candidate input can produce the wrong exit code.** An isolated invocation of `processing/extract_content.sh` with a JSON object missing required candidate fields returned 1. The documented contract requires 2 for malformed input. Per-item handling in `processing/extract_content.py:85` and `:129` treats validation errors as operational collection errors. Validate record shape and distinguish those cases while preserving usable partial results for genuine retrieval failures.

3. **Current status documentation is inconsistent.** `SUBMISSION.md:76` still lists producing and publishing the three videos as remaining work, although its publication table correctly contains all three actual unlisted YouTube URLs. Earlier progress paragraphs and the hardcoded `remaining_manual_actions` in `reporting/summarize_run.py:41` also list completed policy/video work as pending. Historical notes may remain if dated clearly; the current status and remaining-action list should agree.

4. **One reviewed terminology correction was not applied everywhere.** The current article body describes performance profiling and diagnostic artifacts correctly. However, claim `01-c3` in `briefs.jsonl`, and the corresponding article/script reference notes, still say "a concrete debugging use." The student's review requested "performance profiling and diagnosis." Synchronize these records, then rerun checks; any later approval must match the new fingerprint. This is a precision correction, not evidence of a demonstrated repair or speed improvement.

5. **The project is not yet submitted to the student's GitHub repository.** The current remote is `https://github.com/onexi/ps04.git`, the supplied starter. The working tree contains modified and untracked project files; HEAD remains the starter commit. Create or select the student's submission repository, commit the required code and evidence, push it, and check that graders can access it. Do not include `.env`, the virtual environment, or downloaded source media unintentionally.

## Required remaining work, apart from the second live run

| Requirement | Current evidence | Remaining action |
| --- | --- | --- |
| Three Substack articles | Three local drafts; no Substack URLs | Review and publish all three with free shareable access. Preserve the evidence as-of date and reader-usable references. |
| Article/video cross-links | Three YouTube videos exist; article links are absent | Put the matching video in each article and the matching article in each video description. |
| Accessible publication links | Unlisted status was confirmed in Studio | Test every final article/video URL while logged out. YouTube currently requires one-time account verification for clickable external description links; source URLs are present as text. |
| Final human editorial approval | Six-item review sample and policy interpretation exist | Review the final article/script/video versions and record the student's actual decision in `approval.json`, with current `review_id`, reviewer, real review time, and notes. Do not backdate approval. |
| Production package | Neither `approval.json` nor `package/` exists | After matching approval, run `bash run.sh --package runs/20261014T225746Z-d041cf`, or package the actual final run. Fill real links in `package/publication_links.json`. |
| Separate technical demonstration | A recording outline exists | Record a 4–6 minute narrated demonstration covering architecture, entry point, claim-to-evidence tracing, the second run, duplicate handling/failure recovery, a human correction or policy revision, and an architectural tradeoff. Submit its accessible URL. |
| Completed submission document | Topic, architecture, setup, records, and YouTube links are present | Fill student identity, submission repository URL, Substack links, technical-demo link, final run comparison, and reflection. Reconcile stale status prose. |
| Reflection | Placeholder plus one architectural tradeoff example | Supply the student's actual insight, editorial limitation/failure, and next improvement. |
| Final audiovisual review | Videos were produced and uploaded; review fields remain false | Watch each video fully and check captions, names, terminology, claim consistency, attribution, and legibility. Partial caption corrections are not a complete review. |

The videos were uploaded at the student's explicit request before a formal approval file existed. Record the subsequent review honestly; upload authorization is not a completed source-review or final-approval record.

## Requirements currently supported by inspected artifacts

- All 16 required Bash entry points exist. Bash coordinates the workflows; Python helpers remain in their owning components. The architecture permits this arrangement.
- The persistent evidence index is accessed by the store component; extraction queries it through `data/store.sh`.
- The current run contains 33 eligible substantive records from seven configured originating publishers: 22 written RSS items, six YouTube items, and five podcast items. Their retained text and transcript paths resolve; all 11 media records have retained media paths that resolve locally.
- All 33 eligible records have dates within September 15–October 14, 2026, inclusive. Their deterministic version hashes recompute correctly, and no identical `underlying_id` values were found. This is not proof that differently transcribed copies can never be duplicates; human reconciliation remains necessary.
- The series actually cites 11 distinct items from five publishers. Pieces 01, 02, and 03 use three, four, and four publishers, respectively. RSS contributes across the series; YouTube contributes to piece 02 and podcast audio to piece 03. The assignment's 12-item/six-source minimum applies to collection, not a requirement to force every collected item into publication.
- Current article word counts, excluding references, are 854, 859, and 847. Pipeline script narration counts are 468, 496, and 520. The later production edit removes only the spoken opening AI-disclosure sentence; separate current production narration and edit records preserve that change.
- The three pieces address changes, scrutiny of claims, and qualified practical implications, respectively. Their arguments, synthesis, evidence locators, and limitations are present. Mechanical checks cannot certify the quality of those interpretations.
- The student review contains three accepted and three rejected/deferred initial decisions, passages, and reasons. The policy revision retains before/after policy, a real selection rerun, comparison, and the student's interpretation. It does not replace the second live run.
- Actual failure/recovery records exist. Two candidates remained inaccessible; incomplete coverage is reported instead of treating them as successful sources. The assignment allows explicitly reported partial failure/recovery.
- Three current videos were produced through Google Vids and uploaded to YouTube as unlisted: `pDt5vDDNF7E`, `8lIFBSltIm0`, and `xV7t_A6FAcw`. YouTube displayed durations of 3:48, 4:04, and 4:04, within the required range. Sources and AI-narration disclosure are in the descriptions.
- The eight existing local tests passed during this audit. Reassessment of the current run passed and matched saved review fingerprint `901b45b898144a602dfc0efd24c9ca7f7b403096a4cb188eafb708d0481f752c`.
- No exact configured API credential value was found in the scanned project code, documentation, configuration, retained source text, or run text/JSON artifacts. This is a targeted scan, not a general security certification.
- `README.md` and `ARCHITECTURE.md` are unchanged in the Git working tree.

## Conditional requirement after tomorrow's run

The second real run alone is not the entire repeatability demonstration. Compare actual source versions and editorial outputs; explain meaningful changes, unchanged inputs, duplicates, filtering, and failures. Both live runs must occur during the assignment week on different actual UTC dates.

If no meaningful new material appears, the README requires an additional clearly labeled replay introducing a previously withheld eligible real item. It does not require inventing evidence, a fake date, or a simulated second live run. A replay without duplicate evidence must also be demonstrated; an unchanged-material ingestion can serve this purpose and must be recorded clearly.

## Limitations and cost reporting

Independent controlled research and representative beginner/accessibility/failure perspectives remain weak. These limitations are already acknowledged; a vendor benchmark is not independent effectiveness confirmation. Additional source quantity alone would not resolve that weakness.

The recorded main-run model estimate is $1.9788. The separately retained policy-selection comparison estimates another $1.5116, for approximately $3.4904 in those known model estimates combined. Transcription, narration, and certain failed calls have unknown invoice costs. Keep these scopes separate and avoid presenting the main-run estimate as the total project bill. Video production records and policy-comparison records should remain easy for graders to find.

This audit inspected local artifacts and the actual saved upload records. It did not rewatch all three complete videos, verify every original source against its live website, or complete logged-out publication-access tests. Final approval and those access checks remain real tasks.

## Follow-up Corrections Completed

The four requested contract/document corrections above were subsequently repaired. The series workflow propagates failed assessments; invalid candidate input returns exit 2 before any retrieval; current profiling terminology is synchronized; and the submission, progress report, and generated summary now acknowledge the completed YouTube uploads and policy work. Historical findings and snapshots are retained as records of the audit.

All 21 local regression cases passed, including false/malformed assessments, invalid input, retained partial operational output, and handoff status derived from confirmed uploads. Current article/script checks passed after the terminology edit. See [repair record](../runs/20261014T225746Z-d041cf/edits/contract-and-status-fixes/README.md) for the current review ID and preserved prior artifacts. No new collection or paid model call was made. The other submission requirements in this audit remain pending.
