# Step 3: The Gate

> Running example: a **personal trainer** app.

## What it is
The human verification of the requirements, and the only step where nothing is drafted. Everything
below derives from this file, so an error here multiplies into every artifact. The gate is also
where the package's incompleteness becomes a plan instead of a feeling: you decide what proceeds,
what waits, and what has to be asked before anything else moves.

## What goes inside
Two jobs, in order.

**Verify what is there.** Every number and every name against its source. A number with no source is
not a fact, it is a `proposal:`. A name that appears in two spellings is two future bugs. An entity
that no source names is an invention.

**Classify what is missing.** Sort every entry in `open-questions.md` by blast radius, because
"unanswered" is not one thing:

| Class | What it is | Effect |
|---|---|---|
| `blocks-package` | goal, metric, system boundary, a core entity | nothing below proceeds |
| `blocks-point` | one number, one field type, one enum value | the package proceeds, that spot stays a marked hole |
| `non-blocking` | wording, a nice-to-have detail | recorded, no effect |

The classification is the gate's real output. Without it the only two options are to stall on
everything or to guess at everything, and both are worse than proceeding with named holes.

## The three outcomes
- **Pass.** No `blocks-package` entries. The package proceeds.
- **Partial.** No `blocks-package` entries, some `blocks-point` ones. The package proceeds along the
  branches that do not depend on an open answer. Each dependent spot carries the question ID
  instead of a value, never a plausible default.
- **Stop.** One or more `blocks-package` entries. Drafting below the gate is wasted work; go get the
  answers first.

A hole in an artifact looks like this, and never like an invented number:

```
NFR-3  p95 response time: TBD (Q-7)
```

The ID is what makes the return trip cheap. Grep for `Q-7` a week later and every spot that the
answer touches is listed for you.

## What the text looks like
The gate produces one document to send outward: the clarification summary,
[`templates/product-owner-questions.md`](../templates/product-owner-questions.md). It is generated
from `open-questions.md`, ordered by class, addressed to whoever can close each item. It leaves the
project. Write it so someone with no context can answer it in a few minutes, in a thread, without
reading the requirements.

## Which diagram
None. The first diagram is C4 at step 5.

## What does NOT go in
Do not close a question by deciding it yourself at the gate. The gate verifies against sources; it
does not become one. If you find yourself picking between real alternatives, that is not a gate
decision, it is an ADR at step 4.

Do not silence a hole by writing a reasonable default into the artifact. A default with no source
reads as fact to everyone downstream, and nobody will ever ask about it again.

## How to validate
- Every number in the requirements traces to a source, or is marked `proposal:`.
- Every entity, enum and endpoint name appears in `glossary.md` exactly once, in one spelling.
- Every entry in `open-questions.md` has a class and a named closer.
- Every `blocks-point` entry has at least one matching marker in an artifact, and every marker in an
  artifact has a matching entry.
- The clarification summary is answerable by its recipient without further explanation.

## Signs it's good
- You can state, in one sentence each, what proceeds, what waits, and who is being asked what.
- The clarification summary is short enough that someone actually answers it.
- Nothing below the gate contains a number you cannot point at a source for.
- A stranger reading the package can tell a decision from a hole at a glance.

When the answers come back, you do not start over. See
[`SCENARIOS.md`](../SCENARIOS.md), scenario C, for the re-entry path.

Next: [Step 4: ADR](4-adr.md), for the forks this step refused to decide.
