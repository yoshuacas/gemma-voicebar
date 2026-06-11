from __future__ import annotations

import io
import threading

import sounddevice as sd
import soundfile as sf

_lock = threading.Lock()


def play_wav_bytes(data: bytes) -> None:
    samples, sr = sf.read(io.BytesIO(data), dtype="float32")
    with _lock:
        sd.stop()
        sd.play(samples, sr)
        sd.wait()


def play_async(data: bytes) -> None:
    t = threading.Thread(target=play_wav_bytes, args=(data,), daemon=True)
    t.start()
