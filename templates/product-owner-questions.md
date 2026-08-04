# Clarification Summary

The one document the gate sends outward. Generated from `open-questions.md`, addressed to whoever
can close each item, and written so they can answer in a few minutes without opening the package.

This is not an internal register. It leaves the project, as a message or a ticket comment, and it
comes back with the answer column filled. That filled file is the input for scenario C in
[`SCENARIOS.md`](../SCENARIOS.md), so keep it as a file rather than letting the answers live in a
chat thread.

## What is blocked right now

> One sentence: what cannot proceed until these are answered, and what proceeds regardless.
> Someone deciding whether to spend twenty minutes on this reads only this line.

## Blocking the whole package

Answer these first. Nothing is being drafted below them.

| # | Question | Why it matters | What an answer unblocks | Answer |
|---|----------|----------------|-------------------------|--------|
| 1 | <from open-questions, class blocks-package> | <plain language, no artifact jargon> | <what starts moving> | |

## Blocking one spot

The package is proceeding with these left as marked holes. Each one is a placeholder in a document
right now.

| # | Question | Where it lands | Answer |
|---|----------|----------------|--------|
| 2 | <from open-questions, class blocks-point> | <NFR-3, api.yaml> | |

## Worth confirming

No effect on the work, recorded for correctness.

| # | Question | Answer |
|---|----------|--------|
| 3 | <non-blocking> | |

---

Rules for writing it:

- Order by class, and within a class by what moves the most work. A question blocking the gate
  outranks one blocking a single DDL column.
- Ask in the recipient's language, not the package's. "How often should a plan refresh?" beats
  "clarify the trigger semantics for FR-4."
- One question per row, answerable without a meeting.
- Name who each section is for. A question routed to the wrong person comes back as silence, and
  silence looks like a slow method rather than a missing addressee.
- If a question has real alternatives, say so and list them: the answer is then an ADR, not a value.

When the answers arrive, close the entries in `open-questions.md` first, write the ADRs for any
forks, and re-enter at step 2. Do not re-run the pipeline from step 0.
