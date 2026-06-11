# How gemma-voicebar works

*Guiding question: how do you get accurate, live-feeling dictation out of
on-device models on a memory-constrained Mac?*

## Why one process, and why whisper

The first version used Gemma 4 (an any-to-any multimodal model) for ASR behind
a FastAPI daemon, managed by launchd. The transcription quality was excellent —
and the architecture failed anyway: Gemma's ~10 GB working set on a 32 GB
machine triggered constant memory thrashing (at its worst, 44 GB of swap and
inference 50× slower than nominal). No amount of service architecture fixes a
model that doesn't fit comfortably in RAM next to a browser and an IDE.

The redesign inverted both decisions at once:

- **Model:** whisper-small (4-bit quantized, ~500 MB) via mlx-whisper. It
  transcribes 9–30× faster than realtime on an M2 Pro and its accuracy is far
  closer to Gemma's than to Apple dictation's.
- **Topology:** with the model that small, a separate daemon serves no purpose.
  Everything — hotkeys, mic, both models, injection — lives in the single
  menu-bar process. No HTTP, no LaunchAgent, no IPC to debug. A single
  `threading.Lock` serializes engine calls.

The daemon would only return if multiple frontends ever needed to share the
models, which is not the case.

## Live typing on a non-streaming model

Whisper transcribes complete clips; it has no streaming mode. Yet macOS
dictation users expect text to appear as they speak. gemma-voicebar fakes
streaming with **chunked re-transcription plus LocalAgreement-2**
(`streaming.py`):

1. While the PTT key is held, a worker re-transcribes the *entire* audio
   captured so far, every 2.5 s.
2. Whisper revises its hypothesis as context grows, so nothing is trusted
   until two consecutive passes agree. The agreed word-prefix is **committed** —
   typed into the focused app as keystrokes, never to be retracted.
3. On key release, one final pass over the full clip produces the definitive
   transcript, and only the tail beyond the committed words is typed.

Three details make this robust in practice:

- **Holdback.** The last word of any pass is never committed — the audio buffer
  usually cuts mid-word, and whisper guesses the fragment ("seem" for "seems").
- **Content-based alignment.** When whisper revises an already-committed word,
  the new hypothesis is aligned to the committed text by content
  (`difflib.SequenceMatcher`), not by word position — otherwise one revision
  would duplicate or drop its neighbors.
- **Hallucination guards.** Whisper invents repeating word loops over silence
  ("cooling cooling cooling…"), and a loop is *self-consistent across passes*,
  so agreement alone confirms it. Three independent guards stop this:
  whisper's own per-segment quality signals (compression ratio, no-speech
  probability) filter hallucinated segments in `engine/asr.py`; the committer
  refuses to extend a run of more than two identical words; and passes are
  skipped entirely when no new speech has arrived (RMS silence check).

The result is text in confirmed bursts ~2.5 s behind the voice. True
word-by-word output would require a natively streaming model (e.g. a
Zipformer transducer) at a real accuracy cost — accuracy was the reason this
project exists, so the burst cadence is the accepted trade.

## Why paste for one mode and keystrokes for the other

Final transcripts (live typing off, or short utterances) are **pasted**: the
text is placed on the clipboard and ⌘V is synthesized, after snapshotting the
clipboard's full contents — every pasteboard type, as raw `NSData` — and
restoring it afterwards. Pasting is atomic and fast for a paragraph of text.

Live-typing commits are **typed** as synthesized keystrokes instead. Clobbering
the clipboard every 2.5 s mid-dictation would be hostile to the user, and
keystrokes match the as-you-speak feel.

Both paths fail safely in secure fields (password boxes): macOS rejects the
synthesized input, and the app notifies rather than guessing.
