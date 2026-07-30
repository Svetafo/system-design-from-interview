# Business Requirements: Personal AI Trainer

> Filled from a stakeholder interview. Names here are reused verbatim in the API, C4, and DDL,
> and they all come from `glossary.md`.

## 1. Goal and metric
An athlete states a goal once and gets a training plan that keeps adapting to the workouts they
actually complete, so they do not abandon the plan after the first missed week. Success: 60 percent
of users still log a Session in week 4 after their first plan.

## 2. Scope
In scope: goal intake, plan generation, logging a completed Session, adapting an ACTIVE plan,
reading a plan.
Out of scope: nutrition, wearable device sync, social features, payments, coach marketplace.

## 3. Roles and actors
- Athlete: states a goal, logs Sessions, reads plans. The only human actor.
- LLM provider: external system that drafts plan content from the goal and history.

## 4. Functional requirements (FR)

- FR-1: an Athlete creates a TrainingPlan by submitting a Goal.
- FR-2: a generated TrainingPlan is stored with status DRAFT and becomes ACTIVE once the Athlete
  reads it for the first time.
- FR-3: an Athlete logs a completed Session against an ACTIVE TrainingPlan.
- FR-4: after each logged Session the Adaptation Engine recalculates the remaining plan.
- FR-5: an Athlete reads a TrainingPlan by id, including the adapted remainder.
- FR-6: a TrainingPlan becomes DONE when its last week is complete.
- FR-7: a User may have only one unfinished TrainingPlan at a time, counting both DRAFT and ACTIVE.

## 5. Use cases (UC)

- UC-1: Athlete submits Goal STRENGTH -> Plan API asks the LLM provider for a draft -> plan stored
  DRAFT -> plan id returned.
- UC-2: Athlete logs a Session -> Session stored -> Adaptation Engine recalculates the ACTIVE plan
  -> next week adjusted.
- UC-3: Athlete reads a plan that does not belong to them -> refused, nothing disclosed.
- UC-4: LLM provider times out -> generation fails, no partial plan is stored, Athlete may retry.

## 6. Entities

- TrainingPlan: a plan generated for a user from their goal.
- User: the person using the system.
- Session: a completed workout logged by a user.

## 7. Enums

- Goal: STRENGTH | ENDURANCE | WEIGHT_LOSS
- PlanStatus: DRAFT | ACTIVE | DONE

## 8. Non-functional requirements (NFR)

- NFR-1: reading a TrainingPlan responds in 300 ms at p95.
- NFR-2: generating a TrainingPlan responds in 8 s at p95, bounded by the LLM provider.
- NFR-3: 50 requests per second peak, 10 thousand monthly active users at launch.
- NFR-4: availability 99.5 percent monthly for reads.
- NFR-5: Sessions retained 24 months, plans retained for the lifetime of the account.
- NFR-6: adaptation completes within 60 s of a logged Session.

## 9. Business rules

- One unfinished TrainingPlan per User, DRAFT or ACTIVE, enforced in the database, not only in code.
  Generation is refused while an unfinished plan exists, so activation on first read can never collide.
- A Session may only be logged against an ACTIVE plan.
- Adaptation never rewrites a week that is already in the past.
- A DONE plan is immutable.

## 10. Data sources
Athlete input (goal, logged Sessions) and LLM provider output (draft plan content). No sensors, no
third party fitness imports at launch.

## 11. Interfaces and integrations
Athlete client to Plan API over HTTPS, JSON. Plan API to LLM provider over HTTPS, synchronous
request/response, outbound only. Adaptation Engine reads and writes the Database directly.

## 12. Security and access
Bearer token per Athlete. A User may read and write only their own plans and Sessions. Plan content
is not personal health data at launch, so no special regime beyond access control.

## 13. Assumptions

- The Athlete states one goal at a time.
- The LLM provider is reachable from the Plan API network.
- Plan weeks are fixed length, so adaptation changes content, not calendar layout.

## 14. Constraints
PostgreSQL is the only datastore. No queue at launch, adaptation runs in-process on write. Team of
two, so the container count is deliberately small.

## 15. Acceptance criteria

- Submitting a Goal returns a plan id, and reading that id returns a plan whose status moved from
  DRAFT to ACTIVE.
- Logging a Session against an ACTIVE plan changes the remaining weeks and never the past ones.
- A second attempt to generate a plan for a User that already has an unfinished one is refused.
- The consistency gate passes over the whole package.

## 16. Open questions
See [`open-questions.md`](open-questions.md). Nothing above is guessed inline: what the interview did
not state is not stated here. Audit and logging, the DONE trigger, the provider timeout, the error
envelope and data deletion all live there rather than being invented in an artifact.
