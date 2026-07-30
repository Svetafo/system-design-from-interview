---
name: system-design-docs
description: Assembles a system design package from a stakeholder interview, following the method in this repository: business requirements, open questions, glossary, ADRs, C4, OpenAPI with method pages, sequence diagrams and DDL, each validated by its own tool and checked against the glossary by the consistency gate. Use when the user wants design documentation built from an interview or a transcript, mentions C4, OpenAPI, sequence, DDL, ADR or business requirements, or asks to run the pipeline.
---

# System Design Docs

Orchestrates the pipeline from [`AGENTS.md`](../../AGENTS.md). Read that file and
[`CONSTITUTION.md`](../../CONSTITUTION.md) first: the principles there outrank anything here.

Where things live: guides in [`guide/`](../../guide), templates in
[`templates/`](../../templates), tools in [`tools/`](../../tools), a complete worked package in
[`example/`](../../example). Paths below are relative to the repository root, so run from there. If
you copied this skill into `~/.claude/skills/` and work in another project, ask the user where the
clone is and use the tools from it.

## Principle

Why before how. Requirements come first, the architecture is derived from them. Hit a real fork and
you do not stall: mark it an ADR candidate, park it, keep moving.

One artifact at a time, with a checkpoint after each. Generating the whole package in one shot
speeds up the spread of an error, not the work.

## Order of work

Steps 0 and 1 belong to the human. You start from the transcript.

1. **Business requirements** (step 2) from [`templates/business-requirements.md`](../../templates/business-requirements.md),
   16 sections. What the transcript did not settle goes to
   [`templates/open-questions.md`](../../templates/open-questions.md), never into the requirements.
   Seed [`templates/glossary.md`](../../templates/glossary.md) with entities and enums.
2. **Stop.** The human verifies the requirements. This gate is not yours to pass.
3. **ADR** (step 4) per fork, from [`templates/ADR.md`](../../templates/ADR.md):
   Context, Options, Decision, Consequences.
4. **C4** (step 5) as Structurizr DSL, Context and Container views from one model. Render:
   ```bash
   bash tools/c4-render.sh <workspace.dsl> <output-dir>
   ```
   Add the container names to the glossary. They become the OpenAPI tags.
5. **OpenAPI** (step 6), in this order: the method summary
   ([`templates/methods-summary.md`](../../templates/methods-summary.md)) tracing every endpoint to
   an FR or UC, then the YAML, then a page per method
   ([`templates/method-page.md`](../../templates/method-page.md)), then the generated reference:
   ```bash
   npx @redocly/cli lint <api.yaml>                              # expect 0 errors
   npx @redocly/cli build-docs <api.yaml> -o <api-reference.html>
   ```
   Add the endpoints to the glossary. The reference is generated and never hand-edited; the method
   page is analysis and is written by a human-reviewed pass.
6. **Sequence** (step 7): the end-to-end process, plus one diagram per contract method, each with
   its failure branch. Participants are C4 containers, messages are OpenAPI endpoints.
   ```bash
   docker run --rm --user "$(id -u):$(id -g)" -e JAVA_TOOL_OPTIONS=-Duser.home=/tmp \
       -v "$(pwd):/work" -w /work plantuml/plantuml -tpng <diagram.puml>
   ```
7. **DDL** (step 8). It has to apply to a real database, not merely read well:
   ```bash
   docker run --rm -e POSTGRES_PASSWORD=x -d --name sd-pg postgres:16
   docker exec -i sd-pg psql -U postgres -v ON_ERROR_STOP=1 < <schema.sql>
   docker rm -f sd-pg
   ```
8. **Gate** (step 9). Every name checked against the glossary, both directions:
   ```bash
   python3 tools/check-consistency.py --glossary <glossary.md> --openapi <api.yaml> \
       --c4 <workspace.dsl> --sequence <diagram.puml> --ddl <schema.sql>
   ```
   Exit 0 passes, 1 fails. Use `--no-coverage` while the package is still being built. A failure
   names the exact drift: fix it at the source of the name. Then walk
   [`checklists/ai-review.md`](../../checklists/ai-review.md).
9. **Hand off** (step 10), see [`guide/10-implementation.md`](../../guide/10-implementation.md).

## The glossary is the source of names

Read it before writing any artifact. Nothing downstream may introduce a name that is not in it; if a
new name is needed, add it to the glossary first, then use it. This is what makes consistency hold
by construction, and it is what the gate enforces.

## Traps from practice

- **Do not fill gaps with plausibility.** No endpoint, error code, field or value in the source
  means it goes to open questions as an assumption, a proposal or a question, with who closes it. A
  gap is closed by a primary source, never by a guess that reads well.
- **Name the source.** Every substantive statement traces to where it came from: the code, the
  contract, the mockup, the product owner's answer. A guess presented as fact is the failure mode
  models are best at.
- **Do not reopen what was rejected.** A discarded option is recorded in an ADR with status
  rejected, and it stays discarded.
- **Do not mix artifact formats.** User story rules do not migrate into use cases or into OpenAPI.
  Each artifact follows its own template, in its own step.
- **Do not invent audit trails, permission codes or error envelopes** because they look
  professional. If the requirements are silent, so are you.
- **Do not fight the tooling heroically.** If a tool resists, take the simple path. Wrestling with
  an editor is not analyst work.
- **`redocly` reporting a failure is not the same as broken YAML.** It is often a style rule.
  Read what it actually says before rewriting the contract.

## Reporting back

Say which tool you ran and what it returned. An artifact whose tool never ran is not done, and
saying otherwise is the one thing that breaks trust in the whole package. If you have no shell,
say so plainly: you can still draft, but you cannot call it validated.
