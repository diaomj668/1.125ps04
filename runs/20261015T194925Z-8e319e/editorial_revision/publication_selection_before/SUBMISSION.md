# Problem Set 4 Student Submission

**Status:** Two real live runs are recorded on October 14 and October 15 UTC. The October 15 initial drafts failed the YouTube-evidence check; an explicit editorial repair now passes content checks and awaits final student review. Its collection retained 41/42 candidates, with one written-source failure recorded. Three existing Unlisted YouTube videos correspond to the October 14 version. Substack publication, final editorial approval, and reconciliation of the final article/video version remain pending.

**Student:** To be supplied by the student  
**GitHub repository:** Submission repository URL pending

## Topic and Audience

- **Publication name:** Small Project, Real Software
- **Topic:** Recent AI coding assistant capabilities and practices for individual developers completing small software projects.
- **Audience and assumed knowledge:** Individual developers with basic programming and terminal/Git skills who independently build small web apps, scripts, or data tools; includes hobbyists and students.
- **Central question:** Which recent AI coding assistant capabilities and practices help individual developers complete small software projects, including debugging and verification?
- **Scope and exclusions:** Requirements, implementation, debugging, testing, review, and verified delivery costs. Exclude enterprise deployment, model training, and unsupported product rankings.
- **Reason for readers to return:** Follow new capabilities and practical evidence while checking whether earlier judgments still hold.
- **Voice and language:** English, clear, evidence-led, and explicit about uncertainty.

## Published Series

Drafts and word counts are linked in [progress](docs/PROGRESS.md). YouTube videos are uploaded as unlisted; Substack articles and cross-links remain pending.

