"""Text-only smoke test: standard answer vs thinking-mode answer."""
from _common import generate, load


def main():
    processor, model = load()

    prompt = (
        "A train leaves city A at 9:00 AM going 80 km/h. Another leaves city B "
        "at 10:00 AM going 100 km/h toward A. The cities are 500 km apart. "
        "When and where do they meet?"
    )
    messages = [
        {"role": "system", "content": "You are a careful, concise assistant."},
        {"role": "user", "content": prompt},
    ]

    print("\n=== Without thinking ===")
    print(generate(processor, model, messages, max_new_tokens=400))

    print("\n=== With thinking ===")
    print(generate(processor, model, messages, max_new_tokens=900, enable_thinking=True))


if __name__ == "__main__":
    main()
