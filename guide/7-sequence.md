# Step 7: Sequence

> Running example: a **personal trainer** app.

## What it is
A set of sequence diagrams that show behavior over time. One is the end-to-end process (the main
use case, success and the key failure). The rest are one per method in the API contract, each
zooming into that single call in detail. They reuse the participants from C4 and the endpoints
from OpenAPI, so they can't invent new pieces. A tiny API may have only one method, so the whole set collapses
to a single method diagram (as in the running example), but the rule is one sequence per method.

## What goes inside
- **Process diagram:** the primary flow start to finish. For the trainer: user logs a Session,
  the Adaptation Engine updates the TrainingPlan, the user reads the new plan.
- **Method diagrams, one per contract method:** each API call in detail, including its failure
  branch. For example `POST /plans` with validation and the error path, `POST /sessions`, and so
  on for every path in the OpenAPI file.

Participants are the C4 containers. Messages are the OpenAPI endpoints.

## What the text looks like
PlantUML, rendered to PNG. Names match C4 and OpenAPI exactly.

```
@startuml
actor User
participant "Plan API" as API
participant "Adaptation Engine" as Eng
database "Database" as DB

User -> API : POST /sessions (log Session)
API -> DB : insert session
API -> Eng : adapt(TrainingPlan)
Eng -> DB : update training_plan
User -> API : GET /plans/{id}
API --> User : 200 TrainingPlan (ACTIVE)
@enduml
```

Participants and messages are names from the [glossary](../templates/glossary.md): a participant that isn't a glossary container, or a message that isn't a glossary endpoint, is a drift to fix upstream.

## Which diagram
This step is the diagram. The sequence shows the cross-participant
exchange, not the internal logic of any one container. Put internal logic in a flowchart if you
need it.

## What does NOT go in
Participants that aren't C4 containers, and messages that aren't OpenAPI endpoints. If the
sequence needs a box that doesn't exist upstream, that's a gap in C4 or OpenAPI, fix it there,
not here.

## How to validate
It renders from the `.puml` source, and every participant appears in C4 while every message
appears in the OpenAPI paths. This is one of the checks `tools/check-consistency.py` automates.

## Signs it's good
- A process diagram, plus one method diagram for every method in the contract, each with its
  failure branch.
- Every participant is a C4 container, every message is an OpenAPI endpoint.
- It renders cleanly from source.
- No internal container logic leaks into the cross-participant view.

Start from [`templates/sequence.puml`](../templates/sequence.puml), which renders as it stands and
already carries the shape of a failure branch.

See this step's output in the example package: [`sequence/`](../example/sequence), a process diagram plus one per contract method.

Next: [Step 8: DDL](8-ddl.md).
