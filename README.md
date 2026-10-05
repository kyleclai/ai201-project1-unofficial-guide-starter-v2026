# The Unofficial Guide

Kyle Clai — corpus: campus_life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.

## What This Does

The Unofficial Guide searches the `campus_life` corpus of 88 student-written
and administrative campus documents. It answers specific questions about
registration, dining hours, housing, courses, and transportation by retrieving
relevant chunks from those documents. Before asking the model to write an
answer, the system checks whether the closest chunk is relevant enough; answers
that pass the gate cite the source document they used.

## Chunking Strategy

**Chunk size:** paragraph-based, 80–397 characters per chunk, 188 average
**Overlap:** 0; chunks follow paragraph boundaries

The `campus_life` corpus contains 88 short forum posts, between 178 and 549
characters. The starter's 800-character window never split these posts, so a
single chunk could contain several unrelated topics. For example,
`housing_innisfree_hall.txt` combines room information, pros and cons, laundry,
and noise.

I split on blank lines so each paragraph becomes a focused chunk. Paragraphs
shorter than 80 characters merge with the next paragraph instead of becoming
an isolated fragment. I also prepend each document title so a paragraph such as
"Laundry costs $1.75 wash" keeps its building or course context. The result is
88 documents becoming 159 chunks, averaging 188 characters, with a shortest
chunk of 103 characters.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_340_exams.txt#1` — produced by: `chunker.py::split_documents`

```
CS 340 Databases — assessment

Start the term project in week three, not week eight; everyone learns this the hard way.
```

**Chunk 3** — source: `course_stat_150_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for STAT 150 Applied Statistics

People keep asking so: 5 to 6 hours a week outside class. That's real time, not optimistic time.
```

**Chunk 4** — source: `housing_aldridge_hall.txt#1` — produced by: `chunker.py::split_documents`

```
Aldridge Hall — what it's actually like

The good: closest building to the science quad, four minutes to a 9am lab.

The bad: the elevator is out roughly one week per semester.
```

**Chunk 5** — source: `housing_morrow_house.txt#3` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like

Laundry costs $1.50 wash, $1.25 dry, coin or card. On noise: loud until about 1am on weekends, no enforced quiet hours.
```

## Sample Answer

**Question:** When does the latest dining hall close?

**Answer:** Based on the provided documents, Halden Hall closes at 7:00pm.

**Source:** `dining_halden_hall.txt` (also mentioned in
`dining_halden_hall_followup.txt`).

The live run's best distance was `0.334`, below the `0.6` cutoff.

**My relevance cutoff:** `0.6`

The five in-scope questions had best distances from `0.3339` to `0.5279`.
The five out-of-scope questions ranged from `0.8246` to `0.9231`, leaving a
clear gap. The `0.6` cutoff let all five in-scope questions through and refused
all five out-of-scope questions.

| Question | In corpus? | Best distance |
|---|---|---|
| When should I register for classes | Yes | 0.4945 |
| When does the latest dining hall close? | Yes | 0.3339 |
| How many campus housing/dorms are there? | Yes | 0.4882 |
| Which math courses don't have a final? | Yes | 0.5279 |
| How often does the campus bus come around? | Yes | 0.3884 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9231 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8477 |
| How do I write a for loop in Rust? | No | 0.8768 |

## How I Used AI

**1.** I asked AI to pressure-test whether my acceptance criteria were specific
enough for another person to test. It helped identify that the chunk criterion
needed an observable target, so I wrote criterion 4 as “at least 4 of 5 sampled
chunks read as a complete thought.”

**2.** I asked AI to inspect the starter chunking behavior and suggest a
strategy for the short `campus_life` posts. The paragraph-splitting suggestion
was useful, but I chose the 80-character merge threshold and title prefix after
reading the documents. I checked the result manually: 159 chunks, with none
shorter than 103 characters.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Gate lets in-scope questions through | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

**Evidence:** `results/run_2026-10-04_2229_before.md`, produced by
`run_eval.py::main`, using `store.py::search`, `gate.py::check`, and
`generate.py::answer_from_chunks`.

Representative baseline output:

```text
Registration times are staggered by credit hours, and popular courses fill in the first two days (advising_registration.txt).
Based on the provided documents, Halden Hall closes at 7:00pm.
I do not have enough information to determine how many campus housing/dorms there are.
I do not have enough information to answer which math courses don't have a final.
The campus shuttle runs a loop every 20 minutes from 7am to 11pm on weekdays, and every 40 minutes on weekends.
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MISSED | Only 3 of 5 questions had an answer-bearing chunk in the baseline top-five results. |
| 2 | Every answer names a source | MISSED | Four of five answers named a source in each run; housing had no source and math cited one only once. |
| 3 | Gate stops out-of-corpus questions | MET | The gate refused all 5 of 5 out-of-scope questions. |
| 4 | Sampled chunks are complete thoughts | MET | All five sampled chunks begin and end at readable document or paragraph boundaries. |
| 5 | Gate lets in-scope questions through | MET | All 5 of 5 in-scope questions passed the 0.6 gate in every run. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

**Criterion 1 — Retrieval and question design:** The baseline top-five results
contained the registration and shuttle answers, but not the Pellew 8:00pm
chunk, an explicit housing count, or a no-final math course. The dining answer
was ranked below the first five, while the housing and math questions ask for
answers that are not stated directly in the retrieved chunks.

**Criterion 2 — Generation and question design:** The model usually cited a
source when it had a concrete answer, but it correctly refused to invent a
housing count and therefore had no source to name. The math answer also
sometimes refused without a source. The grounding prompt does not require a
source line on an information-shortage refusal.

## The Improvement

**What I changed:** Increased `config.TOP_K` from 5 to 8.

**Why I picked it:** The dining retrieval showed the relevant
`dining_pellew_dining_hall.txt` chunk at rank 6, outside the original result
window. This directly targets Criterion 1's retrieval diagnosis.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 4/5 | 4/5 | 5/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Gate lets in-scope questions through | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Evidence:** `results/run_2026-10-04_2247_after.md`, produced by
`run_eval.py::main` after changing only `config.TOP_K`.

Representative after output:

```text
Pellew Dining Hall is open until 8:00pm daily, which is the latest closing time among the dining halls mentioned. Source: dining_pellew_dining_hall.txt
Based on the provided documents, there are five campus housing/dorms mentioned: Aldridge Hall, Tamsin Court, Innisfree Hall, Old Brewhouse, and Calder Annexe.
I do not have enough information to answer which math courses don't have a final.
```

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

The change helped the dining question and made the housing question answerable
once, but it did not reliably improve the criteria: Criterion 1 stayed at 3/5
and Criterion 2 stayed below 5/5. The gate criteria remained perfect at 5/5.
More context was not enough by itself and sometimes added distractors.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

Criterion 1 is still missed because broad or comparative questions do not
consistently retrieve answer-bearing chunks. The next improvement would be
hybrid keyword-plus-semantic search so exact terms such as `no final`, course
names, and dining-hall names receive more weight. I stopped after one change
because Unit 2 requires a measurable before/after comparison.

Criterion 2 is still missed because grounded refusals do not name a source.
The next prompt change would require every response, including an information
shortage response, to include retrieved source filenames when sources exist. I
did not make that second change in this unit.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I would rewrite Criterion 1 to use five questions whose answers are each
explicitly present in a named document. The original criterion combines
retrieval failure with questions whose answers are not stated directly in the
corpus. I would also clarify Criterion 2 as: every non-refusal answer names a
source, and every refusal explains that the retrieved sources lack enough
information.
