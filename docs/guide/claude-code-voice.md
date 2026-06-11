# How to get spoken summaries from Claude Code

**Goal:** after every Claude Code turn, hear a one-sentence spoken summary of
what it did — instead of reading multi-hundred-word responses.

**You'll need:** the bar app running, and the `claude` CLI on your PATH.

## How it works

```text
Claude finishes a turn
  → Stop hook runs hooks/speak-summary.py (async, non-blocking)
  → summarizes the response to one sentence via `claude -p --model haiku`
  → drops it in ~/.local/state/codewithvoice/speak/
  → the bar app's spool watcher speaks it through Kokoro
```

If the summarizer call fails (no `claude` CLI, no credits, timeout), the hook
falls back to speaking the first two sentences of the response, markdown
stripped.

## Enable it for a project

Copy `hooks/speak-summary.py` into your project and register the hook in the
project's `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "python3 \"$CLAUDE_PROJECT_DIR\"/hooks/speak-summary.py",
        "async": true,
        "timeout": 60
      }
    ]
  }
}
```

The hook is stdlib-only Python — it does not need this project's virtualenv.
Register it in `~/.claude/settings.json` instead to enable it for every
project (use an absolute path to the script in that case).

## Speak anything from the shell

The same spool powers a general-purpose command:

```bash
codewithvoice-speak "build finished"
make test 2>&1 | tail -1 | codewithvoice-speak
```

Text is cleaned for speech (markdown stripped, code blocks replaced with
"code omitted") and spoken by the already-loaded Kokoro — the bar app must be
running with `●` in the menu bar.

## Tuning

- **Summary length/style** — edit `PROMPT` in `hooks/speak-summary.py`.
- **Summarizer model** — `SUMMARY_MODEL` in the same file (default `haiku`:
  fast and cheap; each summary costs roughly 500 input tokens).
- **Voice** — the spool uses the same voice as ⌃⌥S (menu bar → Voice).
