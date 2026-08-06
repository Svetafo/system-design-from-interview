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
ADR ID here.

## Closing an entry

Answers land here first, whatever route they arrived by. Strike the ID, write what closed it in
`Closes by`, with the date and the source:

```
| ~~Q-12~~ | question | CLOSED | Real size of the archive | Section 12 | Closed 06.08: 234 MB.
  Source: `unzip -l` on a real export |
```

Answering directly in this file is the normal case when the person who can answer is the one
holding the package. Four things hold whether you answer in writing or out loud:

- **"I don't know" closes nothing but is not a wasted answer.** It means nobody knows, which is a
  finding: the entry stays open and usually becomes a risk or an ADR rather than a value.
- **A rough answer stays rough.** "A week, I suppose" is recorded as a `proposal:`, not as a
  decision, so nobody quotes it back as fact later.
- **Answers by voice are a normal route.** Say the entry ID before each answer; the rest is in
  [`SCENARIOS.md`](../SCENARIOS.md), scenario C.
- **More than was asked is welcome**, and enters the requirements with its source named.

When the answers are in, follow scenario C: close here, then apply them to the artifacts.

## When to also write a clarification summary

Only when the person answering is outside the package: a stakeholder, a product owner on another
team, someone who will read a forwarded file and nothing else. Then
[`product-owner-questions.md`](product-owner-questions.md) is generated from this register, carrying
only the entries that person can close, in their language.

If the one who can answer is the one holding the package, do not produce it. Two files with the same
questions is not thoroughness, it is a second place to drift from.
