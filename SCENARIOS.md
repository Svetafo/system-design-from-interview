# Scenarios

The method is written as one pass, step 0 to step 10. Real work is rarely one pass: the input is
not always an interview, and answers arrive days after the questions. These are the entry points
and what changes in each. The steps themselves do not change, only where you enter and what you
carry in.

| | Scenario | Enter at | Carry in |
|---|---|---|---|
| A | Interview to package | step 0 | a stakeholder and a recorder |
| B | Tickets instead of an interview | step 0, reading instead of asking | a folder of ticket text |
| C | Resuming after answers arrive | step 2 | the answered clarification summary |
| D | Partial sources | step 0, with the gaps named up front | whatever access you have |

---

## A. Interview to package
The default, described in [`METHOD.md`](METHOD.md). You talk to a stakeholder along the six axes,
transcribe, write requirements, gate, and derive the rest.

This is the only scenario where the requirements have a single source and gaps get closed inside a
single conversation. Every other scenario is this one with a worse input and more round trips.

---

## B. Tickets instead of an interview
The input is a backlog: ticket descriptions, comments, acceptance criteria where they exist. No
stakeholder in the room.

**What changes.** Step 0 becomes reading rather than asking. Step 1 disappears, the text already
exists. Step 2 onward runs unchanged: requirements are written from ticket text the same way they
would be from a transcript, the glossary is seeded from them, and everything unstated goes to
`open-questions.md`.

**What tickets do not contain.** Reliably absent: the goal and its metric, non-functional numbers,
acceptance criteria, and the priority among architectural forks. Tickets record what was decided,
not why or how well. Expect the first gate to be `stop` or a wide `partial`, and expect the first
pass to produce more questions than requirements. That is the correct output for this input, not a
failure of the pass: the questions are what nobody wrote down.

**What raises the yield.** Existing API contracts, the database schema, and message broker configs
are primary sources in the sense of Constitution section 8, and they close name and type questions
that ticket prose never will. If they are available, they belong in step 0 alongside the tickets.

**How the missing part gets collected.** Not by guessing, and not by a second interview either. The
clarification summary from step 3 goes to whoever owns the answers, as a message or a ticket
comment, and comes back answered. It is the same interview, asynchronous, spread over days. Expect
two or three rounds.

---

## C. Resuming after answers arrive
The gate found holes, someone spent a week collecting answers, and now the work resumes. This is the
scenario the linear method does not describe, and the one that decides whether the first pass was
useful or wasted.

**What you carry in.** The clarification summary with its answer column filled and each answer's
source named. Not a verbal recap, not a chat thread: the same file that went out, come back
answered. That file is the input, the way a transcript is the input at step 2.

**Where you re-enter.** Step 2, never step 0. Re-running the whole pipeline from scratch discards
the verified requirements, the gate decisions, and the ADRs, and produces a package that has to be
verified all over again. The instruction is *apply these answers*, not *collect requirements*.

**The order.**

1. Close the answered entries in `open-questions.md`. An answer that opened a real fork becomes an
   ADR at step 4 rather than a line in the requirements.
2. Update the requirements only where the answers touch. Everything else stays as verified.
3. Check whether the glossary moved. This is the one question that predicts the cost of the rest.
4. Regenerate the affected artifacts downstream. Regenerate, do not hand-patch: a contract edited by
   hand and a requirement left behind will disagree silently, and the next pass will overwrite the
   edit anyway.
5. Re-run the gate at step 3 and the consistency check.

**Glossary moved or not.** The cheap test for how much has to be rebuilt:

| The answer | Radius |
|---|---|
| added, renamed or split an entity, enum or endpoint | wide: the glossary changed, everything drawing on that name is regenerated |
| set a number, a rule, or a field type | narrow: one section, one column, one diagram |

Most answers are narrow. That asymmetry is why the first pass is not throwaway work: it built the
frame, and answers land in named slots rather than reopening the design.

**Keep the trail.** Commit at every gate. A week later, `git diff` against the last gate shows
exactly what the answers moved, which is also the honest report of what the round trip bought.

### When the answers come by voice

Writing into a table is not how most people prefer to answer. Talking through the summary out loud
is faster and usually gives more, so treat it as a normal path rather than an exception.

**Nothing detects this on its own.** A recording is not self-describing: you hand it over saying it
is answers to the clarification summary, exactly as a transcript of an interview arrives labelled as
an interview. That statement is the linkage, and it is the human's to make.

**Speak the question id.** Go down the summary in order and start each answer with its id: "Q-2, on
a repeated link...". The id is what attaches an answer to a question without inference. Answers
given without ids have to be matched by meaning, and that is a guess wearing the clothes of a
result.

**Transcribe with the step 1 machinery.** Nothing new is introduced: the same transcriber, the same
rule against smoothing. "A week, I suppose" must survive as "I suppose", because it is a leaning and
not a decision, and it belongs in the register as a `proposal:` rather than in a requirement.

**The transcript is the source, the filled summary is derived from it.** Keep both. The summary
records what was decided; the transcript is what you return to in a month when it turns out the
answer was read one way and meant another. Source column reads "product owner, recording of
<date>".

Three rules keep this honest:

- An answer that cannot be attached to an id with confidence closes nothing. It is reported as
  unmatched and stays open.
- A question that was skipped stays open. Do not infer it from the talk around it.
- Answers beyond what was asked are legitimate, because the product owner is a primary source. They
  enter the requirements with the recording named as their source, which is the reason to keep the
  transcript at all: otherwise a fact appears in the package a week later with no traceable origin.

**Then the human checks the attribution before it goes downstream.** An answer landing on the wrong
question is the failure mode here, and it multiplies exactly like a bad requirement. Verify the
numbers against the audio while you are at it: a misheard fifteen for fifty reaches an NFR and
petrifies there.

From that point the order above applies unchanged, starting at closing the answered entries.

---

## D. Partial sources
Some of what the package needs is out of reach: no database access, no code, a contract nobody can
find, a stakeholder who is unavailable for a month.

**What changes.** Nothing in the method, but the boundary is declared up front instead of
discovered at step 8. Name, before drafting starts, which artifacts cannot be completed and why. A
DDL without access to the real schema is a proposal, and it is marked as one, not presented as a
data model.

**What still gets built.** More than expected. Requirements, the glossary, ADRs for the forks, C4
context, and the method summary rarely depend on the missing access. Build those, mark the rest,
and let the list of blocked artifacts be part of what you hand over.

The failure mode here is not an incomplete package, it is a complete-looking package resting on
invention. An artifact honestly marked as blocked costs nothing later. One quietly filled in costs
whoever builds from it.
