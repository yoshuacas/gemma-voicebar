.PHONY: help install run smoke espeak docs

help:
	@echo "Targets:"
	@echo "  install   uv sync (creates venv, installs everything)"
	@echo "  run       Run the menu-bar app in the foreground"
	@echo "  smoke     In-process ASR + TTS engine smoke test"
	@echo "  espeak    brew install espeak-ng (Kokoro fallback)"
	@echo "  docs      Serve the documentation site locally"

install:
	uv sync

run:
	uv run python -m voicebar

smoke:
	uv run python -c "\
	from pathlib import Path; \
	from voicebar.engine import asr, tts; \
	print('ASR:', asr.transcribe_wav_bytes(Path('samples/Example.ogg').read_bytes())); \
	samples, sr = tts.synthesize('engine smoke test passed'); \
	print('TTS:', round(len(samples)/sr, 2), 'seconds at', sr, 'Hz')"

espeak:
	brew install espeak-ng

docs:
	uv run --group docs mkdocs serve
