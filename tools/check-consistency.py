#!/usr/bin/env python3
"""
Glossary-based consistency gate (pipeline step 9).

The glossary (`glossary.md`) is the single source of truth for names. This gate reads it, then
checks that every name used in the other artifacts exists in the glossary. That turns the "same
names everywhere" rule into a membership check against one list, instead of cross-parsing five
formats against each other.

Hard failures (exit 1):
  - an OpenAPI tag that is not a glossary Container
  - an OpenAPI path that is not a glossary Endpoint
  - an OpenAPI or DDL enum whose values differ from the glossary
  - a DDL table that is not a glossary entity table
  - a C4 container that is not in the glossary
  - a sequence participant that is not a glossary Container (actors are allowed)
  - a sequence message path that is not a glossary Endpoint

It also checks coverage in the reverse direction: every glossary Endpoint has an OpenAPI path,
every entity has a DDL table, every Container appears in C4. That catches names declared in the
glossary but never implemented. Pass --no-coverage to skip it while the package is still being
built one artifact at a time.

Warnings (reported, do not fail): an OpenAPI schema name that is not a glossary Entity, since a
real contract may carry request/response wrappers that are not domain entities.

Usage:
  python3 check-consistency.py --glossary glossary.md \
      [--openapi api.yaml] [--c4 c4/workspace.dsl] \
      [--sequence sequence/process.puml] [--ddl db/schema.sql]

--glossary is required. Every other input is optional; only the checks whose inputs are present
are run. Requires PyYAML (pip install pyyaml) only when --openapi is given.
"""
import argparse
import re
import sys
from pathlib import Path


def read(p):
    return Path(p).read_text(encoding="utf-8") if p else None


def norm(s):
    """Normalize a name for matching across conventions (PlanStatus == plan_status)."""
    return s.replace("_", "").lower()


# --- glossary (the source of truth) ---------------------------------------------------------

def parse_glossary(text):
    """Return canonical name sets from glossary.md."""
    sections, current = {}, None
    for line in text.splitlines():
        h = re.match(r"##\s+(Entities|Enums|Endpoints|Containers)\s*$", line)
        if h:
            current = h.group(1)
            sections[current] = []
        elif current and line.lstrip().startswith("- "):
            sections[current].append(line.strip()[2:])

    entities, tables = set(), set()
    for item in sections.get("Entities", []):
        name = re.search(r"`([^`]+)`", item)
        tbl = re.search(r"table:\s*`([^`]+)`", item)
        if name:
            entities.add(name.group(1))
        if tbl:
            tables.add(tbl.group(1))

    enums = {}
    for item in sections.get("Enums", []):
        m = re.match(r"`([^`]+)`\s*:\s*(.+)", item)
        if m:
            values = {v.strip() for v in m.group(2).split("|") if v.strip()}
            enums[norm(m.group(1))] = values

    endpoints, endpoint_paths = set(), set()
    for item in sections.get("Endpoints", []):
        e = re.search(r"`([^`]+)`", item)
        if e:
            token = e.group(1).strip()
            endpoints.add(token.upper())
            parts = token.split()
            endpoint_paths.add(parts[-1] if parts else token)

    containers = set()
    for item in sections.get("Containers", []):
        c = re.search(r"`([^`]+)`", item)
        if c:
            containers.add(c.group(1))

    return {
        "entities": entities, "tables": tables, "enums": enums,
        "endpoints": endpoints, "endpoint_paths": endpoint_paths, "containers": containers,
    }


# --- per-artifact checks (each appends to fails / warns) ------------------------------------

def check_openapi(text, gl, fails, warns):
    import yaml
    doc = yaml.safe_load(text)
    paths = doc.get("paths") or {}
    for path, methods in paths.items():
        if path not in gl["endpoint_paths"]:
            fails.append(f"OpenAPI path not in glossary Endpoints: {path}")
        for method, op in (methods or {}).items():
            if not isinstance(op, dict):
                continue
            for tag in op.get("tags", []):
                if tag not in gl["containers"]:
                    fails.append(f"OpenAPI tag not a glossary Container: {tag!r}")
    schemas = (doc.get("components") or {}).get("schemas") or {}
    for name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        if "enum" in schema:
            g = gl["enums"].get(norm(name))
            vals = {str(v) for v in schema["enum"]}
            if g is None:
                fails.append(f"OpenAPI enum {name!r} is not in the glossary")
            elif vals != g:
                fails.append(f"OpenAPI enum {name!r} values {sorted(vals)} != glossary {sorted(g)}")
        elif name not in gl["entities"]:
            warns.append(f"OpenAPI schema not a glossary Entity (wrapper?): {name!r}")


