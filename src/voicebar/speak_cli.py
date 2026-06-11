"""`codewithvoice-speak` — queue text for the running bar app to speak.

Usage:
    codewithvoice-speak "hello there"
    some-command | codewithvoice-speak
"""

from __future__ import annotations

import sys

from .spool import submit


def main() -> None:
    args = sys.argv[1:]
    text = " ".join(args) if args else sys.stdin.read()
    if not text.strip():
        sys.exit("codewithvoice-speak: no text given (args or stdin)")
    submit(text)


if __name__ == "__main__":
    main()
