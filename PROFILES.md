# Profiles: how much of the method a feature deserves

`SCENARIOS.md` answers where you enter the method. This file answers how much of it applies once
you are in.

Running all eight steps on every feature is not thoroughness, it is ritual. On a feature that lives
inside one deployable, C4 produces two boxes and a line, and OpenAPI produces one endpoint. Both
steps cost real time and return a diagram nobody consults. The method loses credibility faster from
producing empty artifacts than from producing none.

Two questions decide it. Ask them in order.

---

## Question 1: can this break silently?

If a break announces itself, the package is not where you catch it. A 500, a crash, a red test, a
user who writes in — those are cheaper to catch with tests and monitoring, and you were going to
have those anyway.

A package earns its cost where a break produces a **plausible-looking result**. An answer that
sounds right and was built on half the context. A record written with a cause the model invented. A
job that skipped a third of its work and returned success.

That is the filter for whether to build a package at all. Not size, not risk, not how much of the
code it touches. Silence.

**No silent failure mode → no package.** Write the ticket and move on.

---

## Question 2: which surfaces does it have?

A **surface** is a place where this feature makes a promise that something outside it relies on and
can violate. There are three, and each has exactly one artifact that pins it down.

| Surface | What makes it one | Artifact |
|---|---|---|
| Network | an endpoint, a queue topic, a webhook — something calls it from outside the process | OpenAPI |
| Data | a table whose rows have a lifecycle: created, changed, ended, cleaned up | DDL |
| Model | a prompt whose answer the code parses, stores, or shows to someone | prompt contract |

Reading someone else's table is not a data surface. Owning rows that change state is.

Count the surfaces:

- **Two or three → full profile.** All eight steps.
- **One → reduced profile.** Keep requirements, register, glossary, ADRs, the logic flowchart, and
  the artifact for the surface you have. Drop the artifacts for surfaces that do not exist.
- **Zero → no package.** A refactor that changes no behaviour has no surfaces by construction.

C4 is decided separately, and not by counting surfaces. Ask instead: **does this feature change the
set of deployable pieces, or how they talk to each other?** If it lives entirely inside one of them,
C4 has nothing to draw. Keep the component-level logic in a flowchart instead — a sequence diagram
whose participants are components inside one container is a category error, and the consistency gate
will tell you so.

---

## What the unit is

A feature is **one behaviour with one purpose visible to whoever asked for it**. Not a file, not a
sprint, not a release, not a refactor.

This matters because the wrong unit breaks both questions. "The agent package" is not a feature —
it has every surface and no single purpose, so question 2 says full profile and the package sprawls.
"Renamed a config variable" is not a feature either — no behaviour, no surfaces, and question 1
already sent it to the backlog.

When a candidate resists the two questions, it is usually the wrong unit. Split it until each piece
answers cleanly.

---

## Ordering the queue

When several features qualify, do them in order of **blast radius times silence**.

Blast radius is how much of the product a break touches: a feature that shapes every answer beats
one that runs monthly. Silence is how long a break survives unnoticed. A loud break in the core is
usually already known; a quiet one at the edge is usually not worth the package. The top of the
queue is quiet breaks in the core.

---

## The cost of the reduced profile

Say this out loud in the package, because the reduced profile changes where the guarantee comes
from.

The consistency gate works by cross-checking names between artifacts. Remove C4, OpenAPI and DDL and
you have removed most of what it checks against — it will still pass, but passing now means only
that the glossary does not contradict itself. That is a much weaker claim than a pass in the full
profile, and it looks identical on the terminal.

What replaces it is the obligation to fill the one contract you do have, completely. In a reduced
package that is usually the prompt contract, and specifically its failure table: the rows that read
"not detected", and any two rows that collapse into the same observable outcome. That table is where
a reduced package earns what the gate used to give you.

A reduced profile is not a lighter package. It is the same rigour aimed at fewer surfaces.
