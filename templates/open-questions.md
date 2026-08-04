# Open Questions

External memory against hallucination. Everything the interview didn't settle lives here, not
inside an artifact. Each entry says what kind it is, what it blocks, and how it will be closed.

Kinds:
- `assumption:` something taken as true to keep moving, needs confirmation.
- `proposal:` a number or a design choice with no source yet, marked so no one reads it as fact.
- `question:` an open point for the product owner or a primary source (contract, code).

Classes, assigned at the gate (step 3), by what the entry blocks:
- `blocks-package` the goal, the metric, the system boundary, a core entity. Nothing proceeds.
- `blocks-point` one number, one field, one enum value. The package proceeds; that spot stays a
  marked hole carrying this entry's ID.
- `non-blocking` wording or detail. Recorded, no effect on the work.

| ID | Kind | Class | Statement | Affects | Closes by |
|----|------|-------|-----------|---------|-----------|
| Q-1 | assumption | blocks-package | <what you assumed> | <FRs and artifacts the answer changes> | <source, ADR, or PO answer> |
| Q-2 | proposal | blocks-point | <number/choice not sourced> | <NFR-3, api.yaml> | <who confirms> |
| Q-3 | question | non-blocking | <open point> | <where it lands> | <contract / code / PO> |

`Affects` is what makes the return trip cheap: when the answer arrives days later, it lists the
work without re-reading the package. Every `blocks-point` entry also leaves its ID in the artifact
itself, in place of the missing value, never a plausible default:

```
NFR-3  p95 response time: TBD (Q-2)
```

When a question turns into a real decision with alternatives, promote it to an ADR and note the
ADR ID here. When an answer arrives, close the entry here first, then follow scenario C in
[`SCENARIOS.md`](../SCENARIOS.md).
