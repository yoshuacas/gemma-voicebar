<p align="center"><em>Local, accurate voice dictation for macOS — Whisper ASR + Kokoro TTS in a single menu-bar app.</em></p>

<p align="center">
  <a href="https://yoshuacas.github.io/gemma-voicebar/">Documentation</a> ·
  <a href="https://yoshuacas.github.io/gemma-voicebar/tutorials/getting-started/">Getting started</a> ·
  <a href="https://yoshuacas.github.io/gemma-voicebar/reference/">Reference</a> ·
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
make install
make espeak    # Kokoro fallback for uncommon words
make run       # first run downloads models (~850 MB), then ⏳ → ●
```

Grant **Microphone**, **Accessibility**, and **Input Monitoring** to your
terminal app when prompted, relaunch, then hold **Right Option** in any text
field and speak. Full walkthrough:
[Getting started](https://yoshuacas.github.io/gemma-voicebar/tutorials/getting-started/).

## Documentation

Full docs at **[yoshuacas.github.io/gemma-voicebar](https://yoshuacas.github.io/gemma-voicebar/)**:

- [Tutorial: getting started](https://yoshuacas.github.io/gemma-voicebar/tutorials/getting-started/)
- [Guides](https://yoshuacas.github.io/gemma-voicebar/guide/) — permissions, live-typing tuning, voices, login launch, slow-ASR diagnosis
- [Reference](https://yoshuacas.github.io/gemma-voicebar/reference/) — hotkeys, menu, config keys, models, module map
- [How it works](https://yoshuacas.github.io/gemma-voicebar/explanation/architecture/) — the single-process design and how live typing works on a non-streaming model

Source for all pages lives in [`./docs`](./docs) (MkDocs Material; `make docs`
serves it locally). AI coding agents: start at [AGENTS.md](./AGENTS.md).

## Project layout

```text
src/voicebar/     — the app (engine/, streaming.py, recorder, hotkeys, inject…)
docs/             — documentation site source (MkDocs Material)
samples/          — sample audio used by `make smoke`
Makefile          — install / run / smoke / espeak / docs
```

## License

[MIT](./LICENSE). Whisper weights are MIT, Kokoro TTS is Apache 2.0.
