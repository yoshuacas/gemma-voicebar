<p align="center"><em>Local, accurate voice dictation for macOS — Whisper ASR + Kokoro TTS in a single menu-bar app.</em></p>

<p align="center">
  <a href="./docs/tutorials/getting-started.md">Getting started</a> ·
  <a href="https://yoshuacas.github.io/gemma-voicebar/">Docs</a> ·
  <a href="./docs/reference/index.md">Reference</a> ·
  <a href="./AGENTS.md">Agent guide</a>
</p>

---

# gemma-voicebar

**gemma-voicebar** replaces macOS built-in dictation with a menu-bar app that runs
entirely on-device: [mlx-whisper](https://github.com/ml-explore/mlx-examples) for
speech-to-text and [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) for
text-to-speech, in one process. Apple's dictation types instantly but mishears
constantly; this types a couple of seconds behind your voice, and gets the words
right.

The repo also contains the **Gemma 4 capability demos** (`demos/`) this project
grew out of — standalone scripts exercising Gemma 4's text, image, audio, and
video modalities on Apple Silicon.

## Key features

- **Push-to-talk dictation** — hold Right Option, speak, release; text lands at your cursor.
- **Live typing** — confirmed words are typed *while* you speak (LocalAgreement-2 over chunked whisper passes), with layered guards against whisper's silence-hallucination loops.
- **Speak-back** — ⌃⌥S reads the selected text aloud; 8 Kokoro voices.
- **100% local** — audio never leaves the machine; models are ~500 MB (whisper-small-q4) + ~330 MB (Kokoro).
- **Clipboard-safe** — paste injection snapshots and restores clipboard contents, including rich types.
- **Single process** — no daemon, no HTTP; one `rumps` app owns hotkeys, mic, models, and injection.

## Quickstart

Requires Apple Silicon, macOS 14+, [Homebrew](https://brew.sh), and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/yoshuacas/gemma-voicebar.git
cd gemma-voicebar
make -C ops install-deps
make -C ops espeak        # Kokoro fallback for uncommon words
make -C ops bar           # first run downloads models (~850 MB), then ⏳ → ●
```

Grant **Microphone**, **Accessibility**, and **Input Monitoring** to your
terminal app when prompted, relaunch, then hold **Right Option** in any text
field and speak. Full walkthrough:
[Getting started](./docs/tutorials/getting-started.md) · stuck?
[Fix hotkeys that do nothing](./docs/guide/fix-permissions.md).

## Documentation

The [docs site](https://yoshuacas.github.io/gemma-voicebar/) (also browsable in
[`./docs`](./docs)) covers:

- [Tutorial: getting started](./docs/tutorials/getting-started.md)
- [Guides](./docs/guide/index.md) — permissions, live typing tuning, voices, login launch, slow-ASR diagnosis
- [Reference](./docs/reference/index.md) — hotkeys, menu, config keys, models, module map
- [How it works](./docs/explanation/architecture.md) — the single-process design and how live typing works on a non-streaming model

AI coding agents: start at [AGENTS.md](./AGENTS.md).

## Gemma 4 demos

Standalone capability demos, independent of the dictation app. Gemma 4 E4B-it is
gated — accept the license on
[Hugging Face](https://huggingface.co/google/gemma-4-E4B-it) first.

```bash
uv sync
uv run hf auth login
uv run python demos/text_demo.py     # also: image_demo, audio_demo, video_demo
```

| Modality | Verified | Speed on M2 Pro |
|---|---|---|
| Text + thinking | Multi-step reasoning | 4.7–8.1 tok/s |
| Image | Description, Q&A, OCR | 3–8 tok/s |
| Audio | Verbatim ASR, translation (≤30 s) | 1.5–8 tok/s |
| Video | Frame sequences ≤60 s | 2–3 tok/s |

Inference uses ~10–15 GB unified memory — which is exactly why the dictation app
does *not* use Gemma; see
[How it works](./docs/explanation/architecture.md#why-one-process-and-why-whisper).
Drop your own files into `samples/` — demos auto-discover them. Gotchas
(torchcodec, chat-template quirks) are documented in
[AGENTS.md](./AGENTS.md) and the demo sources.

## Project layout

```text
packages/voicebar/   — the menu-bar app (src/voicebar/)
packages/shared/     — Gemma 4 loader used by the demos
demos/               — Gemma 4 capability demos
docs/                — documentation site (GitHub Pages)
ops/Makefile         — install-deps / bar / espeak
samples/             — sample image/audio/video inputs
```

## License

Code in this repository is for personal experimentation; no license has been
chosen yet. Gemma 4 is governed by the
[Gemma Terms of Use](https://ai.google.dev/gemma/terms). Kokoro TTS is Apache 2.0,
whisper weights MIT.
