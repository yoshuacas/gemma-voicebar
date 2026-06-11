PROJECT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)

.PHONY: help bar install-deps espeak

help:
	@echo "Targets:"
	@echo "  bar           Run the standalone gemma-voice-bar menu app"
	@echo "  install-deps  uv sync + editable installs"
	@echo "  espeak        brew install espeak-ng (Kokoro fallback)"

install-deps:
	cd $(PROJECT_DIR) && uv sync --extra bar
	cd $(PROJECT_DIR) && uv pip install -e packages/shared -e packages/voicebar

espeak:
	brew install espeak-ng

bar:
	cd $(PROJECT_DIR) && uv run python -m voicebar
