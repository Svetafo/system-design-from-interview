# AI-Review Checklist

Step 9. Run the whole package against this before calling it done. It doubles as a defense
against an AI reviewer, since these are the first things such a review flags. Score each axis,
then give the package a letter (A best, F failing).

## Consistency (machine-checkable, see `tools/check-consistency.py`)
- [ ] Every name (entity, enum, endpoint, container) is defined once in `glossary.md`.
- [ ] Conformance: every name used in an artifact exists in the glossary (tags, paths, enums, tables, participants, messages).
- [ ] Coverage: every glossary endpoint, entity table, and container actually appears in the artifacts.
- [ ] Enum values match the glossary in both OpenAPI and DDL.

## The register and the package's own state
- [ ] Every open question carries a class: `blocks-package`, `blocks-point`, `non-blocking`.
- [ ] Every `blocks-point` entry has a matching marker in an artifact, and every marker in an
      artifact has a matching entry. No artifact carries an invented value in place of one.
- [ ] Every closed entry names what closed it, with a date and a source that can be checked.
- [ ] The package state is written and current: method, clone, step, verdict, what blocks, what
      next. Someone opening the folder cold can tell where it stands without asking.
- [ ] A skipped step is recorded as a decision at the time it was skipped, with its reason. A
      reason written after someone noticed the gap is not a decision, it is a cover.
- [ ] At step 10 only: every remaining entry has a fate, work, a decision, documented behaviour, or
      dropped with a reason. Nothing is left open in a package that has shipped.

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
