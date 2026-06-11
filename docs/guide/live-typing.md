# How to tune or disable live typing

**Goal:** change how text appears during dictation — turn live typing off, or
adjust its cadence.

## Disable (or re-enable) live typing

Menu bar `●` → **Live typing**. The checkmark toggles; the setting persists in
`~/.config/gemma-voicebar/config.json` as `"live_typing"`.

- **On (default):** confirmed words are typed while you speak, ~2.5 s behind;
  the remainder lands when you release the key.
- **Off:** the whole transcript is pasted at once on release — the original
  behavior, and the only mode that uses the clipboard.

Short utterances (under ~5 s) behave identically in both modes: nothing has time
to commit early, so all text arrives on release.

## Change the commit cadence

The re-transcription interval is the `interval` parameter of
`StreamingTranscriber` in `src/voicebar/streaming.py`
(default `2.5` seconds, set at the call site in `app.py`).

- **Lower it** (e.g. `1.5`) for snappier commits at the cost of more compute
  per utterance.
- **Raise it** (e.g. `4.0`) if you see ASR passes backing up on a loaded machine.

## Make commits stricter

If a wrongly-committed word ever slips through (typed text is never retracted),
raise `HOLDBACK_WORDS` in `streaming.py` from `1` to `2`. Each commit then waits
for one more confirming pass — slightly more lag, fewer mistakes.

## Known behaviors

- Words arrive in bursts every couple of seconds, not word-by-word. This is
  inherent to the design — see
  [How it works](../explanation/architecture.md#live-typing-on-a-non-streaming-model).
- Keep focus in the target field while dictating; keystrokes follow focus.
- Repeated-word floods from silence (a whisper hallucination) are filtered by
  three guards; at most a doubled word can appear.
