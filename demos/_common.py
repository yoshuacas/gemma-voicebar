"""Shared loader for Gemma 4 E4B-it on Apple Silicon (MPS)."""
from __future__ import annotations

import time
from functools import lru_cache

import torch
from transformers import AutoModelForCausalLM, AutoProcessor

MODEL_ID = "google/gemma-4-E4B-it"


def pick_device() -> tuple[str, torch.dtype]:
    if torch.backends.mps.is_available():
        return "mps", torch.bfloat16
    if torch.cuda.is_available():
        return "cuda", torch.bfloat16
    return "cpu", torch.float32


@lru_cache(maxsize=1)
def load():
    device, dtype = pick_device()
    print(f"[load] device={device} dtype={dtype}")
    t0 = time.time()
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype=dtype,
        device_map=device,
    )
    model.eval()
    print(f"[load] ready in {time.time() - t0:.1f}s")
    return processor, model


def generate(processor, model, messages, *, max_new_tokens=512, enable_thinking=False):
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
        enable_thinking=enable_thinking,
    ).to(model.device)

    input_len = inputs["input_ids"].shape[-1]
    t0 = time.time()
    with torch.inference_mode():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
    new_tokens = out[0, input_len:]
    elapsed = time.time() - t0
    text = processor.decode(new_tokens, skip_special_tokens=True)
    tps = new_tokens.shape[0] / elapsed if elapsed else 0.0
    print(f"[gen] {new_tokens.shape[0]} tok in {elapsed:.1f}s ({tps:.1f} tok/s)")
    return text
