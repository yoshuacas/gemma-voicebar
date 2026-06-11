from __future__ import annotations

import time

from AppKit import NSPasteboard, NSPasteboardItem, NSPasteboardTypeString
from pynput.keyboard import Controller, Key

_kb = Controller()


def _snapshot(pb: NSPasteboard) -> list[tuple[list[str], dict[str, bytes]]]:
    snap: list[tuple[list[str], dict[str, bytes]]] = []
    for item in pb.pasteboardItems() or []:
        types = list(item.types() or [])
        data = {}
        for t in types:
            d = item.dataForType_(t)
            if d is not None:
                data[t] = bytes(d)
        snap.append((types, data))
    return snap


def _restore(pb: NSPasteboard, snap: list[tuple[list[str], dict[str, bytes]]]) -> None:
    pb.clearContents()
    items = []
    for types, data in snap:
        item = NSPasteboardItem.alloc().init()
        for t in types:
            d = data.get(t)
            if d is None:
                continue
            from AppKit import NSData
            ns = NSData.dataWithBytes_length_(d, len(d))
            item.setData_forType_(ns, t)
        items.append(item)
    if items:
        pb.writeObjects_(items)


def _send_cmd_v() -> None:
    with _kb.pressed(Key.cmd):
        _kb.press("v")
        _kb.release("v")


def type_text(text: str) -> bool:
    """Type `text` as synthesized keystrokes (no clipboard involvement).

    Returns False if pynput could not synthesize input (e.g. Accessibility
    permission missing or a secure field rejecting events).
    """
    if not text:
        return True
    try:
        _kb.type(text)
    except Exception:
        return False
    return True


def inject_text(text: str) -> bool:
    """Place `text` on the pasteboard, paste it, then restore the previous contents.

    Returns True on success, False if pynput could not synthesize the keystroke
    (e.g. Accessibility permission missing).
    """
    if not text:
        return True
    pb = NSPasteboard.generalPasteboard()
    snap = _snapshot(pb)
    pb.clearContents()
    pb.setString_forType_(text, NSPasteboardTypeString)
    try:
        _send_cmd_v()
    except Exception:
        return False
    time.sleep(0.08)
    try:
        _restore(pb, snap)
    except Exception:
        pass
    return True
