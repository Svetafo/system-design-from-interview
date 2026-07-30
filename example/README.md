# Example package: Personal AI Trainer

A complete design package produced by this method, so you can see the output before running the
pipeline yourself. The domain is deliberately neutral: an athlete states a goal, the system
generates a training plan and adapts it to the workouts actually logged.

Every artifact here was validated with the toolchain, not just written. The commands to reproduce
that are below, and their real output is in [`assets/`](../assets).

## What is in the package

| File | Step | What it is |
|---|---|---|
| [`glossary.md`](glossary.md) | 2 | The single source of names. Everything downstream draws from it. |
| [`business/business-requirements.md`](business/business-requirements.md) | 2 | Goal, scope, FR, UC, NFR as numbers, rules, acceptance criteria. |
| [`business/open-questions.md`](business/open-questions.md) | 2 | What the interview did not settle, kept out of the artifacts on purpose. |
| [`adr/`](adr) | 4 | Two decisions with real alternatives and consequences. |
| [`c4/workspace.dsl`](c4/workspace.dsl) | 5 | One Structurizr model, Context and Container views. |
| [`c4/diagrams/`](c4/diagrams) | 5 | Rendered PNG and SVG, generated from the DSL. |
| [`openapi/methods-summary.md`](openapi/methods-summary.md) | 6 | The design step before the YAML: every endpoint traced to an FR or UC, with its tag. |
| [`openapi/api.yaml`](openapi/api.yaml) | 6 | OpenAPI 3.1 contract, three operations. |
| [`openapi/methods/`](openapi/methods) | 6 | A page per method: parameters, status codes, the sequence diagram, and the flow step by step with error handling. |
| [`openapi/api-reference.html`](openapi/api-reference.html) | 6 | The mechanical reference, generated from the YAML. Never edited by hand. |
| [`sequence/`](sequence) | 7 | Process diagram plus one diagram per contract method, each with its failure branch. |
| [`db/schema.sql`](db/schema.sql) | 8 | PostgreSQL DDL, including the partial unique index from ADR-0002. |

The step numbers match the [guide](../guide). Step 0 (the interview) and step 1 (transcription)
produced the input and are not published here, since a real transcript is personal material.

## Reproduce every check

From the repository root, with Docker running:

```bash
# 5. C4: validate the DSL, then render Context and Containers to PNG and SVG
bash tools/c4-render.sh example/c4/workspace.dsl example/c4/diagrams

# 6. OpenAPI: lint the contract
npx @redocly/cli lint example/openapi/api.yaml    # 0 errors, 0 warnings

# 6b. the method pages are generated from the contract, never maintained in parallel
npx @redocly/cli build-docs example/openapi/api.yaml -o example/openapi/api-reference.html

# 7. Sequence: render every diagram from source
for f in example/sequence/*.puml; do
  docker run --rm --user "$(id -u):$(id -g)" -e JAVA_TOOL_OPTIONS=-Duser.home=/tmp \
    -v "$(pwd):/work" -w /work plantuml/plantuml -tpng "$f"
done

# 8. DDL: apply the schema to a live PostgreSQL 16
docker run --rm -e POSTGRES_PASSWORD=x -d --name sd-pg postgres:16
docker exec -i sd-pg psql -U postgres -v ON_ERROR_STOP=1 < example/db/schema.sql
docker rm -f sd-pg

# 9. The gate: every name checked against the glossary, in both directions
python3 tools/check-consistency.py \
    --glossary example/glossary.md \
    --openapi example/openapi/api.yaml \
    --c4 example/c4/workspace.dsl \
    --sequence example/sequence/process.puml \
    --ddl example/db/schema.sql
```

The gate passes for each of the four sequence diagrams, not only `process.puml`. Swap the
`--sequence` argument to check the others.

## The gate is not decoration

Rename a path, rename a container, change one enum value, and the gate fails with the exact drift,
in both directions: names used but not declared, and names declared but never implemented.

![Consistency gate output](../assets/consistency-gate.png)

That screenshot is the real output of the command above, first on this package, then on a copy with
three names deliberately drifted.

## Notes worth knowing

- **External systems are drawn as actors in the sequence diagrams.** The LLM Provider is not a
  container of this system, so it cannot be a `participant` without failing the gate. PlantUML draws
  an actor figure for it, which is the honest reading: an external party outside the boundary.
- **The C4 exporter ignores element styles from the DSL.** `plantuml/c4plantuml` applies the standard
  C4 palette, which is what readers expect. Pass `plantuml/structurizr` as the third argument to
  `c4-render.sh` if you need your own styles honoured instead.
- **`User` appears in the contract as the plan owner.** Only the owner can read a plan, so returning
  their own record discloses nothing; without that the schema would be an unused component and the
  linter would flag it.
