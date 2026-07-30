# Business Requirements: <system name>

> Fill from the interview transcript. What the interview didn't state goes to
> `open-questions.md`, not here. Numbers, never adjectives. Names picked here are reused
> verbatim in the API, C4, and DDL.

## 1. Goal and metric
One sentence on why this exists, plus how success is measured as a number.

## 2. Scope
In scope / out of scope, as two short lists.

## 3. Roles and actors
Who uses the system, and external systems it talks to. These become C4 actors.

## 4. Functional requirements (FR)
Numbered, one behavior each. Each FR becomes an endpoint or a system flow.

- FR-1
- FR-2

## 5. Use cases (UC)
Main flows, success and failure.

- UC-1: <trigger> -> <steps> -> <result>

## 6. Entities
The nouns. Each becomes a DDL table and an API schema.

- <Entity>: <one line>

## 7. Enums
Closed value sets used by entities.

- <EnumName>: VALUE_A | VALUE_B

## 8. Non-functional requirements (NFR)
As numbers. Latency (p95), throughput (RPS), availability (SLA), volume, retention.

- NFR-1

## 9. Business rules
Constraints that aren't a single endpoint.

## 10. Data sources
Where data comes from: user input, sensors, external systems.

## 11. Interfaces and integrations
External systems, protocols, direction of data.

## 12. Security and access
Who may do what. Authn/authz at the level the interview gave.

## 13. Assumptions
Stated assumptions carried into the design. Anything shaky goes to open questions instead.

## 14. Constraints
Fixed limits: tech, budget, regulatory, deadlines.

## 15. Acceptance criteria
How correctness is judged. The acceptance test the stakeholder would accept.

## 16. Open questions
Pointer to `open-questions.md`. Nothing is guessed inline.
