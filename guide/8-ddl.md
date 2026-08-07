# Step 8: DDL

> Running example: a **personal trainer** app.

## What it is
The data model as SQL. Every entity from the requirements becomes a table, with real types,
keys, constraints, indexes, and comments. It is checked by applying it to a live database, not
by reading it.

## What goes inside
- One table per requirement entity, named to match (`training_plans`, `sessions`).
- Real types, not `text` for everything. Enums from the requirements become SQL enums or
  constrained columns (`Goal`, `PlanStatus`).
- Primary and foreign keys, `NOT NULL` where the requirement demands it, and comments that
  point back to the requirement.

## What the text looks like
Plain SQL that applies cleanly on PostgreSQL.

```sql
create type plan_status as enum ('DRAFT', 'ACTIVE', 'DONE');
create type goal as enum ('STRENGTH', 'ENDURANCE', 'WEIGHT_LOSS');

create table training_plans (
  id          bigint generated always as identity primary key,
  user_id     bigint not null references users(id),
  goal        goal not null,
  status      plan_status not null default 'DRAFT',
  created_at  timestamptz not null default now()
);
comment on table training_plans is 'FR-2: a plan generated for a user from their goal';
```

The `training_plans` table, the `TrainingPlan` schema, and `POST /plans` are the same entity
seen from three sides.

Table and enum names come from the [glossary](../templates/glossary.md), where each entity lists its snake_case table name, so nothing here is invented.

## Which diagram
None authored here, but an ER diagram falls out of the schema. View it in a GUI such as DBeaver
after the schema applies.

## What does NOT go in
Tables or columns with no requirement behind them, and enum values the requirements never
listed. A speculative column is a proposal in open questions, not a table definition.

## How to validate
Apply it to a real database:

```bash
docker run --rm -e POSTGRES_PASSWORD=x -d --name sd-pg postgres:16
docker exec -i sd-pg psql -U postgres < schema.sql     # expect no errors
```

Then confirm every requirement entity has a table and every enum matches the OpenAPI schema.

## Signs it's good
- The schema applies on PostgreSQL with no errors.
- Every requirement entity is a table, named to match the API schema.
- Enum values equal the OpenAPI enums (checked by `tools/check-consistency.py`).
- Keys and NOT NULL reflect the business rules, and comments trace to FRs.

This is the last authored artifact. Next: the [AI-review checklist](../checklists/ai-review.md)
and the consistency gate.

Start from [`templates/ddl.sql`](../templates/ddl.sql), which applies to PostgreSQL 16 once the
placeholders are replaced.

See this step's output in the example package: [`db/schema.sql`](../example/db/schema.sql), applied to a live PostgreSQL 16.
