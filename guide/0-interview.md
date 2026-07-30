# Step 0: Interview

> Running example: a **personal trainer** app.

## What it is
The step that SDD frameworks don't have. You start not from a written spec but from a live
conversation, because the requirements don't exist yet. Your job is to extract them by asking.
Record the conversation so nothing is lost to memory.

## What goes inside
Ask along 6 axes, in order. Each axis feeds a later section of the requirements.

1. **Goal and metric.** Why does this exist, and how is success measured as a number?
2. **Scenarios.** Walk me through how someone actually uses it, start to finish.
3. **Sources.** Where does the data come from? Sensors, other systems, the user?
4. **Functional.** What must the system do? One behavior at a time.
5. **Non-functional.** How fast, how many, how available? Push for numbers.
6. **Acceptance.** How will you know it's correct? What would count as a failure?

## What the text looks like
There is no artifact here except the recording and your notes. The output is questions, not
documents. Use [`checklists/interview.md`](../checklists/interview.md) as a live prompt sheet
so you don't drop an axis in the flow of conversation.

```
You: "When the plan adapts, how do you know it adapted well?"
Them: "If the user keeps showing up. Adherence over 4 weeks."
    -> that's your acceptance metric, and later NFR-1.
```

## Which diagram
None. This is talking and listening.

## What does NOT go in
Your own assumptions. If the stakeholder is vague ("it should just work"), don't quietly
resolve it. Ask, and if it stays open, it becomes an open question at step 2, not a decision
you made for them.

## How to validate
You have covered all 6 axes, and for every "fast," "reliable," or "accurate" you heard, you
pushed for a number. If you left with adjectives instead of numbers, the interview isn't done.

## Signs it's good
- Every one of the 6 axes has real answers, not silence.
- Non-functional claims came back as numbers (p95, RPS, %, retention).
- You can name the acceptance test the stakeholder would accept.
- The recording is clean enough to transcribe.

Next: [Step 1: Transcription](1-transcription.md).
