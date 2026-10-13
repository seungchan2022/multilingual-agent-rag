# Capturing decision rationale at decision time and rolling it up for human re-reading

Reading note for the report writer. Each cited line carries one of two verification labels.
- **[fetched]**: I opened the page itself and the wording comes from it.
- **[snippet]**: I saw it only in a search-result summary. The wording may be paraphrased. Do not present it as a verbatim quote without re-checking.

Project facts used for the gap framing. From the assignment brief, not re-measured: 137 commits after about 2 days; `HANDOFF.md` for the next AI session; issue closing comments with a plain-language summary; the human-readable process summary postponed to stage 8.

Project facts I checked in the repository on 2026-10-13 (branch `4-corpus`), label **[repo]**:
- 144 decision rows in four files (`common.md` 66, `stage1-scoring.md` 30, `stage1-questions.md` 25, `stage1-analysis.md` 23) and 14 judgment rows in `judgments.md`. Counted with `grep -c '^| 2026'`.
- Decision table columns are exactly: 날짜 | 결정 | 정한 사람 | 이유. There is no status column, no row number or ID, and no short title column.
- Rows are long: `awk` reports an average row length of about 765 (characters or bytes depending on locale; not normalized).
- Supersession rule in `DECISIONS.md`: "바뀐 결정은 지우지 않고 바뀌기 전의 줄이 있는 파일에 새 줄로 적는다." So the log is already append-only. The old row gets no marker; the reader finds the change by reading on in the same file.
- `DECISIONS.md` lists five cross-file dependencies between changed decisions found by one manual read-through, and says "더 있을 수 있다" (there may be more).
- `DECISIONS.md` is an index of files (what is in each, when to read it), not an index of decisions.

## 1. ADR practice beyond the basics: status, supersession, index pages, roll-ups, failure modes

### Takeaway
ADR guidance agrees on three readability mechanisms: keep each record short, make every record carry a status so a live decision can be told from a dead one, and treat the collection as a "decision log" whose headlines are skimmed. None of the sources I fetched prescribes a periodic digest or roll-up of the log; the only human-facing layer they describe is the headline list, and that list only works when status is kept current.

### Cited Findings