| Piece | Editorial purpose | Substack article | YouTube video |
| --- | --- | --- | --- |
| 01 | [New ways to supervise, inspect, and constrain coding agents](runs/20261014T225746Z-d041cf/articles/01.md) | Not published | [YouTube (unlisted)](https://youtu.be/pDt5vDDNF7E) |
| 02 | [A successful signal is not necessarily successful software](runs/20261014T225746Z-d041cf/articles/02.md) | Not published | [YouTube (unlisted)](https://youtu.be/8lIFBSltIm0) |
| 03 | [Make the next agent task bounded, inspectable, and affordable](runs/20261014T225746Z-d041cf/articles/03.md) | Not published | [YouTube (unlisted)](https://youtu.be/xV7t_A6FAcw) |

**Separate technical demonstration video:** Not recorded. See [outline](docs/TECHNICAL_DEMO_OUTLINE.md).

## Setup and Execution

Python 3.12 and Bash were used locally. Install dependencies and configure credentials locally:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.lock.txt
# Create .env from .env.example only if .env does not already exist.
bash run.sh
bash run.sh --package runs/RUN_ID
```

Required variables: OPENAI_API_KEY and PIPELINE_MODEL. Never submit secret values. The selected main model is gpt-6.1-sol with medium reasoning effort. Audio transcription uses whisper-1 when supported native timestamped captions are unavailable. Actual tools, models, times, usage, estimated costs, and unknown costs are retained per run.

Topic settings, source definitions, editorial policy and prompts are in their prescribed config/ and prompts/ files and snapshotted for each run. See the [operating guide](docs/OPERATING_GUIDE.md).

## Architecture and Manual Handoffs

```mermaid
flowchart TD
  R[run.sh: metadata and snapshots] --> C[Collection workflow]
  C --> F[RSS collector]
  C --> Y[YouTube collector]
  C --> P[Podcast collector]
  F --> E[Content extraction and timestamped transcripts]
  Y --> E
  P --> E
  E --> D[store.sh: SQLite evidence and versions]
  D --> W[UTC 30-day filtering]
  W --> S[Series workflow]
  S --> A[AI selection]
  A --> B[Three supported briefs]
  B --> N[Article drafts]
  B --> V[Video scripts]
  N --> K[Content checks]
  V --> K
  K --> H[Student review]
  H --> X[Approved package]
  X --> M[Google Vids or HeyGen, Substack, YouTube]
  R --> T[Run summary]
```

All sixteen required Bash entry points are implemented. Each owning component has its own focused helper; no shared application owns the whole pipeline. The collection workflow uses a real Unix pipe. Only data/store.sh and its owning data/store.py access data/evidence/index.sqlite directly.

The automated run reaches drafts, scripts, references and checks. Only the student can supply approval.json matching current reviewed inputs. Packaging independently rechecks the fingerprint and preserves entered publication links.

Three accompanying videos have been produced using Google Vids and uploaded to YouTube as Unlisted. Remaining work: final evidence, synthesis, caption, and audiovisual review; matching editorial approval and packaging; three 600–900 word free-access Substack publications; article/video cross-links; logged-out access checks; the separate technical demonstration; student interpretation of the two-run comparison; and the final reflection and submission repository. Preparing a package is not publication.

## Evidence and Runs

- Canonical evidence index: data/evidence/index.sqlite.
- Retained text and timestamped transcripts: data/assets/.
- Original downloaded media: data/media/; excluded from Git. Retrieve using each saved item's url or media_url and document any omitted media.
- Actual run directories and draft links: [progress](docs/PROGRESS.md).
- Independence, incentives, and missing perspectives: [source notes](docs/SOURCE_NOTES.md).

| Run | Actual UTC date | Artifacts | Elapsed time and estimated cost |
| --- | --- | --- | --- |
| Clean live run with same-day recovery | 2026-10-14 | [Summary](runs/20261014T225746Z-d041cf/summary.json), [review](runs/20261014T225746Z-d041cf/review.json), [recovery](runs/20261014T225746Z-d041cf/recovery_status.json) | Initial and recovery receipts retained; estimated model tokens $1.9788, plus unpriced audio/failed calls |
| Second-day live run with editorial repair | 2026-10-15 | [Summary](runs/20261015T194925Z-8e319e/summary.json), [review](runs/20261015T194925Z-8e319e/review.json), [repair record](runs/20261015T194925Z-8e319e/editorial_revision/README.md) | Original run about 463.6 seconds; estimated model cost $2.1453; editorial repair made no new paid calls |

Previous generated attempts and fictional replay outputs were deleted before this clean restart. They are not part of the submitted evidence. Both actual live runs are preserved. [Two-run comparison](docs/run-comparison.md) explains five newly retained items, six changed version IDs, thirty unchanged items, and the second-run editorial repair. Changed hashes alone do not establish meaningful source developments.

## Editorial Review

The six-item student source-review sample is complete. Inspect the [review worksheet](runs/20261014T225746Z-d041cf/human_review.md) and its linked actual evidence. Personally compare at least three accepted and three rejected/deferred decisions, record corrections, revise the policy, and preserve before/after outputs. The original policy remains preserved; the implemented student-requested clarification and actual selection comparison are linked below. Student interpretation is complete; revised-draft approval is pending. Mechanical checks cannot establish source independence, semantic support, or sound interpretation.

## Reflection

To be completed by the student using the run's actual findings and personal review. Discuss one insight, one editorial limitation, one next improvement, and one architectural tradeoff.

An implemented tradeoff is media caching: unchanged native IDs, titles and publication metadata permit transcript reuse, reducing cost but potentially missing edits in place. Written content is fetched again and versioned by substantive content rather than retrieval time.

## Student Policy Revision Update

The student supplied judgments for three accepted and three rejected/deferred sources. The access/setup/relevance policy clarification was implemented, with before/after versions and a real selection rerun on identical saved evidence. [Actual comparison](runs/20261014T225746Z-d041cf/policy_revision/comparison.md) records four changed decisions and model-variation limits. The student completed the comparison interpretation and authorized incorporating narrow Cursor coverage. Initial drafts are preserved in editorial_revision/before/. The October 14 revised drafts passed content checks. The October 15 live run is now recorded and its repaired drafts also pass; final approval and Substack publication remain pending.

## October 14 Revised Draft Handoff

[Revision record](runs/20261014T225746Z-d041cf/editorial_revision/README.md) preserves the initial artifacts, exact changes, and actual edit time. Current article word counts are 854, 859, and 847; narration word counts are 468, 496, and 520. References and claim manifests match the revised briefs. Final student approval has not been supplied.

## Current Video Review Drafts

Three actual Google Vids MP4 exports are available for student review. [Editors, exports, production method, and limitations](runs/20261014T225746Z-d041cf/video_production/google_vids/README.md) are recorded separately from the failed HeyGen attempts. Full caption and audiovisual review, final editorial approval, Substack publication, cross-links, and logged-out access checks remain pending. Actual YouTube unlisted links are recorded in the Published Series table above.

## October 15 Repaired Draft Handoff

Latest drafts are in `runs/20261015T194925Z-8e319e/articles/` and `video_scripts/`. [Repair and verification](runs/20261015T194925Z-8e319e/editorial_revision/README.md) preserve the failed initial outputs, exact changes, and a timestamped original YouTube contribution. The articles contain 849, 829, and 867 words excluding references; the scripts contain 486, 485, and 502 spoken words, estimated at 3.74, 3.73, and 3.86 minutes at 130 words/minute. Actual rendering must confirm timing. The initial length warnings counted nonspoken material and are explicitly corrected in the repair record.

The student must review this revision before approval. Existing publication links above correspond to October 14 and are not represented as videos of the October 15 scripts. Confirm the final series version and update or produce its matching video content as needed before final publication. No new approval, video rendering, or publication is claimed by this repair.
