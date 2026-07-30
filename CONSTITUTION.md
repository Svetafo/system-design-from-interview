# Constitution

Principles the **agent** must obey across every artifact in this pipeline. This file is
read by the agent, not just by humans, so the discipline lives in the context rather than
in anyone's memory. When a request conflicts with a principle here, the principle wins;
surface the conflict instead of silently breaking it.

## 1. Requirements before architecture
Write the business requirements first. Derive the API and the data model from them, never
the other way around. An error in the requirements multiplies down into every artifact, so
the requirements are a gate, not a draft.

## 2. Do not invent
Whatever the source (stakeholder, transcript, contract, code) did not state does **not**
enter an artifact. It goes into `open-questions.md` marked as an assumption. A gap is
closed by a primary source (a contract, code, or the product owner's answer), never by a
plausible guess.

## 3. Numbers and names carry a source
Every non-functional number (p95, RPS, SLA, volume) and every entity, field, or endpoint
name traces to where it came from. A number with no source is marked `proposal:` and parked
in open questions. It is not stated as fact.

## 4. Forks go to an ADR
When a decision has real alternatives (transport, trigger, where the AI runs), do not
freeze silently and do not stall. Mark it an ADR candidate, park it, keep moving, and
record it as `Context → Options → Decision → Consequences`.

## 5. One artifact at a time, with a checkpoint
Never generate the whole package in one shot. Produce small, reviewable slices and diff
each one. Without this, what speeds up is not the work but the spread of the error.

## 6. Validate with tools, not by eye
Every artifact is run through a real tool: a linter, a schema compiler, a live database, a
renderer. "Looks right" is not validation.

## 7. Consistency over local polish
The same names for entities, fields, and endpoints across all artifacts. Every functional
requirement maps to an endpoint or a system flow. Every requirement entity maps to a DDL
table. OpenAPI tags equal C4 containers. A correct, ugly, consistent package beats six
beautiful documents that disagree.

## 8. Name the primary source on conflict
When sources disagree, state which one is authoritative (the contract or the code) and why.
Never resolve a conflict by circular reference to your own earlier analysis.

## 9. Names come from the glossary
Every entity, enum, endpoint, and container is named once in `glossary.md`, and every artifact
uses only those names. Nothing downstream introduces a name that is not in the glossary; if a new
name is needed, it is added to the glossary first. Read the glossary before writing any artifact.
This is what makes consistency hold by construction, not by after-the-fact checking.

## 10. A rejected option stays rejected
When an option is discarded, record it in the ADR with status rejected and move on. Do not
resurrect it later in a different artifact or a later session because it reads well out of context.
The record of what was refused, and why, is as load-bearing as the decision itself.

## 11. Each artifact keeps its own format
User story rules do not migrate into use cases, and use case prose does not migrate into the
OpenAPI. Every artifact follows its own template, in its own step. Mixing formats produces
documents that look thorough and answer nothing.

## 12. Do not fight the tooling heroically
When a tool resists (an editor, an export, an encoding), take the simple path instead of building a
workaround for half a day. Wrestling with tooling is not analyst work, and the package does not get
better for it. Note the limitation and move on.

## File versioning
One convention per category, never mixed.

- **Working files** (markdown, YAML, DSL inside the project): the current version is the plain name
  with no suffix, such as `api.yaml`. To keep an old one, rename **the old file** into
  `_archive/name_vN` or `_archive/name_YYYY-MM-DD`. Do not add a suffix to the new one.
- **Deliverables handed to someone** (a document sent for review): the version goes in the name,
  such as `name_v2`, and a new version never overwrites the previous file, because the recipient
  needs to see which version they have.
- The invariant: never a new file without a version sitting next to an old file with one.

## Roles
The human leads, owns, and verifies; the agent drafts. The human asks the stakeholder,
makes the architectural calls, and verifies the numbers and names. The agent turns those
into artifacts from templates and holds the "do not invent" line.
