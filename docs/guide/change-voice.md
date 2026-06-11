# How to change the speaking voice

**Goal:** pick a different Kokoro voice for the ⌃⌥S speak-selection feature.

Menu bar `●` → **Voice** → choose one:

| Voice | Description |
|---|---|
| `af_heart` | American female (default) |
| `af_bella` | American female |
| `af_nicole` | American female |
| `af_sarah` | American female |
| `am_michael` | American male |
| `am_adam` | American male |
| `bf_emma` | British female |
| `bm_george` | British male |

The choice takes effect on the next ⌃⌥S press and persists across restarts in
`~/.config/codewithvoice/config.json` as `"voice"`.

All voices are American/British English; the Kokoro pipeline is initialized
with `lang_code="a"` (American English G2P). Other languages are not exposed
in the UI.
