# This is the Week 2 HW Task of AI201

Show What You Know: The Unofficial Guide, Part 2 — Testing
In the previous unit, you built a system and wrote down what "working" would mean for it. You filed those five criteria before you had any results, which means nobody — including you — knew whether your system would clear them.

In this unit you find out.

You'll run your system against your own criteria, call each one met or missed, work out why the misses happened, fix one thing, and run it again. Same repository, same system, same URL. You're not building anything new.

Missing your own targets does not cost you points. A system that misses every single criterion, with a clear explanation of each miss, earns full marks. What's graded is whether you set a real standard and tested against it honestly. Passing a test unit doesn't open anything up, and failing one doesn't hold you back.

That's worth reading twice, because the instinct in this unit is to make your system look good. Resist it. A criterion quietly loosened until it passes leaves you nothing to diagnose, and the diagnosis is where the points are.


🎯 Goals
By the end of this unit you'll be able to:

Test a system against a standard using repeated trials, not a single lucky run
Judge honestly whether a criterion was met
Trace a failure back to the stage of the pipeline that caused it
Make a change, measure whether it helped, and say so either way

📦 What proves you did the work
Three things, added to the repo you submitted in the previous unit.

A run log — your five criteria, tested three times each, in the format below, with the files it came from committed in results/.
A verdict on every criterion — met or missed, against the target you set in the previous unit.
One improvement, with before and after — the change you made and both sets of results.

✅ Features
Required Features

Run every criterion three times. One run isn't a test. If your criterion names a rate — "4 of 5" — you need enough runs to see whether that rate holds or whether you got lucky once.


A verdict on each of your five criteria. Met or missed, using the target you wrote in the previous unit. Not a new target.


A diagnosis for every miss. Which part of the pipeline caused it, and how. "It got it wrong" isn't a diagnosis.


One improvement, made and measured. Pick something your diagnosis points at, change it, run the test again, and put both results side by side. Options are in Milestone 4.


A written call on what's still broken. What you'd do next, and why you stopped where you did.

Stretch Features
Optional, for extra credit. Say what you're adding in your README before you start.

A second improvement from the Milestone 4 menu, measured the same way.
This unit's stretch list is the one item above. Metadata filtering, conversational memory and a second embedding model were the previous unit's stretch options, and they stay there — adding a feature now would break the one rule below.

⚠️ One rule about changing your system. The only change you make in this unit is your improvement. Your system should look different at the end of the unit because of that change and nothing else. It's the same system, not a second one.

🛠️ Setup
Nothing new to install. You're working in the same fork of the Unofficial Guide starter you submitted in the previous unit, with the same corpus and the same model. Don't fork it again and don't start a fresh repo — the commit history from the previous unit is the thing that proves your criteria existed before your results did.


Open your project folder, activate the virtual environment, and check it still runs:

macOS / Linux

source .venv/bin/activate
python test.py
Windows (PowerShell)

.venv\Scripts\Activate.ps1
python test.py
If test.py fails on something it passed in the previous unit, re-run pip install -r requirements.txt inside the activated environment first. rank-bm25 is already in requirements.txt, so the hybrid-search option in Milestone 4 needs no new install.


Confirm your index is still there — python app.py ask "..." with one of your test questions. If it complains there's no index, run python app.py index again.

RUNNING.md in your repo still has every command, every flag, and the troubleshooting table.

If your system from the previous unit won't run at all, talk to your TF!



## Milestone 1: Run your test
⏰ ~40 min

Run your five test questions against your system three separate times, and write down what happened each time.

Three runs, not one. A system that gets 4 of 5 once and 2 of 5 twice is not a system that gets 4 of 5 — and you can't know which one you have from a single pass.


Run your five questions three times over:

python run_eval.py --label before
It asks each question three separate times with the response cache switched off, so you get three real answers instead of one answer repeated. Everything it saw lands in a file in results/: every question on every run, the best distance each time, whether the gate let it through, and the full answer text. Commit that file — it's your evidence the test actually happened.

It also puts the five questions in OUT_OF_SCOPE through retrieval and the relevance gate and writes what happened under its own heading, so criterion 3 has evidence in the same file as the other four. That part costs no model calls — a question the gate refuses never reaches the model — and it runs them once rather than three times, because retrieval is deterministic and the gate is a comparison against a fixed number.

Running the questions by hand instead is fine. Just make all three passes with no changes in between, and save the actual output rather than reading it and moving on.


Turn that into your run log. The file in results/ has one row per question. The table below has one row per criterion, so this is a step of real work, not a copy-paste: criterion 1 asks how many of your five questions had the answer in the retrieved chunks, and that count is the 4/5 in the example.

