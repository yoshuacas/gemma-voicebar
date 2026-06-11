# Getting started

Take codewithvoice from zero to your first dictated sentence. Takes about
10 minutes; most of that is the one-time model download.

**You'll need:** a Mac with Apple Silicon, macOS 14+, [Homebrew](https://brew.sh),
and [uv](https://docs.astral.sh/uv/getting-started/installation/).

## 1. Clone and install

```bash
git clone https://github.com/yoshuacas/codewithvoice.git
cd codewithvoice
make install
```

This creates a virtualenv and installs everything with `uv`.

## 2. Install espeak-ng

```bash
make espeak
```

Kokoro falls back to espeak-ng for words outside its lexicon; without it,
uncommon words may be skipped during speech playback.

## 3. Launch the app

```bash
make run
```

The menu bar shows `⏳` while models load. The first launch downloads
whisper-small (~500 MB) and Kokoro (~330 MB) from Hugging Face — a few minutes
on a fast connection. Subsequent launches load in 10–25 seconds. When the title
flips to `●`, it's ready.

## 4. Grant permissions

The first time you dictate, macOS prompts for three permissions. All are
attributed to the **terminal app you launched from** (Terminal, iTerm, etc.).
Approve all three under **System Settings → Privacy & Security**:

1. **Microphone**
2. **Accessibility**
3. **Input Monitoring**

After granting Input Monitoring, quit the app (menu bar → Quit) and run
`make run` again so the hotkey listeners pick up the grant.

## 5. Dictate

1. Open TextEdit and click into the document.
2. Hold **Right Option**, say *"hello world, this is my first dictation"*, release.
3. Watch the menu bar: `🔴` recording → `⏳` transcribing → `✓` done.

Your words appear at the cursor. If you spoke for more than ~5 seconds, you'll
see confirmed words being typed *while* you talk — that's live typing.

## 6. Hear it back

Select the text you just dictated and press **⌃⌥S** (Control+Option+S).
Kokoro reads it aloud.

That's it — you have a working local dictation setup.

## 7. Optional: spoken summaries from Claude Code

If you use Claude Code, close the loop — dictate your prompts with Right
Option, and hear a one-sentence spoken summary when Claude finishes each turn:

```bash
mkdir -p ~/.claude/hooks
cp hooks/speak-summary.py ~/.claude/hooks/
```

Then add to `~/.claude/settings.json` (create it if missing):

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "python3 ~/.claude/hooks/speak-summary.py",
        "async": true,
        "timeout": 60
      }
    ]
  }
}
```

Start a new Claude Code session anywhere, ask it something, and the bar speaks
the summary. Details and tuning:
[How to get spoken summaries from Claude Code](../guide/claude-code-voice.md).

**What next?**

- [How to fix hotkeys that do nothing](../guide/fix-permissions.md) — if step 5 didn't work
- [How to tune or disable live typing](../guide/live-typing.md)
- [Hotkeys and menu reference](../reference/index.md)
