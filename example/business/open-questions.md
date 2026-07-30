# Open Questions: Personal AI Trainer

External memory against hallucination. Everything the interview did not settle lives here, not
inside an artifact. Each entry says what kind it is and how it will be closed.

Kinds:
- `assumption:` something taken as true to keep moving, needs confirmation.
- `proposal:` a number or a design choice with no source yet, marked so no one reads it as fact.
- `question:` an open point for the product owner or a primary source (contract, code).

| ID | Kind | Statement | Closes by |
|----|------|-----------|-----------|
| Q-1 | question | Audit and logging were never discussed. Which operations must leave an audit trail, who reads it, how long is it kept? Until this is answered no audit event appears in any method page. | Product owner |
| Q-2 | question | What exactly marks a plan DONE? The requirements say "when its last week is complete", but not whether that is a date passing or the last Session being logged. | Product owner |
| Q-3 | proposal | The LLM Provider timeout is not specified. NFR-2 allows 8 s end to end at p95, so the call itself is proposed at 6 s, leaving room for the rest of the request. | Product owner, then an ADR if it constrains the provider choice |
| Q-4 | assumption | The API is versioned in the path (`/v1`), following the server URL in the contract. The interview did not mention versioning. | Product owner |
| Q-5 | question | Error response shape is not defined. A single `{code, message, details}` envelope is the usual choice, but nothing in the interview says so, so the contract currently describes status codes only. | Product owner |
| Q-6 | question | Account deletion and data export were not discussed, though Sessions are kept 24 months. If the product ships in a jurisdiction with a right to erasure, retention and deletion need a decision. | Product owner, legal |
| Q-7 | assumption | An Athlete states one goal at a time, so a plan has exactly one Goal. Carried into the requirements as an assumption in section 13. | Product owner |
| Q-8 | question | What happens to a DRAFT plan that is never read? It occupies the one unfinished plan slot indefinitely (ADR-0002). An expiry may be needed. | Product owner |

When a question turns into a real decision with alternatives, promote it to an ADR and note the ADR
ID here. Q-3 is the closest to that: if the timeout is what dictates the provider, it stops being a
number and becomes a decision.