If you built scorer.py in class, run_eval.py marks each question pass or fail for you. Without it those cells come out blank and you judge them yourself by reading the answers. Use this format — every test unit in this course uses the same one:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 3/5 | 4/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
Criterion 3 comes out the same in all three columns above, and that's correct rather than lazy — run_eval.py measures the gate in a single deterministic pass, so there is one number and it goes in all three. Criteria that depend on the generated answer are the ones that will move.


Underneath the table, paste the real output for each criterion from one of your runs. Not a description of it — the actual text your system produced. Name the file and function that produced it.

📍 Before you move on

- [x] The run log has all five criteria, three runs each, and pasted output underneath.
- [x] Commit it.

If all three runs came out identical on every criterion, check that you're really re-running rather than reading a cached result.



## Milestone 2: Call each criterion
⏰ ~45 min

Go criterion by criterion and say met or missed, against the target you wrote in the previous unit.

This sounds like the easy part. It's the part people get wrong, because "met" is more comfortable than "missed" and there's always a way to read the numbers generously. Read them plainly instead.


Write MET or MISSED next to each criterion, using the target from the previous unit. If your target said 4 of 5 and your runs came out 4, 3, 4 — that's a miss. The target has to hold, not show up occasionally.


For each one, write a sentence on how you decided. This matters most where it's close.

A note on changing a criterion

Sometimes a criterion turns out to be broken rather than just unmet. That's a real finding and it earns credit — but only one kind of change counts.

✅ This earns points. The criterion couldn't be measured, or measured the wrong thing:

Original: "Retrieval returns relevant chunks for at least 4 of 5 questions." Revised: "For at least 4 of 5 questions, the top three results contain the answer." Why: I couldn't judge "relevant" the same way twice. Two of my questions I scored differently on Monday than on Wednesday. The new version is something I can actually check.

❌ This does not. The criterion was fine; you just missed it:

Original: "Catches out-of-corpus questions 4 of 5 times." Revised: "Catches out-of-corpus questions 2 of 5 times." Why: 2 of 5 turned out to be more realistic for my corpus.

The difference is whether the problem is with the measurement or with the result. A number you missed stays where it is, gets diagnosed, and gets a fix attempted.

If you revise a criterion, leave the original line in place and put the new one underneath with your reason. Never delete or edit the original — the whole point is that someone can see what you said before you knew the answer.
💬 Talk this through

In your breakout: bring the number that surprised you most — good or bad — and say what you expected instead. Then ask whether your verdict sounds right. Someone reading your criterion cold is the fastest way to find out whether it says what you thought it said.

Working on your own? Paste the criterion, the target, your three runs, and your verdict into Claude and ask:

"Here is my criterion, my target, my three runs, and the verdict I reached. Argue the opposite verdict as strongly as you can."

If the argument against you is any good, look again.

📍 Before you move on

- [x] Every criterion has MET or MISSED and a sentence on how you decided.
- [x] No criteria were revised; the original criteria remain unchanged in `criteria.md`.
- [x] Commit.



## Milestone 3: Diagnose every miss
⏰ ~45 min

For each criterion you missed, work out which part of your pipeline caused it.

Your system has five stages — loading, chunking, embedding, retrieval, generation. A failure happens at one of them. The work here is finding which, and saying how.


For each miss, name the stage and the mechanism. The stage alone isn't enough; you need what happened there.

Not a diagnosis:

"Question 3 didn't work."

A diagnosis:

"Question 3 asks about laundry costs. The answer is in one sentence that got split across two chunks, so neither chunk on its own contains it. Retrieval found both halves and neither was enough."


Look for a pattern across your misses. If three of your five questions failed and all three ask about numbers, that's one problem, not three. Patterns are worth more than individual explanations.


If you missed nothing at all, say so — and then say honestly whether your targets were set low. A system that clears every criterion on the first try usually means the criteria were safe, not that the system is excellent. Write down which criterion you'd tighten and to what.

💬 Talk this through

In your breakout: describe one failure your test found — what you asked, what came back — and stop there. Don't say what you think caused it. Let your group guess first. If they land somewhere different from you, that's worth knowing before you write your diagnosis down.

Working on your own? Paste the question and the chunks that came back into Claude and ask:

"Here's a question my system got wrong and the chunks it retrieved. Give me three possible causes at different stages of the pipeline. Don't tell me which is most likely."

Then work out which one it actually was. That part is yours.

🛑 If you're stuck

