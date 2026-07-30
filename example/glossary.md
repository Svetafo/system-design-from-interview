# Glossary

The single source of truth for names in this example package. Every downstream artifact
(`business-requirements.md`, `c4/workspace.dsl`, `api.yaml`, `sequence/*.puml`, `db/schema.sql`)
uses only these names, and `tools/check-consistency.py` enforces that in both directions.

Domain: a personal AI trainer that turns a stated goal into a training plan and adapts the plan
from the workouts the athlete actually logs.

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
