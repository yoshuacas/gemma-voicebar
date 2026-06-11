"""Video understanding via frame sequences. Clip ≤ 60s."""
from pathlib import Path

from _common import generate, load

SAMPLES = Path(__file__).parent.parent / "samples"


def run(processor, model, video_path, label, prompt, **kw):
    print(f"\n=== {label} :: {video_path.name} ===")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "video", "path": str(video_path)},
                {"type": "text", "text": prompt},
            ],
        }
    ]
    print(generate(processor, model, messages, **kw))


def main():
    processor, model = load()

    clips = sorted(p for p in SAMPLES.glob("*") if p.suffix.lower() in {".mp4", ".mov", ".webm", ".mkv"})
    if not clips:
        print(f"No video samples found in {SAMPLES}/. Drop a .mp4 (≤60s) and rerun.")
        return

    for clip in clips:
        run(processor, model, clip, "Describe scene",
            "What is happening in this video? Describe the setting, actions, and any audible speech.",
            max_new_tokens=400)

        run(processor, model, clip, "Timeline summary",
            "Give a chronological summary of events with rough timestamps (e.g. 0-5s, 5-10s).",
            max_new_tokens=400)


if __name__ == "__main__":
    main()
