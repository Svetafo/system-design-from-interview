---
name: question-triage
description: Triages an open-questions register from a system design package. Sorts every entry into what a primary source can close, what only a person can decide, and what is already answered elsewhere, then closes the first kind by going and looking, citing the file and line it came from. Use when the user asks to triage open questions, wants to know which questions actually need them, asks what is left open in a package, or hands over an open-questions.md.
---

# Question Triage

Most of an open-questions register does not need a person. It needs someone to go and look: at the
code, at the schema, at a contract, at the real file on disk. Sorting that from what genuinely
requires a decision is the whole job, and it is worth doing because the two are mixed together and
the mix is what makes a register feel heavy.

You close the first kind. You never close the second.

## The line you do not cross

An entry that has no source outside a person's intent is not yours to answer, however obvious the
answer seems. Target metrics, scope calls, which options are acceptable, whether to warn a user,
how long data is kept: there is nothing to go and look at, so any answer you produce is invention
wearing the clothes of a finding. That is the exact failure the surrounding method exists to
prevent, and closing such an entry defeats it from the inside, quietly, in a way nobody will catch
later.

There is a second reason beyond correctness. The register is what keeps a human accountable for the
design. A package whose questions were closed by an agent is self-certifying: every entry answered,
no trace of who decided. Leave the trail intact.

If you are unsure which kind an entry is, it is the second kind. Say so and move on.

## What you do

Read the register, and for each open entry decide which of these it is.

**Closable by a primary source.** The answer exists in something you can open: code, a migration, a
config, a contract, a rendered file, the output of a command. Go and get it. Close the entry with
what you found and where you found it, `file:line` or the exact command, plus the date. If what you
find contradicts the register's own premise, say that plainly rather than smoothing it over.

**A decision for a person.** No source outside intent. Leave it open, and add one line saying who
can close it and what the answer unblocks. If it has real alternatives, note that it is an ADR
rather than a value, and list the options you can see. Drafting options is useful; choosing is not
yours.

**Already answered elsewhere.** Another entry covers it, an ADR settled it, or an artifact already
documents the behaviour. Point at where, and mark it for merging rather than closing it on your own
authority.

**Not a question at all.** It is a defect or a task: nothing to decide, someone just has to fix it.
Say so and name the file. It belongs in the project's backlog, not in a design register.

## Report

Group by those four, most-blocking first inside each group. For every entry you closed, show the
source, not a summary of it: the reader has to be able to check you in one click. Then state, in one
line, how many entries still need the human and which of those hold up the whole package.

Do not edit artifacts other than the register. Applying an answer to requirements, diagrams or DDL
is scenario C in `SCENARIOS.md` and happens after a human has verified your attribution.

## Traps

- **A plausible answer is not a found answer.** If you did not open something, you did not close
  anything.
- **A confident guess about a number is the worst case.** Numbers get quoted back as fact forever.
- **Code shows what is, not what was intended.** When you close an entry from code, you are
  recording current behaviour; if it looks like a defect, say that instead of blessing it as the
  answer.
- **Do not reclassify an entry to make it closable.** If it is a decision, its being inconvenient
  does not make it a lookup.
