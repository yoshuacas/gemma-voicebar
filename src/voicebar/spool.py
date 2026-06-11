from __future__ import annotations

import threading
import uuid
from pathlib import Path
from typing import Callable

# Other processes (CLI, editor hooks) request speech by dropping UTF-8 .txt
# files here; the bar app watches and speaks them. File-based on purpose:
# no daemon, no socket, and writers need zero dependencies.
SPOOL_DIR = Path.home() / ".local" / "state" / "codewithvoice" / "speak"


def submit(text: str) -> Path:
    """Queue `text` to be spoken by a running bar app. Stdlib-only."""
    SPOOL_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SPOOL_DIR / f".{uuid.uuid4().hex}.tmp"
    tmp.write_text(text, encoding="utf-8")
    final = tmp.with_name(tmp.name[1:-4] + ".txt")
    tmp.rename(final)  # atomic: watcher never sees a partial file
    return final


class SpoolWatcher:
    def __init__(self, on_text: Callable[[str], None], interval: float = 0.5) -> None:
        self._on_text = on_text
        self._interval = interval
        self._stop_evt = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        SPOOL_DIR.mkdir(parents=True, exist_ok=True)
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_evt.set()
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def _loop(self) -> None:
        while not self._stop_evt.wait(self._interval):
            try:
                files = sorted(SPOOL_DIR.glob("*.txt"), key=lambda p: p.stat().st_mtime)
            except OSError:
                continue
            for path in files:
                try:
                    text = path.read_text(encoding="utf-8")
                    path.unlink()
                except OSError:
                    continue
                if not text.strip():
                    continue
                try:
                    self._on_text(text)
                except Exception as e:  # noqa: BLE001
                    print(f"[spool] speak failed: {e}", flush=True)
