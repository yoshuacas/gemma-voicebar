"""Image understanding: description, targeted Q&A, OCR."""
from pathlib import Path

from _common import generate, load

SAMPLE_URL = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"


def run(processor, model, image_ref, label, prompt, **kw):
    print(f"\n=== {label} ===")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "url": image_ref}
                if isinstance(image_ref, str) and image_ref.startswith("http")
                else {"type": "image", "path": str(image_ref)},
                {"type": "text", "text": prompt},
            ],
        }
    ]
    print(generate(processor, model, messages, **kw))


def main():
    processor, model = load()

    run(processor, model, SAMPLE_URL,
        "Describe (URL image)",
        "Describe this image in two sentences. What is unusual about it?",
        max_new_tokens=200)

    run(processor, model, SAMPLE_URL,
        "Targeted Q&A",
        "How many distinct colors of candy do you see, and which color is most common?",
        max_new_tokens=200)

    # Optional: drop your own image into samples/ and uncomment.
    local = Path(__file__).parent.parent / "samples" / "test.jpg"
    if local.exists():
        run(processor, model, local,
            f"Local image: {local.name}",
            "Describe this image. Read any visible text verbatim.",
            max_new_tokens=300)


if __name__ == "__main__":
    main()
