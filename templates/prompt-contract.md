# Prompt contract: <name of the model call>

An LLM call is an interface. It has an input shape, an expected output shape, and failure modes —
the same three things an HTTP method has. What it does not have is a schema anyone can lint, so the
contract stays in someone's head until it breaks.

Use this template for a feature whose real interface is a prompt rather than an endpoint. It is the
OpenAPI of the reduced package: same job, different medium.

Fill every section. A section you cannot fill is a finding, not an omission — record it in
`open-questions.md` and leave the id here.

---

## 1. Identity

| Field | Value |
|---|---|
| Name | `<name from the glossary>` |
| Caller | `<component that makes the call>` |
| Source file | `<path:line>` |
| Model | `<setting name, and the value in production>` |
| Triggered by | `<user action, schedule, or another component>` |
| Requirement | `<FR / UC this serves>` |

## 2. Input

What is assembled into the prompt, where each piece comes from, and what bounds it.

| Piece | Source | Bound | Empty case |
|---|---|---|---|
| `<data>` | `<table / API / previous step>` | `<row cap, char cap, time window>` | `<skipped, or call not made at all>` |

**Assembly rules.** Anything the caller does to the data before it reaches the model: truncation,
ordering, serialization format, what is dropped silently.

**Not sent.** Data the caller has and deliberately withholds. If nothing, say so — a reader will
assume the omission is an oversight otherwise.

## 3. Instruction

The behavioural rules the prompt imposes, as rules, not as a copy of the text.

| Rule | Why it is there |
|---|---|
| `<e.g. answer only from the data above, never from general knowledge>` | `<the risk it guards>` |

Quote verbatim only the phrases that carry a guarantee. A pasted prompt rots; the rules survive
rewording.

## 4. Output

**Expected shape.** The exact structure the caller parses. If it is JSON, give the schema.

**Permitted empty answer.** Whether the model is allowed to decline, in what form, and what the
caller does with it. A model that cannot say "I don't know" will invent — if the prompt has no
empty case, that is a finding.

**Post-processing.** Everything the caller does between the raw response and the value it uses:
unwrapping code fences, parsing, trimming, type checks, defaults.

## 5. Failure modes

The section that earns the template. One row per way this can go wrong.

| Failure | Detected how | Caller behaviour | Visible to whom |
|---|---|---|---|
| Model unavailable or times out | exception | `<fallback / retry / abort>` | `<user, log only, nobody>` |
| Response is not the expected shape | parse error | | |
| Response is well-formed but empty | value check | | |
| Response is well-formed and wrong | **not detected** | | |

Watch for two rows collapsing into one outcome. A technical failure and an honest empty answer that
produce identical behaviour make the difference invisible downstream — that is a defect, and this
table is where it shows up.

## 6. Cost and latency

| Question | Answer |
|---|---|
| Calls per invocation | `<one, or one per item — say per what>` |
| Output cap | `<max tokens>` |
| Blocking | `<does a user wait on this>` |
| Cost driver | `<what makes this expensive>` |

## 7. Change control

How a change to this prompt is validated. If a golden set, snapshot tests, or an eval covers it,
name them and the command. If nothing covers it, say so plainly: an uncovered prompt is a contract
anyone can rewrite silently.
