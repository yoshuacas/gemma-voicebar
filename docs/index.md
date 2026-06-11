# gemma-voicebar

*Local, accurate voice dictation for macOS — in your menu bar, no cloud.*

gemma-voicebar replaces macOS built-in dictation with a small menu-bar app that runs
[mlx-whisper](https://github.com/ml-explore/mlx-examples) for speech-to-text and
[Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) for text-to-speech — entirely
on-device, in a single process. Hold a key, speak, and accurate text appears at your
cursor; with **live typing** enabled, confirmed words are typed as you talk.

Built for Apple Silicon. Tested on an M2 Pro with 32 GB RAM; the whisper model is
~500 MB, so it runs comfortably alongside everything else.

## Why not just use macOS dictation?

Apple's dictation types instantly but mishears too often, and its engine is not
pluggable — there is no API to swap in a better model. gemma-voicebar mimics the
type-as-you-speak experience with whisper's accuracy instead. The trade-off: words
appear in confirmed bursts a couple of seconds behind your voice rather than
word-by-word. See [How it works](explanation/architecture.md) for the design.

## Start here

| | |
|---|---|
| **[Getting started](tutorials/getting-started.md)** | Install and dictate your first sentence (~10 minutes, most of it model download). |
| **[Guides](guide/index.md)** | Grant macOS permissions, tune live typing, fix common problems. |
| **[Reference](reference/index.md)** | Hotkeys, menu items, config file keys, module map. |
| **[How it works](explanation/architecture.md)** | Why a single process, and how streaming commits work on a non-streaming model. |

## At a glance

- **Hold Right Option** — push-to-talk: speak, release, text lands at your cursor.
- **⌃⌥S** — speaks the selected text aloud through Kokoro (8 voices).
- **100% local** — audio never leaves your machine.
- **Live typing** — confirmed words are typed while you speak (LocalAgreement-2 over chunked whisper passes), with guards against whisper's silence-hallucination loops.
- **Clipboard-safe** — paste injection snapshots and restores your clipboard, including rich content.

Source: [github.com/yoshuacas/gemma-voicebar](https://github.com/yoshuacas/gemma-voicebar)
