# Package State: <system name>

The one file that makes a package self-describing. It lives next to the artifacts, in the project
being designed, and it is written at every gate.

Its job: any agent or person opening this folder cold learns, from one file, what method built this,
where the method lives, which step it stopped at, what is blocking, and what happens next. Without
it, every new session starts by re-explaining all of that out loud, and an agent with no state will
help the way it knows how, editing artifacts by hand and drifting from the register.

Keep it short. It is a position report, not a summary of the package.

## Method

- Built with `system-design-from-interview`, following `AGENTS.md` and `CONSTITUTION.md`.
- Clone at: `<path or URL>`
- Scenario: `<A interview | B backlog | C resuming | D partial sources>`, from `SCENARIOS.md`.

## Where it stopped

- **Step reached:** `<n>`, `<name>`
- **Gate verdict:** `<pass | partial | stop>`, as of `<DD.MM.YYYY>`
- **Blocking:** `<question ids, or none>`

## What happens next

<One or two sentences, concrete. Name the action and who does it, not the general procedure.>

**If you are here with answers to the clarification summary:** re-enter at step 2 and apply them to
the existing package. Do not rebuild from step 0, and do not regenerate the requirements from the
sources again: they were verified by a human, and starting over throws that away. The order is in
`SCENARIOS.md`, scenario C.

**If a `blocks-point` value is missing in an artifact,** it carries a question id in place of the
value. Leave it. It is not an oversight, and filling it with something plausible is the one failure
this method exists to prevent.

## Artifacts

| Artifact | File | State |
|---|---|---|
| Requirements | `business-requirements.md` | `<drafted / verified / n/a>` |
| Open questions | `open-questions.md` | `<count open, count closed>` |
| Glossary | `glossary.md` | `<seeded / complete>` |
| Clarification summary | `product-owner-questions.md` | `<sent DD.MM / answered DD.MM / not sent>` |
| ADR | `adr/` | `<parked: ids / written: ids>` |
| C4 | `c4/` | `<not started / rendered>` |
| OpenAPI | `api.yaml` | `<not started / lint clean>` |
| Sequence | `sequence/` | `<not started / rendered>` |
| DDL | `schema.sql` | `<not started / applies on PostgreSQL>` |

## Gate log

One line per gate, newest first. This is what makes the cost of a round trip visible later.

| Date | Step | Verdict | What moved |
|---|---|---|---|
| <DD.MM.YYYY> | 3 | stop | initial pass, <n> questions raised, <n> blocking |
