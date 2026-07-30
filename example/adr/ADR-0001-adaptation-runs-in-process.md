# ADR-0001: Adaptation runs in-process on write, without a queue

Status: accepted
Date: 2026-07-30

## Context
After every logged Session the remaining weeks of the ACTIVE TrainingPlan must be recalculated
(FR-4), and NFR-6 allows 60 s for it. The recalculation is pure arithmetic over the plan and the
Sessions already stored, with no external call. The team is two people and PostgreSQL is the only
datastore the constraints allow.

## Options

- **A. In-process call inside the write transaction.** `POST /sessions` inserts the Session and
  calls the Adaptation Engine before responding. No new infrastructure, the read that follows is
  always consistent. Costs latency on the write path and couples the response time to adaptation.
- **B. Queue plus worker.** `POST /sessions` publishes an event, a worker adapts the plan. Keeps the
  write fast and survives adaptation failures independently. Costs a broker to run and monitor, and
  introduces a window where a plan is read stale.
- **C. Scheduled batch.** Adapt every plan on a nightly job. Cheapest to write, but a Session logged
  in the morning would not change anything until the next day, which contradicts the point of the
  product.

## Decision
Option A: the Adaptation Engine is called in-process on the write path, inside the same
transaction as the Session insert.

## Consequences
Makes easy: no broker, no worker deployment, no eventual consistency to explain, and a read right
after a write always shows the adapted plan. Makes hard: adaptation time is now inside the
`POST /sessions` latency budget, and a slow adaptation degrades the write. Revisit when adaptation
exceeds roughly 500 ms at p95, or when a second writer needs the same recalculation, whichever comes
first. At that point option B is the natural move and the Adaptation Engine already exists as a
separate container, so only its invocation changes.
