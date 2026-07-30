# API Method Summary

The design step before any YAML. Each planned endpoint traces back to an FR or a UC, and
carries the C4 container it belongs to as its tag. Write this first, then the YAML follows it.

| Method | Path | Purpose | Traces to | Tag (C4 container) |
|--------|------|---------|-----------|--------------------|
| POST | /<resource> | <what it does> | FR-N, UC-N | <Container> |
| GET | /<resource>/{id} | <what it does> | FR-N | <Container> |

Rules:
- Every row traces to an FR or UC. No untraceable endpoints.
- The Tag equals a C4 container name exactly.
- Resource and schema names equal the requirement entity names.
