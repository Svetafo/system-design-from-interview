# Toolchain

Everything here validates an artifact with a real tool, so the package is checked, not just
read. Install what you need per artifact.

See it all run against a finished package in [`example/`](../example), including the exact commands
and their output.

## Prerequisites
- **Docker** for C4 rendering, PlantUML and the PostgreSQL check.
- **Node.js** for the OpenAPI linter (`npx`, no global install needed).
- **Python 3** with PyYAML for the consistency gate (`pip install pyyaml`).

## C4 diagrams
```bash
bash tools/c4-render.sh example/c4/workspace.dsl example/c4/diagrams
```
Validates the DSL, exports it to C4-PlantUML, then renders PNG and SVG. Requires Docker.

Notes:
- Uses the consolidated `structurizr/structurizr` image. The older `structurizr/cli` image is
  deprecated upstream and now only prints a migration banner, so it cannot render anything.
- Containers run as the calling user, otherwise the export fails with an access denied while
  writing into the output directory.
- The default format is `plantuml/c4plantuml`, the canonical C4 look. That exporter ignores element
  styles declared in the DSL; pass `plantuml/structurizr` as a third argument if you need your own
  styles applied.

## OpenAPI
```bash
npx @redocly/cli lint example/openapi/api.yaml     # expect 0 errors

# method pages, generated from the contract rather than written beside it
npx @redocly/cli build-docs example/openapi/api.yaml -o example/openapi/api-reference.html
```

## Sequence
```bash
docker run --rm --user "$(id -u):$(id -g)" -e JAVA_TOOL_OPTIONS=-Duser.home=/tmp \
    -v "$(pwd):/work" -w /work plantuml/plantuml -tpng example/sequence/process.puml
```
`--user` keeps the PNG owned by you rather than root, and `user.home` is redirected because that
uid has no passwd entry in the container: without it the JVM writes a `./?/.java` font cache into
your working directory.

## DDL
```bash
docker run --rm -e POSTGRES_PASSWORD=x -d --name sd-pg postgres:16
docker exec -i sd-pg psql -U postgres -v ON_ERROR_STOP=1 < example/db/schema.sql   # expect no errors
docker rm -f sd-pg
```

## Consistency gate (step 9)
```bash
python3 tools/check-consistency.py \
    --glossary example/glossary.md \
    --openapi example/openapi/api.yaml \
    --c4 example/c4/workspace.dsl \
    --sequence example/sequence/process.puml \
    --ddl example/db/schema.sql
```
Runs two passes against the glossary (the single source of names):

- **Conformance:** every name used in an artifact (OpenAPI tags, paths, enums; DDL tables, enums;
  C4 containers; sequence participants and messages) must exist in `glossary.md`.
- **Coverage:** every glossary Endpoint, entity table, and Container must actually appear in the
  artifacts, so nothing is declared but left unbuilt.

`--glossary` is required. Every other input is optional, only the checks whose inputs are present
run. Exit code 0 passes, 1 fails. Pass `--no-coverage` to skip the coverage pass while the package
is still being built one artifact at a time.

Two details of how names are read:
- Convention differences are normalized, so glossary `PlanStatus` matches DDL `plan_status`.
- A C4 container is recognized by the quoted name right after the `container` keyword
  (`api = container "Plan API"`). A container *view* names the software system first
  (`container trainer "Containers"`) and is correctly not treated as a declaration.

## Transcription (step 1)
Not shipped here. Use any speech-to-text tool. Whisper works well for interviews. Compress large
recordings to mono 16 kHz or split them before uploading.
