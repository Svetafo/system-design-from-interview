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
| E | Reverse from code | step 0, reading code instead of asking | a running system and its schema |
| F | Pipeline inside app development | step 0 or 2, depending on the input | a "build me an app" job with the package inside it |

**Who "you" is here.** By default, whoever is running the work: the human brings the input, makes
the decisions and hands the package on; the agent drafts the artifacts and holds the "do not invent"
line. Where the roles diverge, it says so.

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
discovered at step 8. The human names, before drafting starts, which artifacts cannot be completed
and why. A DDL without access to the real schema is a proposal, and the agent marks it as one rather
than presenting it as a data model.

**What still gets built.** More than expected. Requirements, the glossary, ADRs for the forks, C4
context, and the method summary rarely depend on the missing access. The agent builds those and
marks the rest. The human hands the list of blocked artifacts over with the package: it is part of
the result, not an excuse for it.

The failure mode here is not an incomplete package, it is a complete-looking package resting on
invention. An artifact honestly marked as blocked costs nothing later. One quietly filled in costs
whoever builds from it.

## E. Reverse from code

The input is a running system. No stakeholder, no tickets, no transcript: source files, migrations,
a database schema. You are not designing something, you are writing down what already runs.

**What changes.** Step 0 becomes reading code. Step 1 disappears. The glossary is seeded from names
that already exist in the code, not from names that merely seem apt, and every artifact traces to a file and a
line rather than to a requirement.

**What a reverse package does not contain, and why.** Code states what it does. It does not state
what anyone wanted. Everything that is intent has to be left out or asked, never reconstructed:

- **Business requirements.** Absent on purpose. Recovering them after the fact means presenting your
  own reconstruction as a source. If someone later reads them as the original intent, the package
  has done harm.
- **ADRs.** There are no open forks: the decisions were made and are running. Where one looks wrong,
  it goes into the register as a question, not into an ADR that re-litigates it in hindsight.
- **Goal, metric, acceptance criteria.** Not in the code. If they matter, they come from a person,
  which is scenario A or C, not this one.

What a reverse package does contain is the contract and the data model — the two things the code
genuinely asserts — plus sequence diagrams and the register.

**What to expect.** The register fills with findings rather than gaps: places where the code
contradicts its own comments, error paths that collapse into one outcome, names that drift between
layers. That is the payoff of this scenario. Building the artifact forces questions that reading the
code straight through never asks, and the answers are defects.

**Where it ends.** Hand the findings to the backlog as work, not as documentation. A reverse package
is finished when the register is empty of things you can close yourself, not when every step of the
pipeline has been run.

---

## F. Pipeline inside app development

The job is "build me an app" or "implement this feature", and the package is assembled inside it, as
a subtask. The input is ordinary: a written brief, a conversation with the client, sometimes a few
tickets.

**The difference is not the input.** By input this is usually B, occasionally A: the same
requirements written from the same text, the steps unchanged. What differs is the setting. The
documentation competes with the code for the same reply from the agent, and the pull to finish the
main job presses on the pauses between artifacts. This is the only scenario whose failure mode comes
from where the work happens rather than from what was carried in.

**What it looks like when it breaks.** Requirements, register, ADRs, C4 and the contract ship in one
burst, without ever reaching the human. The steps were run in the right order and only the pauses
between them were dropped, which is enough: the gate at step 3 never happened, and everything below
it rests on unverified requirements. The mechanics of the pause are in the Checkpoint section of
[`skills/system-design-docs/SKILL.md`](skills/system-design-docs/SKILL.md).

**Where to place the work.** Three ways, the first two preferable:

- **a separate session.** The package is built on its own and implementation starts after step 10.
  There is no main job left to compete with;
- **a separate subagent.** One session, but the documentation is run by its own agent, with its own
  context and its own dialogue with the human. The checkpoints happen in that dialogue and code is
  not competing for the same reply;
- **the same session.** No lighter in what it requires than the first two, only harder to run: the
  pauses have to hold against the pull of the main job, and they still hold.

**Implementation does not start before step 10.** Code written against unverified requirements gets
reworked together with them, so one error in a requirement is paid for twice: once in the
documentation and once in what was already built from it. What is legitimate earlier is a throwaway
prototype that settles a fork and then becomes an ADR, plus environment setup. Functionality meant
to survive is not.

**When code already exists before the package.** This arrives ready-made: half the app is written
and the documentation was asked for after the fact. Say it out loud, in the package state and to the
human: what is built rests on unverified requirements, and the first gate may well demand rework.
The human decides whether implementation continues in parallel or waits for step 3. What you cannot
do is quietly assemble the package around the existing code. That produces scenario E dressed up as
scenario A: a reconstruction of someone's intent, presented as requirements.
