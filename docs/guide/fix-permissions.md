# How to fix hotkeys that do nothing

**Goal:** Right Option or ⌃⌥S is pressed and nothing happens — no recording
indicator, no notification.

**You'll need:** to know which terminal app you launch gemma-voicebar from.

macOS attributes permissions to the *host application* of the process. When you
launch from Terminal, the grants live on Terminal — not on Python or the bar app.
If you switch terminals (say, Terminal → iTerm), you must grant everything again
for the new app.

## Checklist

Open **System Settings → Privacy & Security** and verify your terminal app is
enabled under all three panes:

| Pane | Symptom when missing |
|---|---|
| **Input Monitoring** | Hotkeys never fire; nothing happens at all |
| **Microphone** | Title flips to `⚠` and a "Microphone error" notification appears |
| **Accessibility** | Transcription works but no text appears (the synthesized ⌘V is blocked); "Paste blocked" notification |

## After changing a grant

1. Quit the app: menu bar `●` → **Quit**.
2. Relaunch: `make -C ops bar`.

Microphone takes effect immediately, but the `pynput` listeners only read
Input Monitoring and Accessibility state at startup — a relaunch is required.

## Still stuck

- Check you're testing in a normal text field. Password and other secure fields
  reject synthesized keystrokes by design; the text is left on the clipboard.
- Run from a foreground terminal and watch the log output: permission errors
  from the listeners print as `[hotkeys] ...` lines.
