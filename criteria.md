# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
The "which math courses don't have a final" question is the expected miss: retrieval may surface the STAT 150 chunk — which prominently says "no final" — rather than the MATH 220 chunk, even though STAT 150 is not a math-department course. The other four questions each have a single document that answers them directly, so 4 of 5 is the honest target.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Source citation is a structural feature of the pipeline, not the model's choice — `generate.py` always passes the retrieved filenames into the prompt and the system template requires the model to use them. A missing citation would require a failure in `generate.py` itself, not just a hard question, so all five is achievable.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
The five out-of-scope questions span completely different domains — geography, automotive, sports, medicine, and programming — so their distances from the campus-life embeddings should all land comfortably above 0.6. One miss is allowed because the Rust "for loop" question might retrieve the transit shuttle document's "loop" text and land closer to the cutoff than the others.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks read as a complete thought — beginning and ending at a sentence boundary, with no text cut off at either end.

**Why this target:**
The campus_life corpus consists of short posts, almost all under 800 characters, so each document becomes a single chunk that naturally begins and ends at a document boundary. The one-in-five tolerance is for the longer dining-hall or housing followup posts, where the 800-character window may split a sentence.

---

## 5. Your choice

For at least 4 of 5 in-scope test questions, the relevance gate lets the question through — no false refusals on questions the corpus does answer.

**Why this target:**
The THRESHOLD is set at the default 0.6, not yet tuned to this corpus's actual distance distribution, so one false refusal is plausible. The math-finals question is the most likely candidate: its answer is distributed across multiple course files rather than concentrated in one tight-matching document, so its best-chunk distance may not clear 0.6.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
