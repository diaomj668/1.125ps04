# Comparison of Two Actual Live Runs

- First execution evidence date: 2026-10-14 UTC.
- Second execution evidence date: 2026-10-15 UTC.
- Both saved run records declare live mode and different actual execution dates.
- This comparison reads saved artifacts; it performs no collection or model calls.

## Collection and Change Observations

The second extraction retained 41 of 42 candidates. One written candidate could not yield substantive text; its failure remains in the extraction receipt. The eligible corpus contains 38 distinct items from seven publishers: 25 written, eight YouTube, and five podcast items.

Comparing successful per-run extraction records yields 5 newly observed items, 6 changed version IDs, and 30 identical version IDs. Newly observed does not necessarily mean newly published; a formerly inaccessible recording can be newly retained. Changed version IDs require passage-level inspection before claiming a substantive development.

### Newly Retained Items

- feed: [Tree Appreciator](https://simonwillison.net/2026/Oct/14/tree-appreciator/), published 2026-10-14T21:23:01Z.
- feed: [The next developer interface is ambient intelligence](https://github.blog/news-insights/company-news/the-next-developer-interface-is-ambient-intelligence/), published 2026-10-15T19:39:27Z.
- feed: [Anthropic tells investors quarterly revenue up nearly 50% to $16.8bn ahead of IPO](https://simonwillison.net/2026/Oct/15/anthropic-tells-investors/), published 2026-10-15T13:04:03Z.
- youtube: [A $6.3 billion open-weight model just got embarrassed by the French...](https://www.youtube.com/watch?v=WrCjAAl9okA), published 2026-10-07T20:24:27+00:00.
- youtube: [The runtime wars are over... and Node won](https://www.youtube.com/watch?v=l3L_lETiSzc), published 2026-10-15T17:35:15+00:00.

## Editorial Outcome, Repair, and Limitations

The initial October 15 execution generated all three articles and scripts but failed the saved assessment: no YouTube evidence reached the briefs. Selection alone was insufficient. This failure was correctly propagated by the workflow and remains in the original receipts and `editorial_revision/before/review.json`.

The initial warnings of 684/682/797 “spoken” words were based on a parser error: inline Narration labels caused directions and citations to be counted. Correct original spoken counts are 417/410/427. This correction is explicitly recorded rather than treating those warnings as measured video durations.

After the student requested repair, the current briefs and all six drafts were revised using the newly retained October 15 Fireship sponsored segment. It contributes a small-project function-renaming/test-scaffolding anecdote. The first article describes the reported task; the second distinguishes scaffolding from executed tests; the third proposes a bounded trial with baseline, diff, and behavior checks. Sponsorship, absence of independent validation, and incomplete timing/cost accounting are explicit. This is a topic-relevant new contribution, not a claim that every newly collected item matters.

Current checks pass. Articles are 849/829/867 words excluding references; scripts are 486/485/502 spoken words, estimated at 3.74/3.73/3.86 minutes at 130 words/minute. Final timing needs actual rendering. [Repair record](../runs/20261015T194925Z-8e319e/editorial_revision/README.md) preserves all pre-repair artifacts, evidence locators, edit diff, and current review fingerprint. No additional paid call or recollection was used for this repair.

The original comparator records 38 unequal editorial records. Its comparison includes reasons and assignments, so this number must not be described as 38 changed accept/reject/defer labels. Model variation, new evidence, and the revised policy can all affect results; this is not a controlled policy-only experiment. Six changed source version IDs still require passage-level interpretation before asserting new substantive developments.

Two actual live executions on different dates are recorded, and the second run's current drafts pass mechanical checks after repair. One collection failure remains honestly recorded. The student must still inspect the comparison and revised content. Existing YouTube uploads belong to October 14; no approval or video publication for the October 15 draft version is claimed. Project-level source review and policy records remain linked to the earlier run rather than being fabricated anew for this version.

## Final Publication Choice

The student subsequently selected the October 14 article/video series for final publication. The October 15 run and editorial repair are retained as repeatability and update demonstrations. They do not imply another publication series or require replacement videos. See [version selection](final_series.json). The selected publications retain their October 14 evidence as-of date; final human editorial approval remains pending.
