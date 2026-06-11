# Reference

## Hotkeys

| Hotkey | Action |
|---|---|
| **Right Option** (hold) | Push-to-talk. Records while held; auto-stops at 29.5 s. With live typing on, confirmed words are typed during the hold; the remainder is typed on release. With live typing off, the full transcript is pasted on release. |
| **⌃⌥S** | Speak the current selection through Kokoro. With no selection, re-speaks the last injected dictation. |

## Menu bar

Title characters:

| Title | State |
|---|---|
| `⏳` | Loading models (startup) or transcribing |
| `●` | Idle, ready |
| `🔴` | Recording |
| `✓` | Injected successfully (flashes briefly) |
| `∅` | Transcript came back empty (flashes briefly) |
| `⚠` | Error — permission missing or engine failure |

Menu items:

| Item | Behavior |
|---|---|
| `Status: …` | `loading models…` → `ready (Ns load)` / `load failed` |
| `Recording method` | `Push-to-talk (Right Option)` — the only method currently |
| `Voice` | One of 8 Kokoro voices; persisted |
| `Live typing` | Toggles streaming commits; persisted |
| `Quit` | Stops hotkey listeners and exits |

## Configuration file

`~/.config/codewithvoice/config.json` — written on change, merged over
defaults at startup.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `voice` | string | `"af_heart"` | Kokoro voice for TTS |
| `live_typing` | bool | `true` | Type confirmed words during dictation |

## Models

| Role | Model | Size | Source |
|---|---|---|---|
| ASR | `mlx-community/whisper-small-mlx-q4` | ~500 MB | Hugging Face, downloaded on first run |
| TTS | `hexgrad/Kokoro-82M` | ~330 MB | Hugging Face, downloaded on first run |

Constants: audio is captured at 16 kHz mono (`recorder.py`), TTS output is
24 kHz (`engine/tts.py`), recordings cap at 29.5 s (`recorder.py:MAX_SECONDS`).

## Module map

All app code lives in `src/voicebar/`:

| Module | Responsibility |
|---|---|
| `app.py` | rumps app: menu, state machine, PTT and speak flows |
| `engine/asr.py` | whisper transcription + hallucinated-segment filter |
| `engine/tts.py` | Kokoro synthesis |
| `streaming.py` | `StreamingTranscriber` — LocalAgreement-2 live commits |
| `recorder.py` | `sounddevice` mic capture, 30 s cap, live `snapshot()` |
| `hotkeys.py` | `pynput` listeners: Right Option PTT, ⌃⌥S |
| `inject.py` | `inject_text()` paste path, `type_text()` keystroke path |
| `selection.py` | `grab_selection()` — synthesized ⌘C with clipboard restore |
| `playback.py` | speaker output |
| `state.py` | config load/save, runtime state |

## Commands

```bash
make install   # uv sync (venv + all dependencies)
make run       # run the app in the foreground
make smoke     # in-process ASR + TTS engine test, no desktop session needed
make espeak    # brew install espeak-ng
make docs      # serve this documentation site locally
```
