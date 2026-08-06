# Step 2: Business Requirements

> Running example throughout the guides: a **personal trainer** app. A user sets a fitness
> goal, the system generates a training plan, the user logs sessions, and the AI adapts the
> plan from those sessions and wearable metrics.

## What it is
The first written artifact and the gate for everything below it. It turns the interview
transcript into structured requirements. Everything downstream, the API, C4, sequence, and
DDL, is derived from this file, so an error here multiplies. Nothing proceeds until a human
has verified it (step 3).

## What goes inside
Fill the 19 sections of [`templates/business-requirements.md`](../templates/business-requirements.md).
The load-bearing ones:

- **Goal and metric:** one sentence, plus how success is measured as a number.
- **Roles and actors:** who uses the system.
- **Functional requirements (FR):** numbered, one behavior each. These become endpoints.
- **Use cases (UC):** the main flows, both success and failure.
- **Entities:** the nouns. These become DDL tables and API schemas.
- **Non-functional requirements (NFR):** as numbers, never adjectives.
- **Business rules:** constraints that aren't a single endpoint.

Three more carry the document rather than the design, and they are the ones people drop first:

- **Document passport:** date, version, author. A requirements document that circulates without
  these cannot be cited, and nobody can tell which version they are holding.
- **Context and background:** the problem, who asked, and why now, in the stakeholder's words. The
  goal says what the system does; this says why anyone wanted it.
- **Risks:** what could make this fail and what it would cost. Not the same as an open question: a
  question has an answer someone can give, a risk may happen anyway. Park it with an early sign to
  watch for, not with a mitigation you invented.

## What the text looks like
Plain, numbered, traceable. Each FR is a testable statement, not a paragraph. Names are the
ones you will reuse verbatim in the API and the DDL, so pick them here, once.

```
FR-2  The system generates a TrainingPlan for a User from their Goal.
FR-3  A User logs a completed Session against a Workout.
FR-4  The system adapts the active TrainingPlan from logged Sessions and wearable Metrics.

Entities: User, TrainingPlan, Workout, Exercise, Session, Metric
Enum Goal: STRENGTH | ENDURANCE | WEIGHT_LOSS
Enum PlanStatus: DRAFT | ACTIVE | DONE
```

That `TrainingPlan` you name here is the same one that later becomes `POST /plans`, the
`training_plans` table, and a participant in the sequence diagram. Naming it once is the whole
point.

The entities and enums named here seed the [glossary](../templates/glossary.md), the single list every later artifact draws names from. Nothing downstream invents a name that isn't in it.

## Which diagram
None at this step, because requirements are text. The first diagram is C4 at step 5, derived
from these entities and roles.

## What does NOT go in (it goes to open questions)
Anything the interview didn't state. If the stakeholder never said how often the plan
regenerates, you do not guess "daily." You write it in
[`open-questions.md`](../templates/open-questions.md):

```
Q-4  assumption: plan regenerates on a schedule vs on demand? Not stated in interview.
     Later becomes ADR-0001 (see guide/3).
NFR-1  proposal: adaptation accuracy >= 95% on an acceptance set. Number not sourced, confirm.
```

An NFR number with no source is a `proposal:`, not a fact (Constitution section 3).

## How to validate
Human review, because this is the gate (step 3). Verify every number and every name against
the transcript. Check that each FR is a single, testable behavior and that the entity list has
no duplicates or synonyms. A `Session` and a `Workout` are different things, so keep them
separate. Nothing below this step starts until the requirements are confirmed.

## Signs it's good
- Every FR maps cleanly to a future endpoint or system flow.
- Every entity is a noun you can point at in the transcript.
- Every NFR is a number (p95, RPS, %, volume), not an adjective.
- Everything the interview didn't cover is in open questions, not quietly filled in.
- You could hand this to a stranger and they'd build the same API you would.

See this step's output in the example package: [`business/business-requirements.md`](../example/business/business-requirements.md) and the seeded [`glossary.md`](../example/glossary.md).

Next: [Step 4: ADR](4-adr.md), for the forks this step parked in open questions.
