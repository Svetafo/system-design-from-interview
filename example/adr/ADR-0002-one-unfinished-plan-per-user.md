# ADR-0002: One unfinished plan per user is enforced by a partial unique index

Status: accepted
Date: 2026-07-30

## Context
FR-7 requires that a User has at most one unfinished TrainingPlan, counting DRAFT and ACTIVE alike.
Two clients can create or activate plans at the same instant, so the rule has to survive a race, not
only a code path. The rule also has to cover DRAFT rather than ACTIVE alone: a plan becomes ACTIVE on
its first read (FR-2), so if two drafts could exist, reading the second one would collide with a
constraint on a plain GET, a failure the caller can do nothing about. PostgreSQL is the only
datastore available.

## Options

- **A. Application check before writing.** Read the User's plans, refuse if an unfinished one exists.
  Simple and expressive in errors, but a race between two concurrent writes leaves two unfinished
  plans and the database cannot tell that this is wrong.
- **B. Partial unique index in the schema.** `unique (user_id) where status <> 'DONE'`. The database
  refuses the second plan regardless of how many processes try it. Costs a less friendly error
  surface, since the API has to translate a constraint violation into a domain error.
- **C. Serializable transactions around creation and activation.** Correct without a schema change,
  but pushes retry handling into every caller and costs throughput on an otherwise cheap write.

## Decision
Option B: a partial unique index on `training_plans (user_id) where status <> 'DONE'`, with the API
translating the violation into a 409 on plan generation.

## Consequences
Makes easy: the invariant holds under concurrent creation and activation, it is visible in the DDL
where a reviewer expects to find it, and activation on first read cannot fail on a constraint,
because a competing draft can never exist. Makes hard: the Plan API must map a PostgreSQL unique
violation onto a 409 instead of raising its own error first, and a User cannot keep a spare draft
while another plan is in progress, which is a deliberate product limit rather than a technical one.
Revisit if plan statuses stop being a closed set, or if keeping several drafts becomes a wanted
feature; a partial index depends on the exact DONE literal.
