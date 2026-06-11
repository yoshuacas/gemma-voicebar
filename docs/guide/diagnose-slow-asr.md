# How to diagnose slow transcription

**Goal:** transcription that normally finishes in well under a second is taking
several seconds, or live typing lags far behind.

## 1. Read the per-pass timing

Run the bar from a foreground terminal (`make run`) and dictate. Every
ASR pass logs a line:

```text
[asr] 6.1s audio in 0.45s (rtf=13.6x)
```

`rtf` is the realtime factor — audio seconds per compute second. Healthy values
on an M2 Pro are 9–30×. Sustained values below ~3× mean something is wrong.

## 2. Check for memory-pressure thrashing

The usual culprit on a 32 GB machine is the model being paged out by other
memory-hungry apps:

```bash
ps -o rss,vsz,comm -p "$(pgrep -f 'python -m voicebar')"
```

If RSS (resident memory) is drastically smaller than the model's working set —
tens of MB resident — the model is swapped out and every pass pays a paging
penalty. Inference can degrade 10–50×.

**Fix:** free RAM. Close the heavy apps (browsers with many tabs, IDEs, other
ML processes) or reboot. Do **not** try to tune inference settings — the model
isn't slow, it's paged out.

## 3. One-off slow first pass is normal

The first pass after launch (and the first pass of each dictation after a long
idle) is often several times slower while caches warm. Consecutive passes speed
up sharply — this needs no action.
