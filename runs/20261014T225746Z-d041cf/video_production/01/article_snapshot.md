# New ways to supervise, inspect, and constrain coding agents

*As of 2026-10-14.*

The clearest recent developments in coding assistants concern how a developer supervises work and examines its results—not demonstrated improvements in the quality of finished software. Cursor describes remote access to local agents. GitHub announces a developer-facing secret-review command. Simon Willison reports asking an agent to produce profiling artifacts. These developments address different questions: Can I direct the work? Can I check for a particular problem? Can I investigate what the program is doing? Treating them as equivalent promises of autonomous delivery would overstate the evidence. [01-c5]

## Remote access changes supervision, not execution

Cursor’s October 6 announcement says its iOS app can display local agents running on a developer’s computer and accept replies. The important boundary is where execution happens: the agent remains on that computer, which must stay on and online. This is remote supervision of an existing local process, not a transfer of the work to another machine. [01-c1] ([Cursor, “Remote control for local agents”](https://cursor.com/changelog/remote-control-local-agents), published 2026-10-06T00:00:00Z.)

For an individual project, the plausible benefit is continuity of oversight: being able to see what an agent is doing and send a message without sitting at the computer. That is an interpretation of the announced interaction, not a measured productivity result. The announcement does not establish that remote replies lead to better code, fewer corrections, or a completed project. Its online-computer requirement also remains part of any practical assessment. [01-c1] [01-c5]

## A secret check has a narrower job than a security guarantee

GitHub’s October 7 announcement describes a `/security-review` command for Copilot CLI and Copilot App users, allowing them to address secrets before a push without requiring an organization’s GitHub Secret Protection plan. Keep this developer-facing command distinct from the organization push-protection feature that the same article describes as being in private preview. Those are separate availability statements, not interchangeable descriptions of one capability. [01-c2] ([GitHub, “Secret protection must scale with software”](https://github.blog/ai-and-ml/github-copilot/secret-protection-must-scale-with-software/), published 2026-10-07T17:45:34Z.)

For a solo developer, the relevant possibility is a specific check within tools they may use, rather than an organization-level prerequisite. But an announced command is not independent evidence of how effectively it identifies problems in a small project. Assess it as a secret-checking step whose results need inspection—not as a declaration that the whole application is safe. The supplied evidence establishes GitHub’s announcement, not comprehensive protection. [01-c2] [01-c5]

Cursor’s September 23 announcement also describes Security Review as checking pull requests for exploitable bugs and supplying a severity, attack path, and proposed fix. It lists Teams and Enterprise access and skips draft pull requests. Individual access and cost still need checking; the announcement does not independently establish effectiveness. [01-c6]

## Diagnostic artifacts offer something concrete to inspect

Willison’s October 12 account describes directing Codex to profile his web-edit Python app and produce a flame graph and heatmap. These are diagnostic views of where execution time is spent. The concrete result in this account is therefore an investigation artifact, not a demonstrated optimization gain. [01-c3] ([Simon Willison, “Profiling web-edit with Python 3.15: flame graphs and source heatmaps”](https://simonwillison.net/2026/Oct/12/python-3-15-web-edit-profiling/), published 2026-10-12T16:58:00Z.)

That distinction matters when asking an assistant to “make this faster.” An artifact gives the developer something to examine before deciding what to change; it does not itself establish that a change improved performance. Willison is an experienced practitioner reporting on his own app. The account supplies neither a controlled comparison nor complete effort accounting, and his ability to choose and interpret diagnostics may not transfer to someone with basic programming skills. [01-c3]

## Evaluation resources are not project-specific endorsements

GitHub also announced ReviewBench as an available evaluation resource for code-review agents. Its reported corpus contains 219 pull requests—proposed code changes—from 187 public repositories across 19 languages. That makes it a concrete resource to examine, but its availability does not establish that any particular reviewer suits a small project. [01-c4] ([GitHub, “ReviewBench: An open benchmark for AI code review”](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/), published 2026-10-05T15:59:40Z.)

A broad repository evaluation and a small script answer different practical questions. Before treating benchmark evidence as relevant, ask whether the evaluated work resembles the change you need reviewed. The supplied material does not close that transfer gap. [01-c4]

## The useful distinction: access, checks, artifacts

Taken together, these sources support a restrained interpretation: remote access lets you direct work, a targeted check can flag possible problems, and diagnostic artifacts let you investigate. Their practical value depends on whether you can inspect the resulting work and use the relevant check. None alone establishes that delivery is complete. [01-c5]

First-time users, accessibility users, and unsuccessful small-project attempts remain insufficiently represented here. The announcements and practitioner account offer specific capabilities worth examining, not grounds for a product ranking or a general promise of autonomous completion. For an individual developer, the useful question is which missing part of supervision or verification each addition addresses—and which parts remain yours to assess. [01-c5]


## References

**01-c1** (reported_fact): Cursor announced that its iOS app can display local agents and accept replies. Execution remains on the developer's computer, which must stay on and online.
- [Remote control for local agents](https://cursor.com/changelog/remote-control-local-agents). Passage: “You can now see and reply to the local agents running on your computer from the Cursor iOS app.” Source version `f0b87f5852d125e85cbeb2438fe5d0ee73e1a1bface9f1ea7031804286fb5ea1`.
- [Remote control for local agents](https://cursor.com/changelog/remote-control-local-agents). Passage: “Your computer needs to stay on and online for remote control to work.” Source version `f0b87f5852d125e85cbeb2438fe5d0ee73e1a1bface9f1ea7031804286fb5ea1`.

**01-c2** (reported_fact): GitHub announced a /security-review command for Copilot CLI and Copilot App users without requiring an organization's Secret Protection plan. This is distinct from the organization push-protection feature described as being in private preview.
- [Secret protection must scale with software](https://github.blog/ai-and-ml/github-copilot/secret-protection-must-scale-with-software/). Passage: “/security-review command for the Copilot CLI and Copilot App, so Copilot users can address secrets before a push even without needing an organization’s GitHub Secret Protection plan.” Source version `8575119cd60816d0cd6c477201ca1ae2245015a6a27d45f5af8b9da87e6c352c`.
- [Secret protection must scale with software](https://github.blog/ai-and-ml/github-copilot/secret-protection-must-scale-with-software/). Passage: “The feature is currently in private preview. Later this month, the feature will be available to organizations with GitHub Secret Protection across Enterprise Cloud and GitHub Teams. It will consume AI credits.” Source version `8575119cd60816d0cd6c477201ca1ae2245015a6a27d45f5af8b9da87e6c352c`.

**01-c3** (source_claim): Simon Willison reports directing Codex to profile his web-edit Python app and produce a flame graph and heatmap—diagnostic views of where execution time is spent. This is a concrete debugging use, not a demonstrated optimization gain.
- [Profiling web-edit with Python 3.15: flame graphs and source heatmaps](https://simonwillison.net/2026/Oct/12/python-3-15-web-edit-profiling/). Passage: “I put the new Python 3.15 profiler through its paces by having GPT-6 Astra Extra High in Codex run it against my new web-edit app:” Source version `de47f3a642088f8a087f0a6f46b95b49b6830aa108fd56ccd1dec0cf490cb5f8`.
- [Profiling web-edit with Python 3.15: flame graphs and source heatmaps](https://simonwillison.net/2026/Oct/12/python-3-15-web-edit-profiling/). Passage: “Here's the resulting example flame graph and heatmap.” Source version `de47f3a642088f8a087f0a6f46b95b49b6830aa108fd56ccd1dec0cf490cb5f8`.

**01-c4** (reported_fact): GitHub launched ReviewBench as an available evaluation resource for code-review agents. Its reported corpus contains 219 pull requests from 187 public repositories across 19 languages; that availability is not itself evidence that a particular reviewer suits a small project.
- [ReviewBench: An open benchmark for AI code review](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/). Passage: “We built ReviewBench, a new code review offline benchmark, to address that gap, and it is available for you to use today.” Source version `754cbbbbef0fdf63f52b8ef6428375ee7418da83b3001588ad78d50c265ee276`.
- [ReviewBench: An open benchmark for AI code review](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/). Passage: “ReviewBench contains 219 pull requests from 187 public open source licensed repositories spanning 19 languages, with its language and repository-size distributions closely matching GitHub overall.” Source version `754cbbbbef0fdf63f52b8ef6428375ee7418da83b3001588ad78d50c265ee276`.

**01-c5** (inference): For a small project, these developments are better assessed as separate additions to supervision, secret checking, and diagnosis than as interchangeable promises of autonomous delivery. Their practical value depends on whether the developer can inspect the resulting work and use the relevant check.
- [Remote control for local agents](https://cursor.com/changelog/remote-control-local-agents). Passage: “Your local agents appear in a list. Tap one to see what it's doing or send it a message.” Source version `f0b87f5852d125e85cbeb2438fe5d0ee73e1a1bface9f1ea7031804286fb5ea1`.
- [Secret protection must scale with software](https://github.blog/ai-and-ml/github-copilot/secret-protection-must-scale-with-software/). Passage: “/security-review command for the Copilot CLI and Copilot App, so Copilot users can address secrets before a push even without needing an organization’s GitHub Secret Protection plan.” Source version `8575119cd60816d0cd6c477201ca1ae2245015a6a27d45f5af8b9da87e6c352c`.
- [Profiling web-edit with Python 3.15: flame graphs and source heatmaps](https://simonwillison.net/2026/Oct/12/python-3-15-web-edit-profiling/). Passage: “Here's the resulting example flame graph and heatmap.” Source version `de47f3a642088f8a087f0a6f46b95b49b6830aa108fd56ccd1dec0cf490cb5f8`.

**01-c6** (reported_fact): Cursor announced Security Review for pull-request security checks on Teams and Enterprise plans. The announcement says findings include severity, an attack path, and a proposed fix, and that draft pull requests are skipped. It does not establish individual purchasing eligibility, total cost, or independent effectiveness.
- [Rollouts and Security Review](https://cursor.com/changelog/rollouts-and-security-reviewer). Passage: “Both are available today on Teams and Enterprise plans.” Source version `126e7b7700183bbf6dfce1990231a8f468e9de35c1f6ac20a396cd30d761b08c`.
- [Rollouts and Security Review](https://cursor.com/changelog/rollouts-and-security-reviewer). Passage: “It reads every pull request in the context of the codebase and posts one review comment reporting exploitable bugs.” Source version `126e7b7700183bbf6dfce1990231a8f468e9de35c1f6ac20a396cd30d761b08c`.
- [Rollouts and Security Review](https://cursor.com/changelog/rollouts-and-security-reviewer). Passage: “Draft PRs are skipped.” Source version `126e7b7700183bbf6dfce1990231a8f468e9de35c1f6ac20a396cd30d761b08c`.
- [Rollouts and Security Review](https://cursor.com/changelog/rollouts-and-security-reviewer). Passage: “Each finding carries a severity, the attack path, and a proposed fix.” Source version `126e7b7700183bbf6dfce1990231a8f468e9de35c1f6ac20a396cd30d761b08c`.
