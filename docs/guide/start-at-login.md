# How to start gemma-voicebar at login

**Goal:** have the bar running after every reboot without keeping a terminal
window open.

There is no code-signed `.app` bundle yet, so the practical option is a small
launcher script registered as a Login Item.

## 1. Create a launcher

```bash
cat > ~/bin/gemma-voicebar-launch.command <<'EOF'
#!/bin/zsh
cd /path/to/gemma-voicebar
exec uv run python -m voicebar
EOF
chmod +x ~/bin/gemma-voicebar-launch.command
```

Replace `/path/to/gemma-voicebar` with your clone location.

## 2. Register it

**System Settings → General → Login Items & Extensions → Open at Login → +** and
select the `.command` file.

## Caveat: permissions follow the host app

`.command` files open in Terminal, so the Microphone / Accessibility /
Input Monitoring grants must be on **Terminal** (see
[How to fix hotkeys that do nothing](fix-permissions.md)). If you normally run
from iTerm, you'll be granting a second set for Terminal.

A proper code-signed `.app` bundle — which would own its permissions and skip
the terminal entirely — is on the roadmap but not built yet.
