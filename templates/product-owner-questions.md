# Clarification Summary

`open-questions.md` rewritten for one specific reader. Not a second register and not a mandatory
artifact: it exists when the register would not be answerable by the person you need an answer from.

**Forwarding the register itself is fine** when the reader is close to the project and reads
`proposal:`, `blocks-package` and `NFR-3` without effort. Do that, and skip this file.

**Rewrite it here** when they are not: when the register carries entries they cannot close (closed by
code, by a linter, by a measurement), when `Affects` lists artifacts that mean nothing to them, or
when the questions are phrased for the package rather than for a person. Forwarding a register to
such a reader does not save work, it moves the translation onto them, and what usually comes back is
silence.

Whichever you send, it comes back with answers and becomes the input for scenario C in
[`SCENARIOS.md`](../SCENARIOS.md). Keep it as a file rather than letting the answers live in a chat
thread.

Everything from the horizontal rule down goes to the recipient as-is, including the block that
tells them how to answer. They have never read this method and never will: whatever they need to
know has to travel inside the document, because you cannot attach yourself to it.

---

## How to answer this

Someone is designing <what>, and the questions below are what the existing description does not
settle. Nothing gets invented in their place, which is why you are being asked.

**Answer whichever way is faster for you.**

- *In writing:* fill the Answer column. A few words each is enough.
- *By voice:* record a message and go down the list, saying the question number before each answer
  ("Q-2, on a repeated upload..."). The number is what attaches your answer to the right question.

**Four things worth knowing.**

- "I don't know" is a real answer, not a failure. It means nobody knows, which is itself a finding
  and changes what gets designed.
- A rough answer is useful if you say it is rough. "A week, I suppose" gets recorded as a leaning
  rather than a decision, and nobody will later quote it back as a fact.
- Skipping a question is fine. It stays open and comes back.
- Saying more than was asked is welcome. Anything you mention is treated as a source and recorded
  with your name on it.

---

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