Can't tell which stage caused a failure? Work backwards. Print the chunks that came back for that question. If the answer isn't in any of them, the problem is before generation. If it's right there in a chunk and the answer still came out wrong, the problem is generation.

That one check separates most failures, and it takes two minutes.

📍 Before you move on

- [x] Every miss has a named stage and a mechanism.
- [x] Commit.



## Milestone 4: Fix one thing and measure it
⏰ ~90 min

Pick one thing your diagnosis pointed at, change it, and run your whole test again.

You're not trying to fix everything. One change, measured properly, is worth more than four changes you can't tell apart.


Pick your improvement. These are the two most likely to move the numbers, and most people should choose one of them:

Hybrid search. Right now you match on meaning only. Add keyword search (BM25) alongside it and combine the two. This usually helps when your questions contain names, numbers, or exact terms that semantic search glides past.

A second chunking strategy. Chunk your documents a different way — different size, different overlap, or split on paragraphs instead of a character count — and run the same test against both.

Or something else your diagnosis points at: tuning the relevance gate, changing top-k, tightening your grounding prompt. If your diagnosis pointed somewhere specific, follow it.


Make the change. One change. If you find yourself fixing three things, stop and pick the one your diagnosis actually named.


Run the full test again — all five criteria, three runs each, same format as Milestone 1.


Put both run logs in your README, before and after, so the difference is visible side by side.


Say whether it helped. If it didn't, say that. A change that made things worse, honestly reported, is worth full credit — and it's more interesting than one that worked. What matters is that you can tell.

💬 Talk this through

In your breakout: before you start building, say which improvement you're making and which failure it's supposed to fix.

If you can't connect the two in one sentence, you're picking a fix because it sounds impressive rather than because your diagnosis pointed at it. Someone else will notice that faster than you will.

Working on your own? Ask Claude:

"I'm going to [your improvement] to fix [your failure]. Tell me why that might not work."

🛑 If you're stuck

Improvement not working after an hour? Keep whatever you have, put both run logs in anyway, and write down what you tried and where it broke.

A failed improvement you can explain is a complete submission. An unfinished one you can't describe isn't.

📍 Before you move on

- [x] Both run logs are in your README.
- [x] You can say in one sentence whether the change helped and how you know.
- [x] Commit.



## Milestone 5: Say what's still broken, and submit
⏰ ~45 min

Finish the write-up and make the call on everything you didn't fix.


Write your What's Still Broken section. For each criterion still missed after your fix: what you'd do about it, and why you stopped where you did. "I ran out of time" is an acceptable reason if it's true — what isn't acceptable is pretending nothing is left.


Add a short What I'd Do Differently note: knowing what you know now, which of your five criteria would you write differently in the next unit, and why?


Update How I Used AI with anything from this unit — especially if you used a model to help spot patterns in your failures.


Check the repo and submit the same URL you submitted in the previous unit.

📍 Before you move on

- [x] Your README has both run logs, a verdict per criterion, your diagnoses, and your call on what's left.
- [x] Same repository URL as in the previous unit.
- [x] Commit.



📬 Submitting your project
Submit the same GitHub repository URL you submitted in the previous unit. Your repo needs these added:

File	What's in it
criteria.md	Unchanged from the previous unit, plus any revisions written underneath the originals with reasons
results/	The run logs from run_eval.py, before and after your improvement
README.md	The six sections below, added to what's already there
—	At least four new commits from this unit
New README sections:

Section	What goes in it
Run Log — Before	Your five criteria, three runs each, in the table format from Milestone 1, with real output pasted underneath
Verdicts	MET or MISSED per criterion, with a sentence on how you decided
Diagnoses	For each miss: the pipeline stage and the mechanism
The Improvement	What you changed, why you picked it, and the Run Log — After in the same format
What's Still Broken	What you'd do about each remaining miss, and why you stopped
What I'd Do Differently	Which of your five criteria you'd write differently in the next unit, and why
Paste everything as text. No screenshots, no video.

Do not delete or recreate your repository. Your commit history from the previous unit is what shows your criteria existed before your results did. If a grade is ever disputed, that history is what settles it.


🗺️ How it's graded
The full breakdown of graded features and points is on the course grading page.

This unit's grade comes from three questions:

Was the system actually run enough times to produce the measure your criteria named?
Were your criteria applied correctly? Not "did you use them" — whether the verdict you reached is the right one given what the runs produced.
Did the improvement make sense, and can you say whether it helped?
Passing your criteria earns nothing. Missing them costs nothing. Points come from criteria that are specific and testable, a test that genuinely happened, and a real diagnosis of each failure.