# Periodic consolidation at checkpoints: when and how a solo developer (with an AI agent) should stop and consolidate

Source-quality legend used below:
- **[primary, read]** = I read the original page or PDF.
- **[search summary]** = I only saw a search-engine summary of the page; wording and attribution to the exact URL are not verified. Treat as leads, not as quotes.

## 1. Which checkpoint triggers are recommended (time-based vs. scope-based vs. volume-based), and how short can a review be?

### Takeaway
The established practices split cleanly: AAR and stage-gate reviews are **scope-triggered** (after an event, phase, or stage), while GTD and Scrum are **time-triggered** (weekly, per sprint). None of the sources I read defines a **volume-based** trigger (e.g. "every N decisions"). The shortest duration with a named source is a 15-minute informal AAR.

### Cited Findings
- AAR timing is tied to the event, not the calendar: "An AAR can be used immediately after an action, event, or at the end of a project. It is critical that the review occurs within 1 to 2 weeks of the event or project. It can also be used during key phases of a longer project or informally during project implementation." **[primary, read]** — [Layland, Koehler, Simpson (2020), After Action Review Guide, National Comprehensive Center, p.5](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- AAR duration: a formal AAR at organization level "requires at least 4 hours", a team-level AAR "about 2 hours", and "An informal review could be conducted in whatever time a team can allot. 'A conversation as short as 15 minutes might identify barriers to progress and strategies to overcome them'" (quoting Salem-Schatz et al.). The same passage warns "an AAR should never be rushed". **[primary, read]** — [After Action Review Guide, p.5](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- Formal vs. informal AAR (table adapted from US Army TC 25-20, 1993): formal ones "are scheduled beforehand" and "take more time"; informal ones "are conducted by internal staff", "take less time", "are scheduled when needed", and happen "at the event or project site". **[primary, read]** — [After Action Review Guide, p.6, Table 1](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- The four AAR questions as this guide words them: "1. What was expected to happen? 2. What actually happened? 3. What went well and what didn't work? (What caused our results?) 4. What will we sustain or improve? What will we do to adapt or refine our executions for a better outcome?" **[primary, read]** — [After Action Review Guide, pp.8-9](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- An AAR starts by restating the plan before discussing results: it "begins with restating the task, purpose, intent, and anticipated results or end state", and the anchoring question is "Did we carry out the work as intended for the purpose and did we get the anticipated results?" **[primary, read]** — [After Action Review Guide, p.8](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- A facilitator tip relevant to a solo reviewer: "Give participants time to think about and write down their recollections" and "Recognize that most lessons that first surface are incomplete or wrong, representing what the unit thinks should work, not what really does work". **[primary, read]** — [After Action Review Guide, pp.8-9](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- The guide names the failure mode of reviews that only produce documents: post-mortems "result in static reports that are all too often filed away and forgotten". **[primary, read]** — [After Action Review Guide, p.4](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- Origin: AARs "were originally developed by the U.S. Army's National Training Center for use by the Opposing Force" (citing Training Circular 25-20). **[primary, read]** — [After Action Review Guide, p.3](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- GTD Weekly Review is time-triggered (weekly) and has three blocks. GET CLEAR: collect loose papers, get "IN" to zero, empty your head. GET CURRENT: review action lists, previous calendar, upcoming calendar, waiting-for list, project lists, checklists. GET CREATIVE: review someday/maybe, be creative. The project step reads: "Evaluate status of projects, goals, and outcomes, one by one, ensuring at least one current action item on each." **[primary, read]** — [GTD Weekly Review checklist, David Allen Company](https://gettingthingsdone.com/wp-content/uploads/2014/10/Weekly_Review_Checklist.pdf)
- Scrum's retrospective is time-triggered per sprint, capped at three hours for a one-month sprint and usually shorter for shorter sprints; its purpose is to plan ways to increase quality and effectiveness, and the most helpful changes may be added to the next Sprint Backlog. **[search summary]** — [Scrum.org, What is a Sprint Retrospective](https://www.scrum.org/resources/what-is-a-sprint-retrospective)
- PRINCE2 is scope-triggered at stage boundaries: the End Stage Report is produced by the project manager to obtain approval to proceed to the next stage and reviews the stage that is finishing, the business case, and issues and major risks. **[search summary]** — [projectengineer.net, The 26 project documents of PRINCE2](https://projectengineer.net/the-26-project-documents-of-prince2)
- Solo-retro practitioner reports **[search summary]**: a solo consultant runs a six-quadrant quarterly retro of about ninety minutes where each quadrant ends in one yes/no decision, and argues team formats feel performative for one person — [pravinkumar.co](https://www.pravinkumar.co/blog/quarterly-retrospective-solo-webflow-practice-2026); a one-page personal retro with five prompts (start, do more, keep, do less, drop) — [t2informatik](https://t2informatik.de/en/downloads/personal-retro-template/); solo game-dev guide suggesting Start/Stop/Continue for efficiency and Mad/Sad/Glad for morale — [wayline.io](https://www.wayline.io/blog/no-nonsense-retrospectives-solo-game-dev)

### Inferences
- For this project, time-based cadence is a poor fit. About 140 decision rows and 137 commits accumulated in roughly 2 days, so a weekly review would cover several hundred rows at once, which recreates the "re-understand everything at once" problem on a smaller scale. A scope trigger aligned to units the project already has (stage end; possibly a group of closed sub-issues within a long stage) matches AAR and PRINCE2 practice.
- The AAR sources support two tiers the project could map directly: a very short informal check per closed issue, and a slightly longer one per stage. The project already has the per-issue artifact (closing comment). What is missing is the stage-level tier and any step where the human does something other than read.
- AAR question 1 ("what was expected to happen?") is the piece most likely absent from the existing records. Decision tables record what was decided and why; judgment logs record what was observed. Neither is organized around "what did we intend this stage to achieve, and did it?".
- A volume-based safety trigger (e.g. "if a stage exceeds N decision rows, do a mid-stage checkpoint") is my own suggestion. No source I read prescribes one.

### Gaps
- I did not obtain the original text of US Army TC 25-20. The four questions above are the wording of a 2020 US Department of Education-funded guide that adapts TC 25-20, not the Army's own wording. Do not present them as verbatim Army text.
- Derby & Larsen, *Agile Retrospectives* (the five-phase structure) was not retrieved. Nothing here is sourced to it.
- The Scrum Guide 2020 itself was not fetched; the timebox comes from search summaries of scrum.org pages.
- I found no empirical study comparing time-based and scope-based review triggers for solo developers, and no evidence on the minimum effective length of a solo retrospective. The "15 minutes" figure is a practitioner statement quoted in a guide, not a measured result.
- The solo-retro sources are individual blog posts seen only as search summaries; they are experience reports, not evidence of effectiveness.

## 2. Progressive summarization and layered notes: how the layers work, criticisms, and translation to a project log

### Takeaway
Progressive summarization keeps the full source and adds thinner layers on top **only when a note is revisited**, so detail is never deleted, and Forte explicitly says most notes should not get the top layers. Its transferable idea for a project log is "summary layer on top, detail intact below, summarize opportunistically"; its weakness is that highlighting and summarizing are rated low-utility for learning.

### Cited Findings
- Layers, as defined in Forte's original post **[primary, read via fetch tool]**: Layer 0 "is the original, full-length source text"; Layer 1 is the initial capture of "anything that feels insightful, interesting, or useful"; Layer 2 is bolding the best parts; Layer 3 is highlighting the "best of the best", done only "when I'm already reviewing the note anyway"; Layer 4 is an executive summary in one's own words at the top, reserved for "a small number of notes that are the most insightful". A further unnumbered "remix" step applies to a "tiny minority of sources". — [Forte Labs, Progressive Summarization: A Practical Technique for Designing Discoverable Notes](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)
- Summarization is opportunistic, not scheduled: it happens "in small spurts, spread across time, in the course of other work", "only doing as much or as little as the information deserves". — [Forte Labs, same post](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)
- The stated tradeoff: "you cannot compress something without losing some of its context". Over-compressed notes scan fast but lose why they mattered; over-detailed notes keep context but bury the key ideas. Keeping earlier layers intact is the mitigation. — [Forte Labs, same post](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)
- Forte's own follow-up warns that applying every layer to every note is perhaps the biggest mistake adopters make, and that more summarization is not better. **[search summary]** — [Forte Labs, Progressive Summarization III: Guidelines and Principles](https://fortelabs.com/blog/progressive-summarization-iii-guidelines-and-principles/)
- Criticism attributed to Nick Milo: the method can lead to over-collecting, over-summarizing, and under-thinking; highlighting can create an illusion of learning where familiarity is mistaken for understanding. **[search summary, single secondary wiki-style source; not verified against Milo's own writing]** — [concepts.dsebastien.net, Progressive Summarization](https://concepts.dsebastien.net/concept/progressive-summarization/)
- Independent support for the "illusion" concern: Dunlosky et al. (2013) rated summarization, highlighting, and rereading as low utility among ten study techniques. **[search summary of the APS press release]** — [Association for Psychological Science, Which Study Strategies Make the Grade?](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)

### Inferences
- Mapping to this project: Layer 0 = raw results and commits; Layer 1 = decision rows and judgment-log rows (already exists); Layer 4 = a short stage-level summary (does not exist until stage 8). Layers 2-3 (bold/highlight) translate to marking the few rows per stage that actually changed direction. The gap is Layer 4 at stage granularity, plus a marker for "which of these 140 rows mattered".
- Forte's "only as much as the information deserves" argues against summarizing every decision row. Most rows are procedural; a stage rollup should name a handful of direction-setting decisions and link to the rest.
- The compression/context tradeoff implies the rollup should link back to row IDs rather than restate reasons, so context is recoverable without duplicating it.
- The low-utility rating for summarization and highlighting concerns the learner's own summarizing as a study technique. An AI-written summary that the human only reads is, if anything, closer to rereading. So a summary layer alone is unlikely to solve the user's "I do not retain why we did that" problem; see section 4.

### Gaps
- Andy Matuschak's evergreen-notes writing and Zettelkasten critiques of progressive summarization were not retrieved. I have no sourced statement from them.
- I found no empirical study of progressive summarization's effectiveness. All claims about it are from its author or from critics.
- Whether Dunlosky's "low utility" rating for summarization came with the caveat that it helps learners already skilled at summarizing is something I recall but did not verify in a fetched source; do not state it as fact.

## 3. Devlogs, weeknotes, changelogs, done lists, release notes: which formats are designed for human re-reading and how they are structured

### Takeaway
Keep a Changelog is the one format here with an explicit design rule that it is for human readers and that commit logs are not a substitute; its structure (newest first, grouped by change type, an "Unreleased" section on top that is rolled into a dated entry at release) is directly reusable for a stage rollup. Weeknotes are deliberately format-free and their value claim is habit, not structure.

### Cited Findings
- Keep a Changelog guiding principles **[primary, read via fetch tool]**: "Changelogs are for humans, not machines." "There should be an entry for every single version." "The same types of changes should be grouped." "Versions and sections should be linkable." "The latest version comes first." "The release date of each version is displayed." — [keepachangelog.com 1.1.0](https://keepachangelog.com/en/1.1.0/)
- Change types: Added, Changed, Deprecated, Removed, Fixed, Security. — [keepachangelog.com 1.1.0](https://keepachangelog.com/en/1.1.0/)
- The "Unreleased" mechanism: "Keep an `Unreleased` section at the top to track upcoming changes"; "At release time, you can move the `Unreleased` section changes into a new release version section." — [keepachangelog.com 1.1.0](https://keepachangelog.com/en/1.1.0/)
- Why raw history is not a rollup: "Using commit log diffs as changelogs is a bad idea: they're full of noise." A changelog entry exists to communicate changes clearly, which often means summarizing across multiple commits. — [keepachangelog.com 1.1.0](https://keepachangelog.com/en/1.1.0/)
- Weeknotes have no set format; one guide suggests about 150 words drafted in about 30 minutes (5 outline, 15 draft, 10 edit); another approach keeps a running daily list during the week and publishes it as is. **[search summary]** — [Medium / We The Catalysts, Weeknotes: how to write one in 30 minutes](https://medium.com/wethecatalysts/weeknotes-how-to-write-one-in-30-minutes-ef3eef0e41f7)
- A weeknotes cadence heuristic reported in a team guide: you can miss one, but do not miss two in a row. **[search summary; the summary did not make clear which of the returned pages states this]** — candidates: [public.digital, No prizes for week notes](https://public.digital/2019/08/02/no-prizes-for-week-notes); [digitalbydefault.com, The why of weeknotes](https://digitalbydefault.com/2017/03/05/the-why-of-weeknotes/)

### Inferences
- The changelog's "Unreleased then cut a dated entry" maps to "current stage section stays open; at stage end it is frozen under the stage name". This gives a natural, scope-based moment to consolidate without adding a new document type per issue.
- "Commit logs are full of noise" applies equally to 137 commits and 140 decision rows: both are complete records, neither is a rollup. The decision tables are the equivalent of a commit log for reasoning. That is the structural reason the human cannot re-orient from them quickly.
- Changelog change types do not fit a reasoning trail. An analogous grouping for this project would be by kind of outcome (e.g. decided / changed our mind / ruled out / still open), since "changed our mind" and "ruled out" are exactly what "why did we do that?" questions target. This grouping is my proposal, not from a source.
- The 150-word weeknote figure is a useful upper bound for the human-authored part of a stage review.

### Gaps
- I found no retrievable authoritative source on indie devlog structure, "done lists", or release-notes practice within the call budget. Nothing in these notes is sourced on those three formats.
- No evidence on whether weeknotes improve the author's own later recall; sources describe them as a communication and habit practice.
- The weeknotes findings are search summaries of blog posts and should be treated as weak.

## 4. Learning-science evidence relevant to reviewing one's own project

### Takeaway
The best-supported techniques are retrieval practice and distributed (spaced) practice; rereading, highlighting, and summarization are rated low. Applied here: one massed read-through at stage 8 is the weakest design, and reading an AI-written summary is close to rereading, so the human should recall the stage from memory first and only then check the summary.

### Cited Findings
- Dunlosky, Rawson, Marsh, Nathan & Willingham (2013, *Psychological Science in the Public Interest*) rated ten techniques: **high** utility for practice testing and distributed practice; **moderate** for interleaved practice, elaborative interrogation, and self-explanation; **low** for summarization, highlighting, the keyword mnemonic, imagery use for text learning, and rereading. **[search summary of the APS press release]** — [Association for Psychological Science, Which Study Strategies Make the Grade?](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)
- Roediger & Karpicke (2006, *Psychological Science*): students studied prose passages and either took one or three immediate free-recall tests without feedback or restudied the same number of times; final tests came after 5 minutes, 2 days, or 1 week. At 5 minutes, repeated studying beat repeated testing; on the delayed tests, prior testing produced substantially greater retention than restudying. **[abstract as relayed by search; the PubMed page itself would not load, so wording is not verified verbatim and I report no percentages]** — [PubMed 16507066](https://pubmed.ncbi.nlm.nih.gov/16507066/)
- Cepeda, Vul, Rohrer, Wixted & Pashler (2008, *Psychological Science* 19(11), 1095-1102): more than 1,350 people learned facts, reviewed them after a gap of up to 3.5 months, and were tested up to 1 year later. At any test delay, lengthening the gap first improved then gradually reduced final performance. The optimal gap, as a proportion of test delay, "declined from about 20 to 40% of a 1-week test delay to about 5 to 10% of a 1-year test delay". **[abstract as relayed by search]** — [PubMed 19076480](https://pubmed.ncbi.nlm.nih.gov/19076480/)
- A York University release about the same study adds that a too-short interval is much more detrimental to retention than one that is too long. **[search summary of a press release]** — [York University YFile](https://www.yorku.ca/yfile/?p=9454)
- Slamecka & Graf (1978, *Journal of Experimental Psychology: Human Learning and Memory*, 4(6), 592-604): across five experiments, words that subjects generated themselves were remembered better than the same words simply read; "performance in the generate condition was superior to that in the read condition" across recognition, recall, and confidence measures. **[abstract as relayed by search]** — [Slamecka & Graf 1978 PDF hosted by Andy Matuschak](https://andymatuschak.org/prompts/Slamecka1978.pdf)
- Caveat on the generation effect reported by a secondary source: later experiments in the paper showed smaller effects and free-recall advantages are not always found in later work. **[search summary]** — [Andy Matuschak's notes, Generation effect](https://notes.andymatuschak.org/z26C6ing3sqiZMHRVFuT6xn)

### Inferences
- **Which part the human must do themself.** The AI can draft the summary, but the retrieval and generation findings attach to the act of producing the answer, not to reading it. The step that cannot be delegated is the human stating, before opening any summary, what the stage set out to do, what was decided, and why. Comparing that against the AI draft afterwards is my addition as a correction step; Roediger & Karpicke tested recall without feedback, so the cited study does not show a benefit from this comparison.
- Roediger & Karpicke's short-delay result explains why reading feels sufficient: right after reading, restudy looks as good or better. The cost only appears days later, which is exactly when the user reports being lost.
- Applying Cepeda's proportions loosely: if the understanding must hold until the stage-8 report (days to a few weeks away), the 1-week figure of 20-40% suggests re-touching a stage's summary a day or more after writing it, rather than only at the moment of closing. A cheap way to get that spacing is to re-recall the previous stage at the start of the next stage's review. This is an extrapolation from fact-learning experiments, not a tested prescription.
- All four studies used word lists, facts, or prose passages with students. Transfer to "recalling the rationale of my own engineering decisions" is plausible but untested. The user also has an advantage the subjects did not: they took part in the decisions.
- Because Dunlosky rates self-explanation and elaborative interrogation as moderate, phrasing the recall prompts as "why" questions ("why did we choose X over Y?") is better supported than "list what was done".

### Gaps
- I did not read the full text of any of the four papers. All four are reported from abstracts or press summaries relayed by search results. Effect sizes and percentages other than the Cepeda proportions quoted above are deliberately omitted.
- The Cepeda et al. (2006) *Psychological Bulletin* spacing meta-analysis was not retrieved; only the 2008 study is cited here.
- No study found on retrieval practice or spacing applied to software project decision histories, to solo developers, or to humans supervising AI agents.
- No sourced evidence on "the cost of massed review at the end" for project work specifically. The claim rests on the general spacing literature.
- No evidence found on whether reading an AI-generated summary of one's own work behaves like rereading. That equivalence is my inference.

## 5. Archiving a finished scope: how to close a stage so live documents stay short, and what makes an archive summary useful later

### Takeaway
The sourced practices agree on a two-part move: a running log during the work, and at the boundary a derived short report while the finished material is moved out of the active set but kept. I found little sourced guidance on what makes the archive summary itself useful later.

### Cited Findings
- PARA defines Archives as "anything from the previous three categories that is no longer active", with "Projects you've completed or put on hold" as an example; the stated reason to keep them is that you "might want to save for future reference". **[primary, read via fetch tool]** — [Forte Labs, The PARA Method](https://fortelabs.com/blog/para/)
- PRINCE2 separates a running Lessons Log, updated continuously and capturing lessons applicable to the rest of the project or future projects, from a Lessons Report that is derived from the log and typically included in each End Stage Report. **[search summary]** — [prince2.com, How PRINCE2 teaches you to learn from mistakes](https://www.prince2.com/uk/blog/how-prince2-teaches-you-to-learn-from-mistakes)
- A PRINCE2 lessons-log template states lessons should be uniquely identified and should show whether action was taken. **[search summary; exact source page among the results is unclear]** — [projectengineer.net, The 26 project documents of PRINCE2](https://projectengineer.net/the-26-project-documents-of-prince2)
- Keep a Changelog's release step is a freeze-and-move: the top "Unreleased" section is moved into a new dated version section, and "Versions and sections should be linkable." **[primary, read via fetch tool]** — [keepachangelog.com 1.1.0](https://keepachangelog.com/en/1.1.0/)
- Progressive summarization's rule for preserving context under compression: earlier layers stay intact so later summarization does not lose material; "you cannot compress something without losing some of its context". **[primary, read via fetch tool]** — [Forte Labs, Progressive Summarization](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)
- Warning that archives go unread: reviews "result in static reports that are all too often filed away and forgotten". **[primary, read]** — [After Action Review Guide, p.4](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)

### Inferences
- The project already has the "running log" half (decision tables, judgment log). The missing half is the derived stage report and the act of moving closed-stage rows out of what the human scans day to day.
- A workable close for a stage, combining the sources: (1) freeze, meaning the stage's rows stop being edited; (2) write a short rollup that links to row IDs; (3) make the index point to the rollup first and the full rows second. Rows should be moved or collapsed, never deleted, because the assignment grades the reasoning trail and Forte's rule is to keep lower layers.
- Since the decision files are "written for the AI to look up", archiving mainly helps the human. For the AI the rows can stay where they are; only the human-facing entry point needs to shrink.
- What should make a stage rollup useful later, derived from the above rather than directly sourced: stable links to the underlying rows (changelog: linkable), whether each lesson was acted on (PRINCE2 template), the intent the stage started with (AAR question 1), and reversals stated explicitly since those generate most "why did we do that?" questions.
- The "filed away and forgotten" warning is the main risk of adding an archive step alone. It needs to be paired with the recall step in section 4, otherwise it only produces one more document.

### Gaps
- No authoritative source retrieved for the exact required headings of the PRINCE2 End Stage Report or Lessons Log fields. Check the official manual before quoting headings.
- No source found that evaluates what makes an archive summary useful on later re-reading. The criteria above are inference.
- PARA says completed projects go to Archives but gives no procedure for summarizing them at that moment.
- No practitioner report found on archiving decision logs specifically (e.g. ADR "superseded" practice was not researched here).

## 6. Concrete short templates for a stage-end review a solo person can finish in 10-15 minutes

### Takeaway
No source provides a ready-made 10-15 minute solo stage-end template for a human working with an AI agent; the templates below are my synthesis from the AAR questions, the testing/generation findings, Keep a Changelog's structure, and Start/Stop/Continue. The defining feature is ordering: human recalls first, AI draft second, comparison third.

### Cited Findings
- AAR four questions (expected / actual / what went well and what did not, and why / sustain or improve). **[primary, read]** — [After Action Review Guide, pp.8-9](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- AAR hindsight-separating prompts: "Given the information and knowledge we had at the time, what could have been done better?" and "Given the information we have now, what can we do differently?" **[primary, read]** — [After Action Review Guide, p.9](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- 15 minutes is cited as a workable length for an informal review. **[primary, read]** — [After Action Review Guide, p.5](https://www.adi.org/downloads/After-Action-Review-Guide.pdf)
- GTD project check: "ensuring at least one current action item on each". **[primary, read]** — [GTD Weekly Review checklist](https://gettingthingsdone.com/wp-content/uploads/2014/10/Weekly_Review_Checklist.pdf)
- Personal-retro prompt sets: start / do more / keep / do less / drop — [t2informatik](https://t2informatik.de/en/downloads/personal-retro-template/); each section ending in one yes/no decision — [pravinkumar.co](https://www.pravinkumar.co/blog/quarterly-retrospective-solo-webflow-practice-2026). **[search summary]**
- Testing without feedback still beat restudy at a delay, and self-generated items beat read items. **[abstracts relayed by search]** — [Roediger & Karpicke 2006](https://pubmed.ncbi.nlm.nih.gov/16507066/); [Slamecka & Graf 1978](https://andymatuschak.org/prompts/Slamecka1978.pdf)
- Grouped, newest-first, linkable entries; do not use raw commit history. **[primary, read via fetch tool]** — [keepachangelog.com 1.1.0](https://keepachangelog.com/en/1.1.0/)

### Inferences

All three templates are synthesis. The bracketed tag on each line names the source idea it draws on.

**Template A. Stage-end review, human part first (about 10-15 min total)**

```
Stage N review — <date>
[Human, from memory, before opening any document. ~5 min]
1. What this stage was supposed to achieve:            [AAR Q1]
2. What actually came out (result, number if any):     [AAR Q2]
3. The 2-3 decisions that shaped it, and why each:     [retrieval + self-explanation]
4. One thing we changed our mind on, and what caused it: [AAR Q3]
[Then open the AI draft and compare. ~5 min]
5. What I got wrong or had forgotten:                  [retrieval first; checking against the draft is my addition, not tested in the cited study]
6. Looking back with what we knew then, what should we have done differently?  [AAR Q4, hindsight split]
7. One change to how we work in the next stage (yes/no to adopt):  [Start/Stop/Continue; one decision]
8. Next concrete action:                               [GTD: one current action]
```

**Template B. AI-drafted stage rollup the human compares against (kept short, links to rows)**

```
## Stage N — <name> (closed <date>)
Intent: one sentence.
Outcome: one sentence, with the stored number if there is one.
Decided: 3-5 bullets, each = decision + reason in one line + row ID link.
Changed our mind: bullets, each = from → to + trigger + row ID link.
Ruled out: bullets, each = option + reason + row ID link.
Still open / carried to stage N+1: bullets.
```
Structure follows Keep a Changelog (grouped by type, linkable, newest stage on top); the grouping labels are my adaptation.

**Template C. Minimal version for a small stage or a mid-stage volume checkpoint (about 5 min)**

```
From memory: what are we doing right now, and why this instead of the alternative?
From memory: what is the most recent thing we decided against?
Check against HANDOFF.md / latest closing comment. What did I miss?
```

Notes on use:
- The human part (lines 1-4 of A) must be written or spoken before the AI draft is shown, otherwise it becomes rereading. The AI can ask the questions one at a time and withhold its draft until the answers are in.
- For spacing, begin stage N+1's review by answering line 3 of Template A again for stage N before starting on N+1.
- A process change adopted at line 7 changes how the project works, so under the project's own rules it needs a decision row with its reason.
- Line 5 has a second use for this assignment: a recurring mismatch between the human's recall and the record is itself a finding worth a row in the judgment log.
- The existing per-issue closing comments already cover "what/why/what changed/what remains"; these templates should not be added per issue. They belong at the stage boundary.
- The project currently postpones the human-readable process summary to stage 8. Template B, produced per stage, would make the stage-8 summary an assembly of existing rollups rather than a first reading of all rows.

### Gaps
- None of these templates has been tested; the 10-15 minute estimate is an assumption based on the 15-minute informal AAR figure and the number of prompts.
- No source found describing a human-recalls-first protocol for people supervising AI coding agents. This appears to be an unaddressed combination in the material I could retrieve.
- Whether the user prefers writing or speaking the recall, and whether stage boundaries are the right grain given stages vary in size, are project decisions I did not make.
