# Step 4: ADR (Architecture Decision Records)

> Running example: a **personal trainer** app.

## What it is
A short record for each real fork in the design. When step 2 hit a choice with genuine
alternatives, you didn't freeze and you didn't stall, you parked it. Now each parked fork
becomes one ADR, so the decision is visible and its reasons survive.

## What goes inside
Use [`templates/ADR.md`](../templates/ADR.md). Four parts, always:

- **Context.** What forces the decision, and what constraints bound it.
- **Options.** The real alternatives, each with a trade-off.
- **Decision.** Which one, stated plainly.
- **Consequences.** What this makes easy, and what it makes hard or closes off.

One decision per file, numbered `ADR-0001`, `ADR-0002`, and so on.

## What the text looks like
Compact and honest about the trade-off. The reader should understand the choice without asking
you.

```
# ADR-0001: Plan regeneration, on a schedule vs on demand

Context: the stakeholder said the plan should not "bug people," but also
    should stay current with logged sessions.
Options:
  A. Regenerate on a fixed schedule (weekly). Predictable, may lag reality.
  B. Regenerate on demand when a Session is logged. Fresh, noisier, more compute.
Decision: A, weekly schedule.
Consequences: simpler load, bounded compute. A burst of sessions won't be
    reflected until the next cycle. Revisit if adherence suffers.
```

## Which diagram
None. An ADR is prose. Any diagram it references lives in C4 or sequence.

## What does NOT go in
A decision with no alternative. If there was only one way, it's a requirement or a constraint,
not an ADR. And don't invent a reason after the fact: if the real driver was a stakeholder
constraint, say so.

## How to validate
Every fork parked in `open-questions.md` at step 2 has either an ADR or an answer from a source.
No parked fork is silently dropped.

## Signs it's good
- Each ADR states a real trade-off, not a foregone conclusion.
- The Decision is one sentence a reader can act on.
- Consequences name what the choice costs, not only what it buys.
- The numbering is stable, ADRs are appended, never renumbered.

See this step's output in the example package: [`adr/`](../example/adr), two decisions with real alternatives.

Next: [Step 5: C4](5-c4.md).
