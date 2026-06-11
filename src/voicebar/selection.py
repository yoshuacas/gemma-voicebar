from __future__ import annotations

import time

from AppKit import NSPasteboard, NSPasteboardTypeString
from pynput.keyboard import Controller, Key

from .inject import _restore, _snapshot

_kb = Controller()


def grab_selection(timeout: float = 0.3) -> str | None:
    """Synthesize Cmd+C, read pasteboard, restore previous contents.

    Returns the selected text or None if nothing changed (no selection).
    """
    pb = NSPasteboard.generalPasteboard()
    snap = _snapshot(pb)
    pb.clearContents()
    cleared_count = pb.changeCount()
    try:
        with _kb.pressed(Key.cmd):
            _kb.press("c")
            _kb.release("c")
    except Exception:
        _restore(pb, snap)
        return None

    # changeCount moves off the post-clear value only once the frontmost app
    # actually processes the Cmd+C. No selection -> no copy -> timeout -> None.
    deadline = time.time() + timeout
    text: str | None = None
    while time.time() < deadline:
        if pb.changeCount() == cleared_count:
            time.sleep(0.02)
            continue
        text = pb.stringForType_(NSPasteboardTypeString)
        break

    _restore(pb, snap)
    if text and text.strip():
        return str(text)
    return None