def check_ddl(text, gl, fails, warns):
    for m in re.finditer(r"create\s+table\s+(?:if\s+not\s+exists\s+)?(\w+)", text, re.I):
        t = m.group(1)
        if t not in gl["tables"]:
            fails.append(f"DDL table not in glossary: {t}")
    for m in re.finditer(r"create\s+type\s+(\w+)\s+as\s+enum\s*\(([^)]*)\)", text, re.I):
        name = norm(m.group(1))
        vals = set(re.findall(r"'([^']+)'", m.group(2)))
        g = gl["enums"].get(name)
        if g is None:
            fails.append(f"DDL enum {name!r} is not in the glossary")
        elif vals != g:
            fails.append(f"DDL enum {name!r} values {sorted(vals)} != glossary {sorted(g)}")


# A container declaration in Structurizr DSL names itself in the first quoted string:
#     planApi = container "Plan API" "Description" "Technology"
# A container *view* puts the software system identifier first, so it is not a declaration:
#     container trainer "Containers" { ... }
# Requiring the quote right after the keyword keeps declarations and skips view keys.
C4_CONTAINER = re.compile(r'(?<![\w-])container\s+"([^"]+)"')


def check_c4(text, gl, fails, warns):
    for m in C4_CONTAINER.finditer(text):
        if m.group(1) not in gl["containers"]:
            fails.append(f"C4 container not in glossary: {m.group(1)!r}")


def check_sequence(text, gl, fails, warns):
    for m in re.finditer(r'(?:participant|database|entity)\s+"([^"]+)"', text):
        if m.group(1) not in gl["containers"]:
            fails.append(f"Sequence participant not a glossary Container: {m.group(1)!r}")
    for path in set(re.findall(r"(/[\w{}/-]+)", text)):
        if path not in gl["endpoint_paths"]:
            fails.append(f"Sequence message path not a glossary Endpoint: {path}")


# --- coverage: the reverse direction, is every glossary name actually implemented? ----------

def check_coverage(gl, openapi, ddl, c4, fails):
    if openapi is not None:
        import yaml
        present = set((yaml.safe_load(openapi).get("paths") or {}).keys())
        for p in gl["endpoint_paths"] - present:
            fails.append(f"Coverage: glossary Endpoint has no OpenAPI path: {p}")
    if ddl is not None:
        present = {m.group(1) for m in
                   re.finditer(r"create\s+table\s+(?:if\s+not\s+exists\s+)?(\w+)", ddl, re.I)}
        for t in gl["tables"] - present:
            fails.append(f"Coverage: glossary entity table missing from DDL: {t}")
    if c4 is not None:
        present = {m.group(1) for m in C4_CONTAINER.finditer(c4)}
        for c in gl["containers"] - present:
            fails.append(f"Coverage: glossary Container missing from C4: {c!r}")


def main():
    ap = argparse.ArgumentParser(description="Glossary-based consistency gate")
    ap.add_argument("--glossary", required=True)
    ap.add_argument("--openapi")
    ap.add_argument("--c4")
    ap.add_argument("--sequence")
    ap.add_argument("--ddl")
    ap.add_argument("--no-coverage", action="store_true",
                    help="skip the reverse coverage check (use while still building the package)")
    args = ap.parse_args()

    gl = parse_glossary(read(args.glossary))
    openapi, ddl, c4, sequence = (read(args.openapi), read(args.ddl),
                                  read(args.c4), read(args.sequence))
    fails, warns = [], []

    # conformance: every name used in an artifact exists in the glossary
    if openapi is not None:
        check_openapi(openapi, gl, fails, warns)
    if ddl is not None:
        check_ddl(ddl, gl, fails, warns)
    if c4 is not None:
        check_c4(c4, gl, fails, warns)
    if sequence is not None:
        check_sequence(sequence, gl, fails, warns)

    # coverage: every glossary name is actually implemented (skip with --no-coverage
    # while the package is still being built one artifact at a time)
    if not args.no_coverage:
        check_coverage(gl, openapi, ddl, c4, fails)

    for w in dict.fromkeys(warns):
        print("  warning: " + w)

    if fails:
        print("CONSISTENCY GATE: FAIL")
        for f in dict.fromkeys(fails):
            print("  - " + f)
        sys.exit(1)

    print("CONSISTENCY GATE: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
