# Async Topic (Kafka or similar)

Use when the design has asynchronous messaging alongside the REST API. One entry per topic,
plus the message structure. The topic name is taken from the service config, not
invented here.

## Topic summary

| Topic | Direction | Producer | Consumer | Purpose |
|-------|-----------|----------|----------|---------|
| <topic.name> | produce / consume | <container> | <container> | <what and why> |

## Message structure

For each topic, the payload shape.

```
topic: <topic.name>
key: <what the key is>
value:
  <field>: <type>   # <source: FR/entity>
  <field>: <type>
```

Rules:
- The topic name matches the real service config (the source of truth for names), not a guess.
- Producers and consumers are C4 containers.
- Payload fields trace to requirement entities or FRs.
