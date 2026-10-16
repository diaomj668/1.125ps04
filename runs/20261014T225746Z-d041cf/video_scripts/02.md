# A successful signal is not necessarily successful software

As-of: 2026-10-14

**Presentation direction:** Planned for synthetic narration. Retain the spoken AI disclosure. Use labeled diagrams and attributed account cards. Evidence annotations are not spoken.

**Visual direction:** Split screen: “Reported success” on one side, “Delivered outcome” on the other. Display the date.

**Narration:**
This presentation uses AI-generated narration. As of October 14, 2026, the evidence supports a caution for individual developers: a successful signal is not necessarily successful software. A green job status, an addressed review comment, a familiar interface, and a low token price measure different things. None alone proves that the intended outcome was delivered and verified. The question is not whether agents can help, but what evidence supports a claim that their work is done.

**Visual direction:** Illustrative status card reading “Completed,” next to an empty review panel. Label “Acknowledged September 28 incident—not a current live demonstration.”

**Narration:**
Start with a specific delivery failure. In its October availability report, GitHub acknowledged a September 28 incident in which Copilot code review reported successful job completion without producing the review. That establishes a mismatch between status and output. It does not establish a general finding about review accuracy: a missing review and an incorrect review are different problems. But it shows why the completion label cannot substitute for checking that the requested output arrived. [02-c1]

