# Step 10: From Package to Implementation

> Running example: a **personal trainer** app.

Steps 0 to 9 produce a validated design package. This step is how you hand that package to a
coding agent and build from it without drift, and where the human still owns the hard parts. The
method is the front half, from interview to package; implementation is the back half. This step
is tool-agnostic: it works with any coding agent and any SDD toolchain.

## Close out the register first

Before the handoff, every entry still open in `open-questions.md` gets a fate. A package that goes
into implementation with a live register leaves a folder nobody can read six months later: twenty
questions, and no way to tell which are still real.

Each remaining entry becomes exactly one of four things.

- **Work.** It was never a question, it was a defect or a task. Move it to the project's backlog,
  with the file and the fix, and link back to the package. It leaves the register.
- **A decision.** It has real alternatives and someone has to choose. Write the ADR, or, if the
  choice belongs to implementation, hand it over named as a decision the builder must make and not
  quietly resolve.
- **Documented behaviour.** Not work and not a decision, just something nobody had written down.
  It lives in the artifact that describes it, the contract or the DDL, and it leaves the register
  with a pointer there.
- **Dropped.** It stopped mattering. Say so and say why. A dropped entry with a reason is a
  record; a dropped entry that quietly disappears is a hole in the trail.

What must not happen is the fifth option: leaving it open and handing the package over anyway. An
open entry is a claim that someone will come back to it, and nobody comes back to a register whose
package has already shipped.

Update the package state with the outcome, so the folder still describes itself after the work
moves elsewhere.

## What the package gives the agent
A grounded, consistent brief instead of a vague ticket:

- **glossary.md** the names are locked; the agent draws from one list.
- **OpenAPI** the endpoints, request and response shapes, schemas.
- **DDL** the data model, ready to apply.
- **C4** the container boundaries, which map to services or modules.
- **Sequence** the call flows, one per method.
- **ADR** the decisions the agent must respect (transport, trigger, where the AI runs).
- **CONSTITUTION** the discipline: do not invent, names from the glossary, forks to an ADR.
- **Requirements** the why and the acceptance criteria.

## The handoff, in order (prompt recipe)
Feed the discipline first, then the contract, then build one step at a time.

```
1. First message (set the rules):
   "Follow CONSTITUTION.md. Use only names from glossary.md. If you need a new
    name, add it to the glossary first. Do not invent entities, endpoints, or
    fields that are not in the package."

2. Attach the package:
   glossary.md, api.yaml, schema.sql, c4/workspace.dsl, sequence/*.puml,
   adr/*.md, requirements.md

3. Drive one step at a time, gating after each:
   a. "Propose an implementation plan and the tech stack, respecting the ADRs."
   b. "Break the plan into tasks, one per endpoint, table, and flow."
   c. "Implement task <n>. Use glossary names. Stop at the task boundary."

4. After anything is generated or regenerated, run the gate:
   python3 tools/check-consistency.py --glossary glossary.md --openapi api.yaml ...
```

## Two ways from package to code
Pick one; both start from the same package.

### A. Bridge to an SDD toolchain
Your package is the specification. Feed it as the input to the back half of any Spec-Driven
Development tool, which handles plan, tasks, and implement. Examples, in no particular order:
GitHub spec-kit (`/speckit.plan`, `/speckit.tasks`, `/speckit.implement`), AWS Kiro, Cursor Plan
Mode, OpenSpec, BMAD. spec-kit is the most adopted open-source one and is model-agnostic, so it is
a convenient reference, but the package does not depend on any single tool. You supply the
front-half artifact these tools assume already exists.

### B. Built-in variant (no external tool)
Drive the agent directly with the recipe above: ask it to derive a plan from the package, then a
task list (one task per endpoint, table, and flow), then implement task by task, checking each
against the glossary. This keeps the method self-contained: interview to running code with nothing
but the package and a coding agent.

## What the agent builds vs what stays with you
**The agent builds directly, high confidence:**
- API scaffolding from the OpenAPI contract.
- The database from the DDL.
- Models and DTOs from the schemas and glossary.
- Service or module skeletons from the C4 containers.
- Endpoint stubs and their orchestration from the sequence diagrams.

**Stays with the human:**
- Core business logic and algorithms (for the trainer, how the AI actually adapts the plan). The
  sequence shows the call flow, not the algorithm inside.
- The acceptance dataset and tests behind the NFRs (an accuracy target needs a real test set).
- The tech stack, unless an ADR already fixed it.
- Edge cases, error handling depth, security and auth specifics the interview left thin.

## The leash: consistency through codegen
The same glossary and `check-consistency` that governed the design now govern the code. Names in
the code equal names in the contract. Run the gate against regenerated artifacts too. The agent may
not introduce an entity or endpoint that is not in the glossary; if it needs one, it goes into the
glossary first and back through the gate. The "do not invent" rule extends from documents to code.
This is the part of the method that keeps adding value into implementation, and it is what most
raw agent codegen lacks.

## Human gates in implementation
Review generated code against the contract, not just against "it runs." Run the acceptance tests.
Reject any endpoint or entity that is not in the glossary. Autonomy of execution is not autonomy of
decision: the agent builds, you decide and verify. In a regulated environment this is not
optional, it is what makes agent-built software shippable.

## The honest boundary
This is not one-click product generation. It is a grounded, consistent starting point plus a leash
that makes agent codegen reliable, with the hard parts (core logic, acceptance data, security)
still owned by a human. That honesty is the point: the method makes the agent dependable, it does
not pretend to replace the engineer.

This is the last step. Back to the [README](../README.md) for the whole pipeline.
