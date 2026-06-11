"""Audio: ASR (transcribe) and translation. Audio clip ≤ 30s."""
from pathlib import Path

from _common import generate, load

SAMPLES = Path(__file__).parent.parent / "samples"


def run(processor, model, audio_path, label, prompt, **kw):
    print(f"\n=== {label} :: {audio_path.name} ===")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "path": str(audio_path)},
                {"type": "text", "text": prompt},
            ],
        }
    ]
    print(generate(processor, model, messages, **kw))


def main():
    processor, model = load()

    clips = sorted(p for p in SAMPLES.glob("*") if p.suffix.lower() in {".wav", ".mp3", ".flac", ".m4a", ".ogg"})
    if not clips:
        print(f"No audio samples found in {SAMPLES}/. Drop a .wav or .mp3 (≤30s) and rerun.")
        return

    for clip in clips:
        run(processor, model, clip, "Transcribe",
            "Transcribe this audio verbatim.",
            max_new_tokens=400)

        run(processor, model, clip, "Translate to English",
            "Translate the speech in this audio into natural English.",
            max_new_tokens=400)

        run(processor, model, clip, "Describe non-speech",
            "Beyond any speech, describe other sounds: tone, background, mood, language.",
            max_new_tokens=200)


if __name__ == "__main__":
    main()
