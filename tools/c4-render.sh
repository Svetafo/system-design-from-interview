#!/usr/bin/env bash
# Validate a Structurizr DSL workspace, then render it to C4 PlantUML, PNG and SVG.
# Requires Docker.
#
# Uses the consolidated structurizr/structurizr image. The older structurizr/cli image is
# deprecated upstream and now only prints a migration banner, so it cannot render anything.
#
# Usage: bash tools/c4-render.sh <workspace.dsl> <output-dir>
set -euo pipefail

DSL="${1:?usage: c4-render.sh <workspace.dsl> <output-dir>}"
OUT="${2:?usage: c4-render.sh <workspace.dsl> <output-dir>}"
mkdir -p "$OUT"

# Both containers run as the calling user, otherwise they write output as root and the export fails
# with an access denied on the output directory. That uid has no passwd entry inside the container,
# so the JVM resolves user.home to "?" and PlantUML litters a ./?/.java font cache into the working
# directory; pointing user.home at /tmp keeps the repository clean.
DOCKER_RUN=(docker run --rm --user "$(id -u):$(id -g)"
            -e JAVA_TOOL_OPTIONS=-Duser.home=/tmp
            -v "$(pwd):/work" -w /work)

structurizr() {
  "${DOCKER_RUN[@]}" structurizr/structurizr "$@"
}

# 1. Fail early if the DSL itself is not valid.
structurizr validate -w "$DSL"

# 2. Structurizr DSL -> C4-PlantUML
# The default is the canonical C4-PlantUML look, which is what readers expect from a C4 diagram.
# Note that this exporter ignores element styles declared in the DSL and applies the C4 palette
# instead; use plantuml/structurizr as the third argument if you need your own styles honoured.
FORMAT="${3:-plantuml/c4plantuml}"
structurizr export -w "$DSL" -f "$FORMAT" -o "$OUT"

# 3. PlantUML -> PNG and SVG
for puml in "$OUT"/*.puml; do
  "${DOCKER_RUN[@]}" plantuml/plantuml -tpng "$puml"
  "${DOCKER_RUN[@]}" plantuml/plantuml -tsvg "$puml"
done

echo "Rendered C4 diagrams into $OUT"
