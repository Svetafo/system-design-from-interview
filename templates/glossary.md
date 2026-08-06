# Glossary

The single source of truth for names. Every entity, enum, endpoint, and container is named
here once, and every downstream artifact uses only these names. This is what makes consistency
hold by construction instead of by after-the-fact checking: the agent pulls names from this one
file, so drift cannot start.

When feeding this method to an agent, give it the glossary first. Nothing downstream may
introduce a name that is not in this file. If a new name is needed, add it here first.

How it fills up:
- **Entities and Enums** are seeded at step 2 from the requirements.
- **Containers** are added at step 5 (C4).
- **Endpoints** are added at step 6 (OpenAPI).

## Entities
Nouns from the requirements. Each becomes an API schema (same name) and a DDL table (the
snake_case name in parentheses, so the gate does not trip over the naming convention).

- `TrainingPlan` (DDL table: `training_plans`): a plan generated for a user from their goal
- `User` (DDL table: `users`): the person using the system
- `Session` (DDL table: `sessions`): a completed workout logged by a user

## Enums
Closed value sets. Name plus the exact values, matched verbatim in OpenAPI and DDL.

- `Goal`: STRENGTH | ENDURANCE | WEIGHT_LOSS
- `PlanStatus`: DRAFT | ACTIVE | DONE

## Endpoints
API operations, added at step 6. The same paths appear as messages in the sequence diagrams.

- `POST /plans`: generate a TrainingPlan
- `POST /sessions`: log a Session
- `GET /plans/{id}`: read a TrainingPlan

## Containers
Deployable pieces, added at step 5. These names are also the OpenAPI tags and the sequence
participants.

- `Plan API`: generates and serves TrainingPlans
- `Adaptation Engine`: adapts a plan from Sessions and Metrics
- `Database`: PostgreSQL

## External systems
Systems outside the boundary. Not containers, and nothing here is built by this package, but
sequence diagrams talk to them, so they are named once like everything else.

- `LLM Provider`: drafts plan content from a goal and history

## Designing a feature inside a running system
A package for one feature references tables and containers it does not create. Mark those entries
`existing` and the gate keeps them usable everywhere while not demanding a `CREATE TABLE` this
package has no business writing:

```
- `User` (DDL table: `users`, existing): the person using the system
- `Plan API` (existing): already deployed, this feature only adds to it
```

Without the marker the coverage check fails on every table the surrounding system already owns,
which reads like a defect in the package and is not.
