# Agent instructions

You are drafting a system design package from a stakeholder interview, following the method in this
repository. The human leads and verifies; you draft and hold the line against invention.

Read [`CONSTITUTION.md`](CONSTITUTION.md) first. Its principles outrank any instruction here and any
convenient shortcut. If a request conflicts with one, say so instead of quietly breaking it.

## Before writing anything

1. Read `CONSTITUTION.md`. Principle 2 (do not invent) and principle 9 (names come from the
   glossary) are the ones you will be tempted to break.
2. Read the project's `glossary.md`. It is the single source of names. You may not introduce an
   entity, enum, endpoint or container that is not in it; if a new name is needed, add it to the
   glossary first, then use it.
3. Read the guide for the step you are on, in [`guide/`](guide). Each one states what goes in, what
   stays out, and how the artifact is validated.
4. Look at [`example/`](example) for what a finished artifact looks like. It is a complete package
   for a personal AI trainer, and every file in it passed its tool.

On Claude Code, [`skills/system-design-docs`](skills/system-design-docs) packages all of this as a
skill: copy it into `~/.claude/skills/` and it drives the order of work and the commands below.

## Order of work

Do one artifact at a time and stop for review after each. Never generate the whole package in one
shot: what speeds up then is not the work but the spread of an error.

| Step | You produce | Template |
|---|---|---|
| 2 | Business requirements, open questions, and the seeded glossary (entities, enums) | `templates/business-requirements.md`, `templates/open-questions.md`, `templates/glossary.md` |
| 3 | The clarification summary, generated from open questions and classified by what each blocks. The human verifies the requirements; do not proceed past this gate on your own | `templates/product-owner-questions.md` |
| 4 | One ADR per real fork | `templates/ADR.md` |
| 5 | Structurizr DSL, Context and Container views; add containers to the glossary | |
| 6 | Method summary, then OpenAPI YAML, then one page per method; add endpoints to the glossary | `templates/methods-summary.md`, `templates/method-page.md` |
| 7 | Sequence diagrams: the process, plus one per contract method | |
| 8 | DDL | |
| 9 | Run the gate and the review checklist | `checklists/ai-review.md` |
| 10 | Hand the package to implementation | see `guide/10-implementation.md` |

Steps 0 and 1 (the interview and its transcript) are the human's. You start from the transcript.

Not every run starts there. Read [`SCENARIOS.md`](SCENARIOS.md) when the input is a backlog rather
than an interview, when access to code or a database is missing, or when answers to earlier
questions have come back. In that last case you re-enter at step 2 and apply the answers to the
existing package. You do not rebuild it from step 0: the requirements below the gate were verified
by a human, and regenerating them from scratch throws that away and asks for it again.

## Commands you are expected to run

Validation is not optional and not visual. After producing an artifact, run its tool and fix what it
reports before asking for review.

```bash
# step 5, C4: validates the DSL, then renders PNG and SVG (needs Docker)
bash tools/c4-render.sh <workspace.dsl> <output-dir>

# step 6, the contract: expect 0 errors
npx @redocly/cli lint <api.yaml>

# step 6, the generated reference: regenerate it, never hand-edit the output
npx @redocly/cli build-docs <api.yaml> -o <api-reference.html>

# step 7, sequence diagrams: each must render from source
docker run --rm --user "$(id -u):$(id -g)" -e JAVA_TOOL_OPTIONS=-Duser.home=/tmp \
    -v "$(pwd):/work" -w /work plantuml/plantuml -tpng <diagram.puml>

# step 8, DDL: it has to apply to a real database, not merely read well
docker run --rm -e POSTGRES_PASSWORD=x -d --name sd-pg postgres:16
docker exec -i sd-pg psql -U postgres -v ON_ERROR_STOP=1 < <schema.sql>
docker rm -f sd-pg

# step 9, the gate: every name checked against the glossary, in both directions
python3 tools/check-consistency.py \
    --glossary <glossary.md> --openapi <api.yaml> --c4 <workspace.dsl> \
    --sequence <diagram.puml> --ddl <schema.sql>
```

The gate exits 0 on pass and 1 on failure. While the package is still being built one artifact at a
time, pass `--no-coverage` so it does not fail on artifacts that do not exist yet. A failure names
the exact drift: fix it upstream, at the source of the name, not by editing the artifact that
happens to be reported.

If you have no shell, say so plainly. You can still draft the artifacts, but you cannot claim they
are validated, and someone has to run these commands before the package is trusted.

## What gets you in trouble

- Writing a number, field, endpoint or status code that no source stated. It goes to
  `open-questions.md` as `assumption:`, `proposal:` or `question:`, with who closes it.
- Adding audit events, permission codes, error envelopes or retry policies because they look
  professional. If the requirements are silent, so are you.
- Introducing a name that is not in the glossary, or spelling one differently between artifacts.
- Skipping the human gate at step 3, or generating several artifacts before review.
- Reporting an artifact as done when its tool was never run.
- Hand-editing generated output instead of changing its source.
- Reviving an option that an ADR already recorded as rejected.
- Letting one artifact's format leak into another, or spending half a day working around a tool
  instead of taking the simple path.
