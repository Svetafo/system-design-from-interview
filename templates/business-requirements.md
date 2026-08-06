# Business Requirements: <system name>

> Fill from the interview transcript. What the interview didn't state goes to
> `open-questions.md`, not here. Numbers, never adjectives. Names picked here are reused
> verbatim in the API, C4, and DDL.

## 1. Document passport
Who wrote this, when, and which version the reader is holding. A requirements document that
travels without this cannot be cited later.

| Date | Version | Author | Change |
|---|---|---|---|
| <DD.MM.YYYY> | 0.1 | <name> | Initial version |

## 2. Context and background
Why this exists at all, in the stakeholder's words rather than the solution's.

- **Problem or need:** <the pain, for the user or the business>
- **Requested by:** <who asked, e.g. the product owner>
- **Why now:** <what changed to make this current>

## 3. Goal and metric
One sentence on what the system gives its user, plus how success is measured as a number.

## 4. Scope
In scope / out of scope, as two short lists.

## 5. Roles and actors
Who uses the system, and external systems it talks to. These become C4 actors.

## 6. Functional requirements (FR)
Numbered, one behavior each. Each FR becomes an endpoint or a system flow.

- FR-1
- FR-2

## 7. Use cases (UC)
Main flows, success and failure.

- UC-1: <trigger> -> <steps> -> <result>

## 8. Entities
The nouns. Each becomes a DDL table and an API schema.

- <Entity>: <one line>

## 9. Enums
Closed value sets used by entities.

- <EnumName>: VALUE_A | VALUE_B

## 10. Non-functional requirements (NFR)
As numbers. Latency (p95), throughput (RPS), availability (SLA), volume, retention.

- NFR-1

## 11. Business rules
Constraints that aren't a single endpoint.

## 12. Data sources
Where data comes from: user input, sensors, external systems.

## 13. Interfaces and integrations
External systems, protocols, direction of data.

## 14. Security and access
Who may do what. Authn/authz at the level the interview gave.

## 15. Assumptions
Stated assumptions carried into the design. Anything shaky goes to open questions instead.

## 16. Constraints
Fixed limits: tech, budget, regulatory, deadlines.

## 17. Risks
What could make this fail, and what it would cost. A risk is not an open question: a question has
an answer someone can give, a risk is a thing that may happen anyway.

| Risk | Impact if it happens | Early sign |
|---|---|---|
| <what may go wrong> | <what it costs> | <what you would see first> |

## 18. Acceptance criteria
How correctness is judged. The acceptance test the stakeholder would accept.

## 19. Open questions
Pointer to `open-questions.md`. Nothing is guessed inline.
