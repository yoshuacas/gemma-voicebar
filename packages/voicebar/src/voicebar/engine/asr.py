from __future__ import annotations

import io
import time

import numpy as np
import soundfile as sf

import mlx_whisper

MODEL_REPO = "mlx-community/whisper-small-mlx-q4"
TARGET_SR = 16000


def warmup() -> None:
    silence = np.zeros(TARGET_SR, dtype=np.float32)
    mlx_whisper.transcribe(silence, path_or_hf_repo=MODEL_REPO, fp16=True)


def transcribe_wav_bytes(wav_bytes: bytes) -> str:
    samples, sr = sf.read(io.BytesIO(wav_bytes), dtype="float32", always_2d=False)
    return transcribe_samples(samples, sr)


def transcribe_samples(samples: np.ndarray, sr: int = TARGET_SR) -> str:
    if samples.ndim > 1:
        samples = samples.mean(axis=1)
    if sr != TARGET_SR:
        import scipy.signal as ss

        samples = ss.resample_poly(samples, TARGET_SR, sr).astype(np.float32)
    duration = len(samples) / TARGET_SR

    t0 = time.time()
    result = mlx_whisper.transcribe(
        samples,
        path_or_hf_repo=MODEL_REPO,
        fp16=True,
        language="en",
        condition_on_previous_text=False,
    )
    text = _clean_result(result)
    elapsed = time.time() - t0
    rtf = duration / elapsed if elapsed else 0.0
    print(f"[asr] {duration:.1f}s audio in {elapsed:.2f}s (rtf={rtf:.1f}x)", flush=True)
    return text


# Standard whisper hallucination heuristics: a repetition loop compresses
# extremely well (high compression_ratio); text invented over silence pairs
# high no_speech_prob with low avg_logprob.
COMPRESSION_RATIO_MAX = 2.4
NO_SPEECH_MAX = 0.6
LOGPROB_MIN = -1.0


def _clean_result(result: dict) -> str:
    segments = result.get("segments")
    if not segments:
        return (result.get("text") or "").strip()
    kept = []
    for seg in segments:
        if (seg.get("compression_ratio") or 0.0) > COMPRESSION_RATIO_MAX:
            continue
        if (
            (seg.get("no_speech_prob") or 0.0) > NO_SPEECH_MAX
            and (seg.get("avg_logprob") or 0.0) < LOGPROB_MIN
        ):
            continue
        kept.append(seg.get("text") or "")
    return "".join(kept).strip()
