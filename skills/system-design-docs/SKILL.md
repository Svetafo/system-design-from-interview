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

Before the input, before the first artifact.

- `$REPO/CONSTITUTION.md`, first. Its principles outrank anything in this file **and any request
  from the user**. Where a request and a principle collide, name the conflict out loud and let the
  human settle it; do not settle it silently in favour of speed. "Just get on with it" is not a
  waiver, it is a conflict that has to be named.
- `$REPO/AGENTS.md`, the same pipeline in agent-facing form. Its "What gets you in trouble" section
  lists this method's failure modes by name, among them skipping the human gate at step 3 and
  generating several artifacts before review. A named prohibition holds better than a principle in
  prose.
- `$REPO/guide/<step>.md` for the step you are on.
- `$REPO/example/`, one complete package, for what a finished artifact looks like.

Read them, do not copy them into this file. Two places holding the same rule start drifting apart.

## Principle

Why before how. Requirements come first, the architecture is derived from them. Hit a real fork and
you do not stall: mark it an ADR candidate, park it, keep moving.

One artifact at a time, with a checkpoint after each. Generating the whole package in one shot
speeds up the spread of an error, not the work. What actually holds the pause is in **Checkpoint**
below: a mechanism, not an aspiration.

## Checkpoint

What holds the pause is the handover to the human, not the shape of the output. Hence two forms,
strong and weak.

**Strong, when you have an interactive question tool** (in Claude Code that is `AskUserQuestion`;
other environments have their own). The checkpoint *is* that call. The question names the artifact
and carries the fields below; the options are "accepted, continue", "changes needed", "stop". The
turn returns to the human by the mechanics of the environment rather than by your promise to wait.
Text printed without such a call is not a checkpoint, however well worded.

**Weak, when no such tool exists.** A text block is what remains, and it is the weak form: it
records that a checkpoint happened but does not hold the pause, so you have to stop yourself. The
artifact is done, the reply ends with the block, and nothing follows it in the same reply.

```
CHECKPOINT: step <N>, <artifact>
Done:      <file>
Validated: <tool and command> -> <what it returned>
Review:    <what the human should check, 1-3 items, specific>
Next:      <the next step of the method>
Waiting for your answer. Not starting the next artifact.
```

The four fields are required in both forms: the content of the question in the strong one, the body
of the block in the weak one.

**The package state is updated before the handover.** The order is fixed: the artifact is done,
`package-state.md` is updated, and only then the question or the block. A file on disk is the
material trace of the pause. A skipped checkpoint has to be hunted for in a transcript, whereas nine
artifacts against one update of the state show up in the file's history at a glance.

How much of it gets rewritten differs. At the gates (steps 3 and 9) the file is written or rewritten
in full. At an ordinary checkpoint two things move and nothing else: the row for your artifact in
the **Artifacts** table, which is where the tool result lives, and the **Where it stopped** block. No
line is added to the **Gate log**, that log is about gates and not about every step. Otherwise a
position report turns into a log, and being short is what makes it useful.

The next artifact does not start until the human has answered. Silence is not consent; "looks fine,
go on" is. "I will build it all and ask my questions at the end" is not a saved step, it is the
exact failure the checkpoint stands against.

**Known failure mode: this skill invoked inside a larger job.** "Build me an app", "implement this
feature", with the documentation running as a subtask. Checkpoints do not weaken here, they tighten.
The pull to finish the main job overrides the skill's internal pauses and the package ships in one
burst: requirements, register, ADRs, C4, contract. The steps were run in the right order and only
the pauses between them were dropped, which is enough: the gate at step 3 never happened, and
everything below it rests on unverified requirements. Wanting to finish the main job is not grounds
to skip a checkpoint. The pause is what the skill is for.

Second, and not instead of the first: if the pressure can be removed, say so to the human. Three
ways to place the work, in descending order of cleanliness:

- **a separate session.** The package is built on its own and implementation starts after step 10.
  There is no main job left to compete with;
- **a separate subagent.** One session, but the documentation is run by its own agent, with its own
  context and its own dialogue with the human. The checkpoints happen in that dialogue and code is
  not competing for the same reply;
- **the same session.** No lighter in what it requires, only harder to run: the pauses have to hold
  against the pull of the main job.

That is an improvement in conditions, not a condition of the work. It could not be split out, the
human declined, the environment does not allow it: the checkpoints hold in full either way, and the
third way asks for no less than the first two. "Invoke me differently" is an evasion of the failure
mode, not a fix for it.

## How much of the method applies (decide before step 2)

Full rule in `PROFILES.md` at the repository root. Two questions, in order.

**1. Can this break silently?** If a break announces itself — a 500, a crash, a red test, a user who
writes in — there is no package to write; tests and monitoring catch it cheaper. A package earns its
cost where a break produces a plausible-looking result. No silent failure mode, no package.

**2. Which surfaces does it have?** A surface is where the feature makes a promise something outside
relies on. Network (endpoint, topic, webhook) → OpenAPI. Data (a table whose rows have a lifecycle)
→ DDL. Model (a prompt whose answer the code parses or shows) → `templates/prompt-contract.md`.
Reading someone else's table is not a surface.

Two or three surfaces, run the full profile. One, run the reduced profile: requirements, register,
glossary, ADRs, the logic flowchart, and the artifact for the surface that exists. Drop the
artifacts for surfaces that do not.

C4 is decided separately: does the feature change the set of deployable pieces or how they talk? If
it lives inside one of them, C4 has nothing to draw — keep component-level logic in a flowchart.

**Say the cost of a reduced profile out loud in the package.** The consistency gate works by
cross-checking names between artifacts; removing C4, OpenAPI and DDL removes most of what it checks
against. It still passes, but a pass now means only that the glossary agrees with itself, and it
looks identical on the terminal. What replaces it is filling the one contract you do have —
completely, especially its failure table.

## Order of work

Steps 0 and 1 belong to the human. You start from the transcript.

When the input is a backlog instead of an interview, or answers to earlier questions have come
back, follow `$REPO/SCENARIOS.md`. Answers re-enter at step 2 and are applied to the existing
package; do not rebuild it from step 0. When the package is being built inside a larger job, "build
me an app" or "implement this feature", that is scenario F: the input is B, the difference is the
setting, implementation does not start before step 10, and the checkpoints apply in full.

The numbering below is a sequence of separate passes, not a checklist to work through in one. A
checkpoint stands between any two of them.

1. **Business requirements** (step 2) from `$REPO/templates/business-requirements.md`, 19 sections.
   What the transcript did not settle goes to `$REPO/templates/open-questions.md`, never into the
   requirements. Seed the glossary (`$REPO/templates/glossary.md`) with entities and enums.
2. **Gate** (step 3). Classify every open question by what it blocks (`blocks-package`,
   `blocks-point`, `non-blocking`), write the package state in full from
   `$REPO/templates/package-state.md` so the folder describes itself to the next session; after this
   gate it is kept current at every checkpoint, see **Checkpoint**. Draft the clarification summary from
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