Record length and why (foundational, 2011)
- [fetched] Nygard: "The whole document should be one or two pages long." and "Bite sized pieces are easier for for all stakeholders to consume." — [Nygard 2011, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [fetched] Nygard's argument against big documents: "Large documents are never kept up to date." "Nobody ever reads large documents, either." "Small, modular documents have at least a chance at being updated." — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [fetched] Intended reader: "We will write each ADR as if it is a conversation with a future developer." — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [fetched] Nygard's evidence is anecdotal: "we've had six to ten developers rotate through projects using ADRs" and "All of them have stated that they appreciate the degree of context they received by reading them." — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

Status and supersession
- [fetched] Nygard: a decision may be "proposed", then accepted, and later "it may be marked as "deprecated" or "superseded" with a reference to its replacement." "If a decision is reversed, we will keep the old one around, but mark it as superseded." Reason given: "It's still relevant to know that it was the decision, but is no longer the decision." — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [fetched] AWS: "When the team accepts an ADR, it becomes immutable. If new insights require a different decision, the team proposes a new ADR. When the team accepts the new ADR, it supersedes the previous ADR." States used: Proposed, Accepted, Rejected, Superseded. — [AWS Prescriptive Guidance, ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [fetched] AWS on rejected records: the owner "adds a reason for the rejection to prevent future discussions on the same topic." — [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [fetched] Microsoft (page dated 2026-04-10): "The ADR serves as an append-only log. Don't go back and edit accepted records. If a decision changes, write a new record that supersedes the original and link the two together. This approach preserves the history of your thinking and makes it clear when and why the direction shifted." — [Azure Well-Architected, Maintain an ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] Microsoft ties status to volume: "Tracking status makes the current state of each decision clear, especially as the number of decisions grows." — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] Microsoft adds a field most templates lack: "Record the confidence level of the decision. Sometimes an architecturally significant decision is made with relatively low confidence. Documenting that low confidence status could prove useful for future reconsideration decisions." — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] MADR status line: `status: "{proposed | rejected | accepted | deprecated | … | superseded by ADR-0123"`. Its optional "More Information" section asks the writer to define "if/when it should be re-visited." — [MADR](https://adr.github.io/madr/)
- [fetched] Practitioner (Herrington, engineering leader, 2026-03-23): "when you supersede a decision, you update the old ADR's status in the same PR." "`Deprecated` and `Superseded` save people from following outdated guidance." — [Herrington 2026](https://www.jonoherrington.com/blog/how-to-write-adrs-that-actually-get-used)
- [snippet] UK GDS standard: a replaced ADR must be marked superseded with a status line directly under the heading and a link to the new ADR. — [GDS Way, architecture decisions](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)
- [snippet] Shopware moves superseded ADRs into a separate `/adr/_superseded` directory. — [Shopware ADR 2020-06-25](https://developer.shopware.com/docs/resources/references/adr/2020-06-25-implement-architecture-decision-records)

Decision log / index as the skim layer
- [fetched] AWS: "This collection creates the decision log." "Project members skim the headlines of each ADR to get an overview of the project context. They read the ADRs to dive deep into project implementations and design choices." — [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [fetched] AWS sizes the reading cost of one record: in a review meeting, "On average, 10 to 15 minutes should be enough" to read an ADR. — [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [fetched] MADR on organizing many records: "MADR logs may be categorized ADRs by defining subdirectories and put the ADRs into these folders." Cost: "numbers of ADRs are no longer unique throughout the repository, but locally within a category only." The page describes no index generation and says "There is currently no tooling supporting MADR 3.0.0." — [MADR](https://adr.github.io/madr/)

What deserves a record (volume control at the source)
- [fetched] Microsoft: "Only include choices that affect the system's structure, key quality attributes, or are difficult to reverse." — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] Herrington's threshold: write one if someone will wonder "why did we do it this way?" in six months. Target effort: 10 to 30 minutes to write, 5 minutes to read. — [Herrington 2026](https://www.jonoherrington.com/blog/how-to-write-adrs-that-actually-get-used)

Failure modes
- [fetched] Zimmermann's content anti-patterns (2023): "Fairy Tale" (only pros, no cons), "Free Lunch Coupon" (no consequences documented), "Dummy Alternative", "Sprint" (only one option considered), "Maze" (content drifts off topic), "Mega-ADR" ("A lot of detailed information about the architecture is stuffed into several multi-page ADRs"), "Novel/Epic", "Blueprint or Policy in Disguise" ("The writing style is not that of a journal reporting activities and their outcome"). He also warns: "ADR logs should not turn into epics." — [Zimmermann 2023, ozimmer.ch ADRCreation (page title not confirmed)](https://ozimmer.ch/practices/2023/04/03/ADRCreation.html)
- [fetched] Experience report, real project (2021): the team "ended up with several records (about 60)", never settled what belongs in a record, and got "a wild mix" of philosophy, macro-architecture and unconcluded technology evaluations. A single-page rendering became hard to handle with "40-50 records included." Context sections grew long. Lessons: set boundaries on scope and size; separate micro- from macro-architecture; add a way to verify each record. — [unexist.dev 2021, Learnings from using ADR in a real project](https://blog.unexist.dev/documentation/myself/2021/08/18/learnings-from-using-adr-in-a-real-project.html)
- [fetched] Herrington: "My early ADRs were 3,000+ word documents. Nobody read them." Stale status: "We had ADRs marked "Accepted" that described systems we'd completely replaced." He reports that an outdated ADR cost one new engineer three days of work, and that an ADR written eight months earlier saved about two weeks of migration work. These are one author's self-reported figures. — [Herrington 2026](https://www.jonoherrington.com/blog/how-to-write-adrs-that-actually-get-used)
- [snippet] Action-research study on ADRs in agile teams (2023) reports challenges in "culture and organisation, tacit knowledge, documentation process and tools". — [Chalmers research record](https://research.chalmers.se/en/publication/538920)

Evidence on which template humans read better
- [fetched, abstract only] Nogueira, Silva, Conte (arXiv, 2026-04-30) compared 5 ADR templates (Tyree/Akerman, Nygard, arc42, Y-statements, MADR); the top two went to a controlled experiment with undergraduates, where Nygard's template outperformed MADR on the overall score. Nygard supported concise documentation; MADR supported structural detail. The abstract gives no participant count or score values. — [arXiv 2604.27333](https://arxiv.org/abs/2604.27333)

### Inferences
- The project's decision tables already do what ADR guidance says about capture (decision, who, why), and already follow the append-only rule (changed decisions get a new row; nothing is deleted) [repo]. Do not recommend either.
- Verified gap 1, status: the tables have no status column and the old row is not marked when a later row changes it [repo]. Nygard, AWS, Microsoft, GDS and Herrington all pair append-only with a mark on the old record plus a link to its replacement. The project has the first half only. A reader landing on an old row cannot tell it is no longer the decision without reading the rest of the file, and for cross-file changes without the manually maintained list in `DECISIONS.md`, which itself says it may be incomplete.
- Verified gap 2, headlines: rows have no ID and no short title, and average about 765 in length [repo]. AWS's "skim the headlines" mode has nothing to operate on. `DECISIONS.md` indexes files, not decisions.
- At 140 rows in 2 days the project is far past the density ADR guidance assumes. Microsoft and Herrington both filter at capture time (hard to reverse; "will someone ask why in six months"). The project deliberately records more, for the AI. So the ADR answer is not "record less" but "mark which rows are the few the human must know". This is my inference, not a sourced recommendation.
- The 60-record project's complaint ("a wild mix") suggests that mixing decision sizes in one list is itself what makes a log unreadable, independent of count.
- The template study favors the shorter Nygard form for readers, consistent with every practitioner source here. Treat it as weak evidence: student participants, and I read only the abstract.

### Gaps
- No fetched source prescribes a scheduled re-read or periodic digest of the decision log. AWS, Microsoft, MADR and Herrington describe review only at acceptance time or during code review. I found no ThoughtWorks Tech Radar text or Google guidance on this; I did not fetch either.
- I did not verify log4brains or adr-tools index generation from a primary page. The MADR page does not mention them.
- No source gives a record count at which a decision log stops being readable. The 40-60 figure is one team's report.
- The "ADR graveyard" label appears only in aggregator pages I did not treat as citable.

## 2. Lab notebook / engineering daybook / research log: raw log vs. periodic summary, and cadence

### Takeaway
Notebook conventions separate an append-only daily log from a scheduled re-read: an end-of-session summary, a weekly review that adds clarifications and links between entries, and a monthly pass over everything. The summary is produced by the person re-reading their own raw entries, and the re-read is also placed at the start of the next session.

### Cited Findings
- [fetched, slides read directly] LSU LaACES (course material, rev. 2026-07-15), cadence slide. Daily: "Every day that you are working in the lab on exercises or project development, you should use the lab book as a general log. Document questions, observations, preliminary results, even failures." Weekly: "Review the previous week's entries and add notes/clarifications as needed. Ensure continuity and connectivity between entries. Especially crucial in the second half of the project cycle." Monthly: "Review all entries to date and add notes/clarifications as needed." — [LSU LaACES L01.02 Lab Notebooks](https://laspace.lsu.edu/laaces/wp-content/uploads/2026/08/L01.02-Lab-Notebooks.pdf)
- [fetched] Same source, start-of-session re-read: "Get to the lab at least 15 minutes early and review your lab book: read previous entries to refresh your mind and clean up errors". — [LSU LaACES](https://laspace.lsu.edu/laaces/wp-content/uploads/2026/08/L01.02-Lab-Notebooks.pdf)
- [fetched] Same source, index and titles: a table of contents is created first (6 pages reserved) and "Table of contents up-to-date" is a review checklist item. "The Title should be a meaningful description of activities in the entry", not just a session date. — [LSU LaACES](https://laspace.lsu.edu/laaces/wp-content/uploads/2026/08/L01.02-Lab-Notebooks.pdf)
- [fetched] Same source, append-only with later annotation: "Never, ever, remove a page"; "Do NOT omit any result, no matter how odd"; "Cross out mistakes with a single straight line (allows them to be read afterwards)"; leave space "for future notes and elaborations (initial & date these)". — [LSU LaACES](https://laspace.lsu.edu/laaces/wp-content/uploads/2026/08/L01.02-Lab-Notebooks.pdf)
- [fetched] Same source, content checklist separates plan from what happened: "Plans: tests to run, research to review, questions to answer" and "Realities: deviations from the plan; adjustments". It also says the cumulative notebook exists so its content can be transferred "with relative ease" to lab reports and design documents. — [LSU LaACES](https://laspace.lsu.edu/laaces/wp-content/uploads/2026/08/L01.02-Lab-Notebooks.pdf)
- [snippet] Michigan State Physics 451 (1990s course page): "At the end of each day, make a summary of your accomplishments and unresolved problems as well as your current plans for next time." — [MSU PHY451 Laboratory Notebooks](https://web.pa.msu.edu/courses/1999fall/PHY451/labbook.htm)
- [snippet] Purdue ECE 477 grades weekly summaries as a category separate from entries, and asks for entries at least every 3 days. — [Purdue ECE 477 Project Notebook Guidelines](https://engineering.purdue.edu/ece477/Course/Assignments/Guidelines/Project%20Notebook%20Guidelines.pdf)
- [snippet] The Pragmatic Programmer, 20th Anniversary Edition (2019) has "Topic 22: Engineering Daybooks", opening with engineers who carried paper notebooks. I could only see the section opening. — [O'Reilly preview, Topic 22](https://www.oreilly.com/library/view/the-pragmatic-programmer/9780135956977/f_0041.xhtml)
- [snippet] ML practitioner posts: "Note down a few lines on what progress was made each day"; write what is being tested and why before a long run; "logging is not the work. It's a support system." — [Towards Data Science, lessons learnt working on applied ML research](https://towardsdatascience.com/lessons-learnt-working-on-applied-machine-learning-research-1a7a5059aa75/); [Towards Data Science, this month's ML lessons learned](https://towardsdatascience.com/this-months-machine-learning-lessons-learned/)
- [snippet] `lablog` (PyPI) tracks experiments, code changes and todos and offers a recap for returning to a project after time away. — [lablog on PyPI](https://pypi.org/project/lablog/)

### Inferences
- The notebook cadence scales with project length: daily log, weekly review, monthly full pass, for a semester-long project. This project produces a week's worth of decisions in a day (140 rows in 2 days), so the equivalent trigger is more plausibly "per closed issue" and "per stage" than per calendar week. This rescaling is my inference; no source states it.
- In every notebook source the person who must understand the work is the one who writes the summary or does the re-read. In this project the AI writes both the raw record and the summaries (handoff, issue comment). The notebook practice that has no counterpart in the brief is the human's own scheduled re-read with annotations.
- The project already has an end-of-session summary (`HANDOFF.md`) and a per-issue summary (closing comment). What the notebook model adds on top is the next level up: a review across several entries that checks "continuity and connectivity", which in project terms is a stage-level view.
- "Plans vs. Realities" maps onto the project's existing split between decision tables (what was chosen) and the judgment log (what the result showed). The notebook sources treat deviations from plan as the thing worth re-reading.

### Gaps
- I could not read the Pragmatic Programmer daybook section itself, so its claimed benefits are not cited here.
- All cadence guidance comes from university course material, not from studies comparing cadences. I found no evidence that weekly beats any other interval.
- I found no ML-specific source that formally separates raw run logs from a periodic written summary; the practitioner posts are individual opinion.

## 3. Layering: raw log → per-scope digest → top-level narrative, and which layer is for the human

### Takeaway
The sources describe two layers explicitly, a headline layer that humans skim and a detail layer they open on demand, plus a separate "report" layer that the raw record feeds. I found no source that defines a three-layer scheme for decisions by name, so the middle "per-scope digest" layer is an inference from notebook weekly summaries and course practice.

### Cited Findings
- [fetched] Two reading modes on one log: "Project members skim the headlines of each ADR to get an overview of the project context. They read the ADRs to dive deep". — [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [fetched] Keep the record separate from supporting material: "Avoid making decision records design guides. If more justification or design ideation is available, provide a link to a document as supplemental material, but the decision must be clear and stand alone without that material." — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] The raw notebook is explicitly the source for later human-facing reports: proper documentation "will enable you to transfer information with relative ease to" lab reports and design documents. — [LSU LaACES](https://laspace.lsu.edu/laaces/wp-content/uploads/2026/08/L01.02-Lab-Notebooks.pdf)
- [fetched] Entry titles as the skim layer: a title "should be a meaningful description of activities in the entry", and the table of contents must be kept up to date. — [LSU LaACES](https://laspace.lsu.edu/laaces/wp-content/uploads/2026/08/L01.02-Lab-Notebooks.pdf)
- [snippet] A middle layer exists in course practice: weekly summaries graded separately from raw entries. — [Purdue ECE 477](https://engineering.purdue.edu/ece477/Course/Assignments/Guidelines/Project%20Notebook%20Guidelines.pdf)
- [fetched] "Options considered" is called "the most valuable section" because it prevents re-evaluating rejected options; context should be written "for someone who has zero context on the problem." — [Herrington 2026](https://www.jonoherrington.com/blog/how-to-write-adrs-that-actually-get-used)
- [fetched] Decisions that play out in phases should be logged as separate records per phase: "Break one decision into multiple if an architectural decision is going to result in multiple phases". — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)

### Inferences
- Mapping to the project: raw layer = `decisions/*.md` and `judgments.md` (for the AI); scope digest = issue closing comments (exists, per issue); position = `HANDOFF.md` (exists, but addressed to the next AI session). The missing layer is a human-addressed view above the issue level: one place that answers "where are we and what are the handful of decisions that shaped this stage", updated as stages close rather than written once at stage 8.
- Postponing the narrative to stage 8 is the pattern the notebook sources warn against indirectly: LSU calls the weekly review "especially crucial in the second half of the project cycle", when accumulated entries are largest.
- Because the stage-8 report needs the same narrative, a per-stage digest is not an extra document system; it is the report's process section written incrementally. This satisfies the constraint to extend existing records, but it is my reasoning, not a sourced practice.
- The headline layer only works if headlines exist. The project's rows have no title or ID column [repo], so a human-facing digest cannot simply point at rows; it has to restate the few decisions it selects in a plain sentence each.

### Gaps
- I did not research Amazon narrative memos or Google design-doc "alternatives considered"; both target team review rather than one person's re-orientation, and I have no fetched source for either.
- I found no source describing a named "decision digest" or "state of the project" document format with a template. Any such format in the final report would be a design proposal, not a cited practice.

## 4. Evidence on the cost of reconstructing rationale later vs. capturing it early

### Takeaway
The research names the problem clearly (rationale that is not written down "vaporizes", and "why was it done this way" is among the hardest questions developers ask), and 2026 work argues AI-speed development makes it worse. I found no study that measures the cost of late reconstruction against early capture; the only numbers are single-author anecdotes.

### Cited Findings
- [snippet] Knowledge vaporization is attributed to Jansen and Bosch: documentation records components and connectors but neglects the reasoning behind them, and losing that tacit information is called knowledge vaporization. — [arXiv 2604.27333, related-work text as shown in search](https://arxiv.org/pdf/2604.27333)
- [snippet] Why capture is skipped: architectural documentation "is often considered as a tedious and resource intensive task, that is usually skipped or performed inadequately. As a result the rationale of the architect's decisions gets lost." — [van Heesch & Avgeriou, pattern-driven approach against AK vaporization](https://www.academia.edu/144187842/A_Pattern_driven_Approach_against_Architectural_Knowledge_Vaporization)
- [snippet] After-the-fact recovery methods depend on the architect's tacit knowledge and require researchers "to acquire a deep understanding of the software system"; an expert survey cited there found vaporization "is a problem in practice, even at the individual level." — [Uncovering Architectural Design Decisions, arXiv 1704.04798](https://arxiv.org/pdf/1704.04798)
- [snippet] LaToza & Myers (PLATEAU 2010): 179 professional developers reported 371 hard-to-answer questions, clustered into 21 categories and 94 distinct questions. "The most frequently reported categories dealt with intent and rationale -- what does this code do, what is it intended to do, and why was it done this way?" — [Hard-to-Answer Questions about Code, DOI 10.1145/1937117.1937125](https://www.springerprofessional.de/doi/10.1145/1937117.1937125)
- [fetched] Nygard's claimed benefit, supported only by developer feedback (see section 1): "Developers and project stakeholders can see the ADRs, even as the team composition changes over time." — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [fetched] Microsoft: "A decision that's made but never recorded will likely be forgotten, leading to repeated debates or later changes that unknowingly contradict the original intent." And: "A record without justification loses its value over time as stakeholders can't evaluate whether the decision still applies when circumstances change." — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] Retrospective writing loses options: "By the time you're writing it after the fact, you've forgotten half the options you considered." Self-reported costs: a stale ADR cost one engineer three days; an existing ADR saved about two weeks; a roughly two-hour decision-review meeting versus a 5-minute ADR read. — [Herrington 2026](https://www.jonoherrington.com/blog/how-to-write-adrs-that-actually-get-used)
- [fetched, abstract only] Storey (arXiv, 2026-03-23, v4 2026-04-06) proposes a "Triple Debt Model": technical debt in code, cognitive debt in people, intent debt in externalized knowledge. Cognitive debt is "the erosion of shared understanding across a team"; intent debt is "the absence of externalized rationale that developers and AI agents need to work safely with code." The abstract reports no empirical data. — [arXiv 2603.22106](https://arxiv.org/abs/2603.22106)
- [snippet] Storey first used "cognitive debt" in October 2025 after students using AI in a startup course "had lost track of what features they were trying to build and why." — [LeadDev, AI coding creates two kinds of debt](https://leaddev.com/ai/ai-coding-creates-two-kinds-of-debt-youre-only-measuring-one)

### Inferences
- Storey's split is the most useful lens for this project. The project has very little intent debt: rationale is externalized in 140 rows. The user's pain is cognitive debt: the rationale exists on disk but not in the human's head. More capture does not reduce it. Only the human reading, or being walked through, the record does.
- This means the classic "capture early vs. reconstruct late" trade-off is already settled in the project's favor, and the open cost is a different one: re-reading a large correct record all at once versus in small pieces. I found no study measuring that.
- Herrington's point that retrospective writing loses the rejected options applies to the stage-8 summary too: a narrative written only at the end would be reconstructed from dense tables rather than from fresh understanding.

### Gaps
- No quantified study of reconstruction cost versus early-capture cost. Record this as absent, not as unknown-but-probably-large.
- I did not open the Jansen & Bosch, Tyree & Akerman, Kruchten or Zimmermann academic papers; the vaporization claims above are from search-result text of papers citing them.
- A secondary write-up mentioned an experiment where 77% of an unrestricted-AI group failed a later maintenance task versus 39% of a group required to explain AI code first, and an Anthropic study with a 17% comprehension drop. I could not trace either to a primary source, so they are not cited as findings. If the report wants them, they must be verified first.
- I found no study of a solo developer with an AI agent specifically.

## 5. When volume becomes the problem, and pruning / archiving rules

### Takeaway
Sources handle volume four ways: filter what gets a record, mark status so dead decisions can be skipped, physically separate superseded or categorized records, and keep history append-only rather than deleting. Nobody deletes; the pruning is always of the reader's view, not of the record.

### Cited Findings
- [fetched] Filter at capture: "Only include choices that affect the system's structure, key quality attributes, or are difficult to reverse." — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] Status as the volume tool: "Tracking status makes the current state of each decision clear, especially as the number of decisions grows." — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] Never delete: "we will keep the old one around, but mark it as superseded." — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). "Never, ever, remove a page." — [LSU LaACES](https://laspace.lsu.edu/laaces/wp-content/uploads/2026/08/L01.02-Lab-Notebooks.pdf)
- [fetched] Split by category into subdirectories, at the cost of globally unique numbers. — [MADR](https://adr.github.io/madr/)
- [snippet] Move superseded records to their own directory (`/adr/_superseded`). — [Shopware ADR](https://developer.shopware.com/docs/resources/references/adr/2020-06-25-implement-architecture-decision-records)
- [fetched] Observed breaking points in one project: about 60 records with mixed scope; one rendered page hard to handle at "40-50 records included"; the author did not find a splitting solution. — [unexist.dev 2021](https://blog.unexist.dev/documentation/myself/2021/08/18/learnings-from-using-adr-in-a-real-project.html)
- [fetched] Stale status is worse than volume: records "marked "Accepted" that described systems we'd completely replaced" misled a new engineer for three days. — [Herrington 2026](https://www.jonoherrington.com/blog/how-to-write-adrs-that-actually-get-used)
- [fetched] Low-confidence flag as a re-review selector: documenting low confidence "could prove useful for future reconsideration decisions." — [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [fetched] Size limit per record as volume control: "Watch the word count of an ADR as it evolves." — [Zimmermann 2023](https://ozimmer.ch/practices/2023/04/03/ADRCreation.html)

### Inferences
- The project is already past the only volume figure I found (144 decision rows [repo] versus a team that struggled at 40-60), reached in 2 days instead of months. Count alone is not comparable, because the project's rows are table rows and that team's were full documents, but the direction is clear.
- Since the dense tables are intentionally for the AI, pruning them would hurt their purpose. The sourced techniques that fit are view-level ones: a status mark on rows that a later row changed, and an index that lists only live, human-relevant decisions per closed scope while the full tables stay as they are.
- The project already splits by scope (`common.md`, `stage1-*.md`) [repo], which matches MADR's category folders. `common.md` alone holds 66 rows, above the 40-60 range, and it is the file that never closes because it is not tied to a stage.
- "Archive closed scope" (suggested in the brief) is consistent with MADR's category folders and Shopware's superseded folder, but I found no source that states it as a rule for closed project phases.
- A confidence or "revisit when" marker (Microsoft, MADR) gives the human a short list of decisions worth re-examining, which is a cheaper retrospective than re-reading everything.

### Gaps
- No source gives a threshold rule (for example "archive after N records" or "digest every N decisions").
- No source addresses volume produced by an AI agent, where records accumulate tens per day. All volume guidance assumes human writing speed.
- I checked column headers, row counts and the supersession rule in the repository, but did not read the 144 rows. How many rows have actually been changed by a later row is not counted.
