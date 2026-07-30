# API Method Summary: Personal AI Trainer

The design step before any YAML. Each endpoint traces back to an FR or a UC from
[`business-requirements.md`](../business/business-requirements.md), and carries the C4 container it belongs to
as its tag. Written first, then [`api.yaml`](api.yaml) followed it.

| Method | Path | Purpose | Traces to | Tag (C4 container) |
|--------|------|---------|-----------|--------------------|
| POST | /plans | Generate a TrainingPlan from a stated Goal, stored as DRAFT | FR-1, FR-2, UC-1 | Plan API |
| POST | /sessions | Log a completed Session and trigger adaptation of the remainder | FR-3, FR-4, UC-2 | Plan API |
| GET | /plans/{id} | Read a TrainingPlan including its adapted remainder; first read activates it | FR-2, FR-5, UC-3 | Plan API |

## Responses per method

| Method | Success | Failure branches |
|--------|---------|------------------|
| POST /plans | 201 TrainingPlan (DRAFT) | 400 invalid goal, 401 unauthorized, 409 an unfinished plan exists (FR-7, ADR-0002), 504 LLM Provider timeout with nothing stored (UC-4) |
| POST /sessions | 201 Session | 400 invalid payload, 401 unauthorized, 404 no such plan for this User, 409 the plan is not ACTIVE |
| GET /plans/{id} | 200 TrainingPlan | 401 unauthorized, 404 no such plan for this User, nothing disclosed (UC-3) |

## Checks against the rules

- Every row traces to an FR or a UC. There are no untraceable endpoints.
- Every tag equals the C4 container name `Plan API` exactly, as declared in
  [`glossary.md`](../glossary.md) and [`c4/workspace.dsl`](../c4/workspace.dsl).
- Resource and schema names equal the requirement entity names: TrainingPlan, User, Session.
- FR-6 (a plan becomes DONE when its last week completes) has no endpoint on purpose: it is a state
  transition the Adaptation Engine performs, not an API operation. It appears in the DDL as a
  `plan_status` value and in the requirements, and that absence is deliberate rather than missed.

## Not in the contract

The Adaptation Engine and the Database are C4 containers but not API tags: nothing calls them from
outside. That is why the glossary lists three Containers while the contract carries one tag.
