# AI-Review Checklist

Step 9. Run the whole package against this before calling it done. It doubles as a defense
against an AI reviewer, since these are the first things such a review flags. Score each axis,
then give the package a letter (A best, F failing).

## Consistency (machine-checkable, see `tools/check-consistency.py`)
- [ ] Every name (entity, enum, endpoint, container) is defined once in `glossary.md`.
- [ ] Conformance: every name used in an artifact exists in the glossary (tags, paths, enums, tables, participants, messages).
- [ ] Coverage: every glossary endpoint, entity table, and container actually appears in the artifacts.
- [ ] Enum values match the glossary in both OpenAPI and DDL.

## Coverage
- [ ] Every FR maps to an endpoint or a system flow.
- [ ] Every requirement entity has a DDL table.
- [ ] Every UC appears in a sequence diagram.
- [ ] Every parked fork has an ADR or a sourced answer.

## Grounding
- [ ] Every number traces to a source, or is marked `proposal:`.
- [ ] No entity, field, or endpoint exists that the requirements didn't name.
- [ ] Open questions hold everything the interview didn't settle.

## Validity (tools, not eyes)
- [ ] OpenAPI: `redocly lint` returns 0 errors.
- [ ] DDL: applies on PostgreSQL with no errors.
- [ ] C4 and sequence: render from source.

## Verdict
Consistency and grounding failures cap the grade hard, an inconsistent package is not
rescued by pretty diagrams. Record the letter and the top issues to fix.
