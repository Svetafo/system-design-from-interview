---
name: system-design-docs
description: Assembles a system design package from a stakeholder interview, following the method in this repository: business requirements, open questions, glossary, ADRs, C4, OpenAPI with method pages, sequence diagrams and DDL, each validated by its own tool and checked against the glossary by the consistency gate. Use when the user wants design documentation built from an interview or a transcript, mentions C4, OpenAPI, sequence, DDL, ADR or business requirements, or asks to run the pipeline.
---

# System Design Docs

Orchestrates the method in the `system-design-from-interview` repository. The templates, guides and
tools it needs live in that repository, not in this file.

## First: locate the repository

Every path in this skill is written relative to the repository root, and the skill cannot work
without it: the templates are the artifact formats, and `tools/` holds the validators.

Resolve the root once, before anything else, in this order:

1. `$SD_METHOD_REPO`, if the user has set it.
2. The current project, if it *is* the repository (a `CONSTITUTION.md` and a `guide/` next to each
   other at the top level).
3. Ask the user where their clone is. Do not guess a path and do not proceed without one.

If there is no clone, say so and stop. Drafting from memory produces documents in the right shape
with none of the discipline, which is worse than not starting, and the tools in step 5 onward will
not exist. The clone is one command:

```bash
git clone https://github.com/Svetafo/system-design-from-interview
```

Call that root `$REPO` for the rest of this skill and read from it with full paths. Run the shell
commands below from `$REPO` too, since they invoke `tools/` by relative path.

## Read before drafting

- `$REPO/CONSTITUTION.md`, first. Its principles outrank anything in this file.
- `$REPO/AGENTS.md`, the same pipeline in agent-facing form.
- `$REPO/guide/<step>.md` for the step you are on.
- `$REPO/example/`, one complete package, for what a finished artifact looks like.

## Principle

Why before how. Requirements come first, the architecture is derived from them. Hit a real fork and
you do not stall: mark it an ADR candidate, park it, keep moving.

One artifact at a time, with a checkpoint after each. Generating the whole package in one shot
speeds up the spread of an error, not the work.

## Order of work

Steps 0 and 1 belong to the human. You start from the transcript.

When the input is a backlog instead of an interview, or answers to earlier questions have come
back, follow `$REPO/SCENARIOS.md`. Answers re-enter at step 2 and are applied to the existing
package; do not rebuild it from step 0.

1. **Business requirements** (step 2) from `$REPO/templates/business-requirements.md`, 19 sections.
   What the transcript did not settle goes to `$REPO/templates/open-questions.md`, never into the
   requirements. Seed the glossary (`$REPO/templates/glossary.md`) with entities and enums.
2. **Gate** (step 3). Classify every open question by what it blocks (`blocks-package`,
   `blocks-point`, `non-blocking`), write the package state from `$REPO/templates/package-state.md`
   so the folder describes itself to the next session. Draft the clarification summary from
   `$REPO/templates/product-owner-questions.md`, with its recipient-facing block, only when someone
   outside the package answers; when the holder of the package can answer, they answer in the
   register and no summary is made. Then stop: the human verifies the requirements, and
   this gate is not yours to pass. A `blocks-point` question leaves its ID in the artifact where the
   value is missing, never a plausible default.
3. **ADR** (step 4) per fork, from `$REPO/templates/ADR.md`: Context, Options, Decision,
   Consequences.
4. **C4** (step 5), two paths. Default is Structurizr DSL,
   `$REPO/templates/c4-workspace.dsl`, Context and Container views from one model. The canvas path,
   `$REPO/templates/c4.drawio`, exists for when the diagram has to be edited by someone who will not
   read a DSL; it is validated by nothing, so names are kept aligned by hand. See
   `$REPO/guide/5-c4.md` before choosing. On the default path, render:
   ```bash
   bash tools/c4-render.sh <workspace.dsl> <output-dir>
   ```
   Add the container names to the glossary. They become the OpenAPI tags.
5. **OpenAPI** (step 6), in this order: the method summary
   (`$REPO/templates/methods-summary.md`) tracing every endpoint to an FR or UC, then the YAML, then
   a page per method (`$REPO/templates/method-page.md`), then the generated reference:
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
   `$REPO/checklists/ai-review.md`.
9. **Hand off** (step 10), see `$REPO/guide/10-implementation.md`.

Artifacts are written into the user's project, not into `$REPO`. The repository is read-only here:
it supplies the formats and the validators.

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
