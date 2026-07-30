# Step 1: Transcription

> Running example: a **personal trainer** app.

## What it is
Turning the interview recording into text, so the requirements step works from a searchable,
quotable source instead of memory. The transcript is the primary source that closes gaps later,
so keep it.

## What goes inside
Run the recording through any speech-to-text tool. Whisper is a common choice and works well
for interviews. This repo does not ship a transcription script on purpose, because the tool is
external and easy to install yourself.

- Large files: compress to mono 16 kHz before sending, or split into chunks, since most APIs
  cap the upload size.
- Keep the raw audio and the `.txt` side by side, named the same.

## What the text looks like
A plain `.txt` of the conversation. Speaker labels help but aren't required. Don't clean it up
into prose, you want the literal words, because a requirement often hides in an offhand phrase.

```
them: we don't want to bug people, so the plan only regenerates once a week
    -> later: FR on scheduled regeneration, and ADR-0001 (schedule vs on demand)
```

## Which diagram
None.

## What does NOT go in
Don't paraphrase while transcribing. If you smooth "once a week, I guess" into "weekly," you've
erased the uncertainty that should have become an open question.

## How to validate
Spot-check the transcript against the audio at a few points, especially where numbers were
said. A misheard "15" for "50" propagates all the way to an NFR.

## Signs it's good
- The numbers in the transcript match what you hear in the recording.
- Uncertain phrasing survived as uncertain, not rounded into fact.
- The file is ready to read straight into the requirements template.

Next: [Step 2: Business Requirements](2-business-requirements.md).
