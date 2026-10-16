# HeyGen Production Instructions

Title: Make the next agent task bounded, inspectable, and affordable
Language: English
Format: 16:9 landscape, 1920 x 1080 if available.
Evidence as-of date: 2026-10-14. This is the evidence collection date, not the render date.
Target duration: 3–5 minutes. Estimated narration at 125 words per minute: 246.7 seconds; verify actual render duration.

Use the exact narration below. Use a clear, neutral English synthetic voice at approximately 125 words per minute. Preserve the opening spoken AI disclosure. Do not read scene labels, claim IDs, visual directions, evidence annotations, URLs, or source hashes aloud.

Use clean typography, simple diagrams, and subtitles. Do not use a digital twin, public preset avatar, or any visible presenter. Use an ordinary neutral synthetic English narrator, with diagrams and subtitles. Do not clone a voice. Use illustrative screens, not fabricated product demonstrations or invented test results. Show short publisher credits near the relevant scenes and the evidence as-of date. Retain uncertainty and access/cost limitations. Do not introduce factual assertions or imply the series is published. Render a draft for review; do not upload to YouTube or publish.

## Scenes

### Scene 1
Visual direction (not spoken): Title card and date. Show a loop: “Define → Check → Inspect → Account for effort → Decide.”
Narration (spoken exactly): This presentation uses AI-generated narration. As of October 14, 2026, the strongest practical implication of the supplied evidence is modest: try one bounded agent task with explicit checks and a stopping budget before expanding autonomy. Record how to test it, inspect what arrives, and include correction and verification in the cost. This is a proposed evaluation workflow, not a proven productivity recipe. We do not have a comparison showing that it improves small-project completion rates.

### Scene 2
Visual direction (not spoken): File cards for `.github/copilot-instructions.md` and `.github/skills/quality-checks/SKILL.md`. Highlight “Test commands,” “What they check,” and “Troubleshooting.”
Narration (spoken exactly): Begin by making testing expectations explicit. For a Copilot repository, GitHub describes a repository instruction file where you can record expectations for testing and validation. It also describes a quality-checks skill that can explain which scripts run tests and linting, what they check, and how to troubleshoot failures. Linting means checking code against specified rules. These are places to record guidance—not proof that the agent followed it, or that any check ran and passed.

### Scene 3
Visual direction (not spoken): Review checklist with separate boxes: “Status says complete” and “Review output exists.” Add an attributed September incident card.
Narration (spoken exactly): Next, inspect delivery. GitHub acknowledged a September incident in which Copilot code review reported successful completion without producing the review. It advised customers to request affected reviews again. So check whether your requested review actually arrived, instead of relying only on its status. For future reliability reporting, watch for evidence that reviews were delivered, not merely that jobs were labeled successful. Instructions and status indicators cannot replace looking at the output.

### Scene 4
Visual direction (not spoken): Cursor Security Review card: Teams / Enterprise; access and cost to verify; draft pull requests skipped. Label the feature description as a vendor announcement.
Narration (spoken exactly): If considering Cursor Security Review, verify individual access and cost first. Check pull-request eligibility, because the announcement skips drafts. Inspect each reported attack path and proposed fix, and try to reproduce the finding. These are proposed verification steps, not a claim that the tool has been independently validated.

### Scene 5
Visual direction (not spoken): Diagram showing a main thread and worker thread feeding a profile. Label “Willison’s workload: 95.1% of stacks from AnyIO’s worker thread.”
Narration (spoken exactly): Diagnostic checks also need the right coverage. In Simon Willison’s web-edit profiling example, sampling all threads was essential: 95.1 percent of recorded stacks came from AnyIO’s worker thread and would have been missed by a main-thread-only profile. Threads are separate execution paths within an application. If you ask an agent to profile a threaded Python app, check that the profile includes the threads doing the work. Inspect its flame graph and heatmap before choosing an optimization. This is a conditional check, not a prediction of your bottleneck.

### Scene 6
Visual direction (not spoken): Attributed podcast cards: “Short tasks + check-ins” and “Longer orchestration exhausted usage.” Avoid universal quota or model-ranking graphics.
Narration (spoken exactly): Keep the first trial bounded. On HTML All The Things, one host describes short agent tasks with periodic check-ins. Another reports that longer orchestration burned through usage and prompted a return to smaller tasks. Those practitioner accounts support trying bounded work before assuming a subscription can sustain a longer cycle. They do not establish a universal quota, an ideal task duration, or a best model.

### Scene 7
Visual direction (not spoken): Trial record template: “Observable outcome / Checks / Retained outputs / Agent usage / Human testing and correction time / Stopping budget.” End on “Expand only after inspecting the whole cycle.”
Narration (spoken exactly): For your next trial, define one observable outcome, specify its checks, retain their outputs, and record agent usage alongside human testing and correction time. Expand only after examining that whole cycle. Instructions can be ignored, tests can miss bugs, and review adds effort that a solo developer must bear. Experienced practitioners’ judgment may not transfer to beginners. Start with checks you understand; another model’s agreement is not a substitute. The evidence to seek next is repeatable small-project results, including failures and total effort—not just prices or completion messages.
