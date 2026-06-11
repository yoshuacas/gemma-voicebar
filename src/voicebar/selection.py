from __future__ import annotations

import time

import Quartz
from AppKit import NSPasteboard, NSPasteboardTypeString
from pynput.keyboard import Controller, Key

from .inject import _restore, _snapshot

_kb = Controller()

_MODIFIER_MASK = (
    Quartz.kCGEventFlagMaskControl
    | Quartz.kCGEventFlagMaskAlternate
    | Quartz.kCGEventFlagMaskShift
)


def _wait_modifiers_released(timeout: float = 1.0) -> None:
    """Block until the physical Ctrl/Option/Shift keys are up.

    The speak hotkey fires on key-DOWN, so the user is still holding ⌃⌥ when
    we synthesize ⌘C. macOS merges physical modifier state into the event,
    turning it into ⌘⌃⌥C — which matches no Copy command in most apps
    (terminals especially), so the grab silently fails.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        flags = Quartz.CGEventSourceFlagsState(
            Quartz.kCGEventSourceStateHIDSystemState
        )
        if not (flags & _MODIFIER_MASK):
            return
        time.sleep(0.02)


def grab_selection(timeout: float = 0.3) -> str | None:
    """Synthesize Cmd+C, read pasteboard, restore previous contents.

    Returns the selected text or None if nothing changed (no selection).
    """
    _wait_modifiers_released()
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
