# The Method

How to assemble a System Design package from a stakeholder interview in one pass. This is the
narrative version. The per-artifact detail lives in [`guide/`](guide/), the rules the agent
obeys live in [`CONSTITUTION.md`](CONSTITUTION.md).

## The idea in one line
Requirements are extracted from a live conversation, then everything downstream (API, C4,
sequence, DDL) is derived from them, one artifact at a time, each validated by a real tool,
with a human gate on the requirements.

## Principles

1. **Why before how.** Requirements are written before architecture. The API and the data
   model are derived from requirements, not the other way around. An error in the requirements
   multiplies down into every artifact, so the requirements are a gate.
2. **Do not invent.** What the source didn't state doesn't enter an artifact. It goes into the
   open-questions register marked as an assumption. A primary source closes the gap (a contract,
   code, the product owner), never a plausible guess.
3. **Forks go to an ADR.** A real choice (transport, trigger, where the AI runs) is not frozen
   silently and not stalled on. Mark it an ADR candidate, park it, keep going, record it.
4. **A checkpoint after every step.** The package is not generated in one shot. Small,
   reviewable slices, diff each one. Without this, what speeds up is the spread of the error.
5. **Validate with tools.** Every artifact is run through a linter, a schema compiler, a live
   database, or a renderer, not judged by eye.

## Roles
The human leads, owns, and verifies. The agent drafts. The human asks the stakeholder, makes
the architectural calls, and verifies the numbers and names. The agent turns those into
artifacts from templates and holds the "do not invent" line. The human is what gets evaluated,
not the agent.

## The steps

| # | Step | What happens | Output |
|---|------|--------------|--------|
| 0 | Interview | The analyst asks along 6 axes: goal and metric, scenarios, sources, functional, non-functional, acceptance. Recorded. | audio |
| 1 | Transcription | The recording is run through a transcriber (Whisper). Large files are compressed. | `.txt` |
| 2 | Business requirements | The transcript fills the 16-section template. Entities and enums are seeded into the glossary. What isn't in the interview goes to open questions. | `requirements.md`, `open-questions.md`, `glossary.md` |
| 3 | Gate | The human verifies numbers and names, and classifies what is missing by what it blocks. Nothing below proceeds until confirmed. | verified requirements, `product-owner-questions.md` |
| 4 | ADR | Each parked fork is written up as Context, Options, Decision, Consequences. | `adr/ADR-000N.md` |
| 5 | C4 | Context and Containers are derived from the requirements. API tags equal C4 containers. | `Context.png`, `Containers.png` |
| 6 | OpenAPI | A method summary traces to FR and UC first, then YAML as the source of truth. Method pages are generated from the YAML. | `api.yaml` |
| 7 | Sequence | The end-to-end process plus one diagram per method in the contract, each in detail. Same participants and endpoints as C4 and OpenAPI. | `.puml`, `.png` |
| 8 | DDL | The data model: types, keys, constraints, indexes, comments. Checked on a live database. | `schema.sql` |
| 9 | Review | The whole package is checked for consistency, validity, grounding, and coverage. | verdict A to F |
| 10 | Implementation | The package is handed to a coding agent, which plans, breaks into tasks, and builds, with the glossary as the leash. Bridges to any SDD toolchain or runs built-in. | working software |

## Cross-artifact consistency
This is what a review catches first. The same names for entities, fields, and endpoints across
all artifacts. Every FR maps to an endpoint or a system flow. Every requirement entity maps to
a DDL table. OpenAPI tags equal C4 containers. Sequence participants equal C4 containers plus
OpenAPI endpoints. All of these names come from one place, `glossary.md`, so they agree by
construction rather than by luck. Consistency matters more than the polish of any single artifact,
and `tools/check-consistency.py` verifies the artifacts against the glossary in both directions,
conformance (nothing used that is not in the glossary) and coverage (nothing in the glossary left
unbuilt).

## Context engineering, built in
- **Write.** The open-questions register is external memory against hallucination.
- **Isolate.** One artifact at a time, so an error doesn't flow onward.
- **Compress and select.** Templates and the "do not invent" rule are the output format.
- On conflicting sources, name the authoritative one (contract or code), not a circular
  reference to your own analysis.

## When it isn't one pass
The table above reads as a single run from a conversation to working software. Real work enters at
different points: the input is a backlog rather than an interview, or answers to the gate's
questions arrive a week later and the package has to resume without being rebuilt.
[`SCENARIOS.md`](SCENARIOS.md) covers those entry points. The steps do not change; what changes is
where you enter and what you carry in. The one rule worth stating here: when answers come back, you
re-enter at step 2 with the answered summary, never at step 0, because starting over discards the
requirements a human already verified.

## Where the method starts, and why that matters
SDD frameworks assume a specification already exists. This method starts one step earlier, at
step 0, with a conversation where the requirements don't exist yet. Extracting them by asking
is analyst work, and it is the part the tools don't cover.

## Seeing it done
[`example/`](example) is one complete package built by this method for a personal AI trainer:
glossary, business requirements, two ADRs, a Structurizr model with rendered views, an OpenAPI
contract, four sequence diagrams, and PostgreSQL DDL. Every artifact in it passed its own tool, and
the whole package passes the step 9 gate. The commands to reproduce that are in
[`example/README.md`](example/README.md).
