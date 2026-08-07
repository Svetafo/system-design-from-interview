# Step 6: OpenAPI

> Running example: a **personal trainer** app.

## What it is
The API contract, and the point where the design becomes an executable artifact. YAML is the
source of truth. Human-readable method pages are generated from the YAML, never maintained in
parallel, so they can't drift.

## What goes inside
Four parts, in order:

1. **A method summary** ([`templates/methods-summary.md`](../templates/methods-summary.md))
   that traces each planned endpoint back to an FR or a UC. This is the design step, done
   before any YAML.
2. **The YAML** (OpenAPI 3.1), where each method from the summary becomes a real path, request,
   and response.
3. **A method page per endpoint** ([`templates/method-page.md`](../templates/method-page.md)): the
   document a developer actually works from. Fields, types and status codes are taken from the YAML
   and never invented here. What the page adds is what a contract cannot express: the flow step by
   step, the permission checks, the error handling, the audit events, and a link to the sequence
   diagram for that method.
4. **The generated reference**, produced from the YAML rather than written beside it.

Points 3 and 4 are different documents and it is worth keeping them apart. The reference is
mechanical, so it is regenerated and never edited. The method page is analysis, so it is written and
reviewed by a human. Neither one restates the other.

Tags in the YAML equal the C4 container names from step 5. Schema names equal the entity names
from the requirements.

## What the text looks like
A traceable summary first, then strict YAML.

```
# methods summary
POST /plans     generate a TrainingPlan     <- FR-2, UC-1     tag: Plan API
POST /sessions  log a Session               <- FR-3           tag: Plan API
GET  /plans/{id} read a TrainingPlan        <- FR-2           tag: Plan API
```

```yaml
paths:
  /plans:
    post:
      tags: [Plan API]           # equals the C4 container name
      summary: Generate a TrainingPlan
      responses:
        "201": { $ref: "#/components/schemas/TrainingPlan" }
```

Tags, schema names, and endpoints all come from the [glossary](../templates/glossary.md). Add each new endpoint to the glossary as you define it, so the sequence step reuses the same paths.

Start from [`templates/openapi-skeleton.yaml`](../templates/openapi-skeleton.yaml), which passes
`redocly lint` as it stands: tags already sit where C4 container names go, schema names where
glossary entities go, and enum values where the DDL `CHECK` will repeat them.

## Which diagram
None here, but the API feeds the next step: sequence diagrams use these exact endpoints.

## What does NOT go in
Endpoints with no FR behind them, and schema fields the requirements never mentioned. A field
that "seems useful" but isn't sourced is a proposal in open questions, not a contract line.

The reference is generated, never hand-edited:

```bash
npx @redocly/cli build-docs api.yaml -o api-reference.html
```

Regenerate it after every contract change. If you find yourself editing the output, the change
belongs in the YAML or on the method page instead.

## How to validate
Lint it, don't eyeball it:

```bash
npx @redocly/cli lint api.yaml     # expect 0 errors
```

Then check that every method traces to an FR or UC, every tag is a C4 container, and every
schema is a requirements entity.

## Signs it's good
- `redocly lint` returns 0 errors.
- Every endpoint traces to an FR or UC in the summary.
- Tags equal C4 containers, schemas equal requirement entities.
- The method pages are generated from the YAML, not written by hand.

See this step's output in the example package: [`openapi/`](../example/openapi), the method summary, the linted contract, and the reference generated from it.

Next: [Step 7: Sequence](7-sequence.md).