**Inline evidence — not spoken:** [GitHub availability report](https://github.blog/news-insights/company-news/github-availability-report-september-2026/), item `feed:5942317efb2e306a353cac42`, version `2b8477c36458d01b02ef31fabffdfe1ae8339b51ac8a1407d7819528f05c4151`; text locator: “As a result, Copilot code review could not build a review, but reported that the job had completed successfully.”

**Visual direction:** Two metric cards: “Comment prompted a change” and “Change was correct.” Do not draw an equals sign between them.

**Narration:**
Evaluation has a separate gap. GitHub’s ReviewBench deliberately reduces tiny, single-file pull requests, which qualifies its relevance to many solo tasks. GitHub’s production addressed-rate metric measures whether a large language model judges that a review comment prompted a corresponding code change. It does not directly establish that the change was correct. A developer responding to a comment is an observable signal, but correctness is a different question. [02-c2]

**Inline evidence — not spoken:** [ReviewBench documentation](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/), item `feed:9e3099b85951738510dd7533`, version `754cbbbbef0fdf63f52b8ef6428375ee7418da83b3001588ad78d50c265ee276`; text locators: “This reduces the overrepresentation of tiny, single-file changes while preserving more substantive, multi-file pull requests where review quality matters most.” and “Addressed rate, our online counterpart to precision, is the percentage of CCR comments that an LLM determines prompted a developer to make a corresponding code change, based on the diff, thread, reactions, resolution state, and post-review code.”

**Visual direction:** Cursor Security Review card: Teams / Enterprise; access and cost to verify; draft pull requests skipped. Label the feature description as a vendor announcement.

**Narration:**
Cursor’s Security Review announcement provides another distinction: a finding’s format is not proof of accuracy. Cursor describes severity, an attack path, and a proposed fix, while skipping draft pull requests. These are vendor claims about the tool. Individual access and cost remain to be checked, and the supplied evidence does not establish detection accuracy. [02-c6]

**Inline evidence — not spoken:** See [02-c6] in the references for the exact Cursor passages and source version.

**Visual direction:** Attributed account card: “Fireship: FilmCraft editing attempt.” Show “Familiar interface” followed by “Reported playback lag / disappointing transitions.” Include “Video discloses Appify sponsorship.”

**Narration:**
Usability can diverge from appearance, too. Fireship reports attempting to edit a video in FilmCraft and encountering playback-related lag and disappointing transitions despite a familiar interface. This is an attributed usability failure, not a reproducible comparison, and it does not establish that AI caused the defects. Hardware and version details are missing. The video also discloses Appify sponsorship. Keep those limitations attached to the account, rather than turning it into a general verdict. [02-c3]

**Inline evidence — not spoken:** [Fireship video](https://www.youtube.com/watch?v=wajoP_5Cpw8), item `youtube:wajoP_5Cpw8`, version `8744a09c189c7fe57c5beddc39f9817bb8e2d72e7bc3470320481ece2bd2220f`; segment locators: `s00060` (109.76–113.4 seconds), `s00063` (115.2–118.72 seconds), `s00068` (124.56–128.8 seconds), `s00074` (135.84–138.959 seconds), and `s00158` (298.919–303.4 seconds).

**Visual direction:** Separate cards for Lance and Vaishnavi’s team. Label “Different accounts—not a controlled comparison.”

**Narration:**
GitHub’s hackathon reporting offers another reminder about attribution. Participant Lance credits Copilot with creating a frontend and integrating an API in 30 minutes. Elsewhere, GitHub reports Vaishnavi’s team struggling with a movement-detection model. These are different accounts, not a controlled success-versus-failure comparison. Vaishnavi’s difficulty is not identified as a Copilot failure. Neither account tells us what a beginner working alone should expect. [02-c4]

**Inline evidence — not spoken:** [GitHub hackathon account](https://github.blog/developer-skills/career-growth/hack-the-world-why-hackathons-are-still-the-best-place-to-learn-to-build/), item `feed:4194b86040a10a4eac9e887c`, version `f6fa81764f870f94f07aec62e182fa40e3fc33d09536079532a0d241369c0820`; text locators: “GitHub Copilot was able to not only create a frontend in 30 minutes but also connects with the actual API itself and integrates it all together.
Lance, hackathon participant” and “Vaishnavi’s team spent part of the time fighting a model that couldn’t detect their movements. “Like, nothing is working,” Vaishnavi said at one point.”

**Visual direction:** Closing checklist: “Actual output,” “Representative behavior,” “Task-level expenditure.” Footer: “Independent comparisons and maintenance follow-up remain missing.”

**Narration:**
Finally, cost needs an outcome attached. Simon Willison argues that token prices are not readily comparable without knowing how many tokens a model consumes to achieve a goal in an agent workflow. That is not a measured small-project delivery study. Our qualified conclusion is to assess actual output, representative behavior, and task-level expenditure together. Independent controlled research, maintenance follow-up, and representative evidence for budget-constrained and accessibility users remain missing. Favorable signals are clues—not proof of verified delivery. [02-c5]

**Inline evidence — not spoken:** [GitHub availability report](https://github.blog/news-insights/company-news/github-availability-report-september-2026/), item `feed:5942317efb2e306a353cac42`, version `2b8477c36458d01b02ef31fabffdfe1ae8339b51ac8a1407d7819528f05c4151`, text locator: “As a result, Copilot code review could not build a review, but reported that the job had completed successfully.”; [Fireship](https://www.youtube.com/watch?v=wajoP_5Cpw8), item `youtube:wajoP_5Cpw8`, version `8744a09c189c7fe57c5beddc39f9817bb8e2d72e7bc3470320481ece2bd2220f`, segment locator `s00068` (124.56–128.8 seconds); [Willison’s cost discussion](https://simonwillison.net/2026/Oct/13/llm-gemini/), item `feed:6ff0735dfa2a1786602e7b58`, version `a6cb93a068bca6b88086500d4f84badfd6255baa823a198066b04d6a8e160110`, text locator: “Prices like this aren't really comparable these days since what really matters is how many tokens a model takes to achieve a goal within an agentic harness.”


## References

**02-c1** (reported_fact): GitHub's October availability report acknowledged a September 28 incident in which Copilot code review reported successful job completion without producing the review. This establishes a specific output-delivery failure, not a general finding about review accuracy.
- [GitHub availability report: September 2026](https://github.blog/news-insights/company-news/github-availability-report-september-2026/). Passage: “As a result, Copilot code review could not build a review, but reported that the job had completed successfully.” Source version `2b8477c36458d01b02ef31fabffdfe1ae8339b51ac8a1407d7819528f05c4151`.

**02-c2** (reported_fact): ReviewBench's relevance to very small changes is qualified by its deliberate reduction of tiny single-file pull requests. GitHub's production addressed-rate metric measures whether an LLM judges that a comment prompted a code change, rather than directly establishing that the change was correct.
- [ReviewBench: An open benchmark for AI code review](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/). Passage: “This reduces the overrepresentation of tiny, single-file changes while preserving more substantive, multi-file pull requests where review quality matters most.” Source version `754cbbbbef0fdf63f52b8ef6428375ee7418da83b3001588ad78d50c265ee276`.
- [ReviewBench: An open benchmark for AI code review](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/). Passage: “Addressed rate, our online counterpart to precision, is the percentage of CCR comments that an LLM determines prompted a developer to make a corresponding code change, based on the diff, thread, reactions, resolution state, and post-review code.” Source version `754cbbbbef0fdf63f52b8ef6428375ee7418da83b3001588ad78d50c265ee276`.

**02-c3** (source_claim): Fireship reports attempting to edit a video in FilmCraft and encountering playback-related lag and disappointing transitions despite a familiar interface. This supports an attributed usability failure, without establishing that AI caused the defects. The video discloses Appify sponsorship.
- [Every app on Earth is now open source... whether it likes it or not](https://www.youtube.com/watch?v=wajoP_5Cpw8&t=109s), 1:49, segment s00060. Source version `8744a09c189c7fe57c5beddc39f9817bb8e2d72e7bc3470320481ece2bd2220f`.
- [Every app on Earth is now open source... whether it likes it or not](https://www.youtube.com/watch?v=wajoP_5Cpw8&t=115s), 1:55, segment s00063. Source version `8744a09c189c7fe57c5beddc39f9817bb8e2d72e7bc3470320481ece2bd2220f`.
- [Every app on Earth is now open source... whether it likes it or not](https://www.youtube.com/watch?v=wajoP_5Cpw8&t=124s), 2:04, segment s00068. Source version `8744a09c189c7fe57c5beddc39f9817bb8e2d72e7bc3470320481ece2bd2220f`.
- [Every app on Earth is now open source... whether it likes it or not](https://www.youtube.com/watch?v=wajoP_5Cpw8&t=135s), 2:15, segment s00074. Source version `8744a09c189c7fe57c5beddc39f9817bb8e2d72e7bc3470320481ece2bd2220f`.
- [Every app on Earth is now open source... whether it likes it or not](https://www.youtube.com/watch?v=wajoP_5Cpw8&t=298s), 4:58, segment s00158. Source version `8744a09c189c7fe57c5beddc39f9817bb8e2d72e7bc3470320481ece2bd2220f`.

**02-c4** (source_claim): GitHub attributes a 30-minute frontend-and-API integration claim to hackathon participant Lance. Elsewhere it reports Vaishnavi's team struggling with a movement-detection model. These are different accounts, not a controlled success-versus-failure comparison, and Vaishnavi's failure is not identified as a Copilot failure.
- [Hack the World: Why hackathons are still the best place to learn to build](https://github.blog/developer-skills/career-growth/hack-the-world-why-hackathons-are-still-the-best-place-to-learn-to-build/). Passage: “GitHub Copilot was able to not only create a frontend in 30 minutes but also connects with the actual API itself and integrates it all together.
Lance, hackathon participant” Source version `f6fa81764f870f94f07aec62e182fa40e3fc33d09536079532a0d241369c0820`.
- [Hack the World: Why hackathons are still the best place to learn to build](https://github.blog/developer-skills/career-growth/hack-the-world-why-hackathons-are-still-the-best-place-to-learn-to-build/). Passage: “Vaishnavi’s team spent part of the time fighting a model that couldn’t detect their movements. “Like, nothing is working,” Vaishnavi said at one point.” Source version `f6fa81764f870f94f07aec62e182fa40e3fc33d09536079532a0d241369c0820`.

**02-c5** (inference): A defensible delivery assessment needs the actual output, representative behavior, and task-level expenditure—not a completion label or token price alone. The missing review, FilmCraft usability account, and Willison's token-consumption observation identify distinct ways a favorable signal can fall short of the intended outcome.
- [GitHub availability report: September 2026](https://github.blog/news-insights/company-news/github-availability-report-september-2026/). Passage: “As a result, Copilot code review could not build a review, but reported that the job had completed successfully.” Source version `2b8477c36458d01b02ef31fabffdfe1ae8339b51ac8a1407d7819528f05c4151`.
- [Every app on Earth is now open source... whether it likes it or not](https://www.youtube.com/watch?v=wajoP_5Cpw8&t=124s), 2:04, segment s00068. Source version `8744a09c189c7fe57c5beddc39f9817bb8e2d72e7bc3470320481ece2bd2220f`.
- [llm-gemini 0.35](https://simonwillison.net/2026/Oct/13/llm-gemini/). Passage: “Prices like this aren't really comparable these days since what really matters is how many tokens a model takes to achieve a goal within an agentic harness.” Source version `a6cb93a068bca6b88086500d4f84badfd6255baa823a198066b04d6a8e160110`.

**02-c6** (source_claim): Cursor describes Security Review findings with severity, an attack path, and a proposed fix, while skipping draft pull requests. These vendor-described outputs do not establish detection accuracy; individual access and cost also require verification.
- [Rollouts and Security Review](https://cursor.com/changelog/rollouts-and-security-reviewer). Passage: “Both are available today on Teams and Enterprise plans.” Source version `126e7b7700183bbf6dfce1990231a8f468e9de35c1f6ac20a396cd30d761b08c`.
- [Rollouts and Security Review](https://cursor.com/changelog/rollouts-and-security-reviewer). Passage: “It reads every pull request in the context of the codebase and posts one review comment reporting exploitable bugs.” Source version `126e7b7700183bbf6dfce1990231a8f468e9de35c1f6ac20a396cd30d761b08c`.
- [Rollouts and Security Review](https://cursor.com/changelog/rollouts-and-security-reviewer). Passage: “Draft PRs are skipped.” Source version `126e7b7700183bbf6dfce1990231a8f468e9de35c1f6ac20a396cd30d761b08c`.
- [Rollouts and Security Review](https://cursor.com/changelog/rollouts-and-security-reviewer). Passage: “Each finding carries a severity, the attack path, and a proposed fix.” Source version `126e7b7700183bbf6dfce1990231a8f468e9de35c1f6ac20a396cd30d761b08c`.
