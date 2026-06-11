from __future__ import annotations

import re

_FENCE = re.compile(r"```.*?```", re.S)
_INLINE_CODE = re.compile(r"`([^`]*)`")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_BOLD_ITALIC = re.compile(r"(\*{1,3}|_{1,3})(\S(?:.*?\S)?)\1")
_HEADER = re.compile(r"^#{1,6}\s+", re.M)
_BULLET = re.compile(r"^\s*[-*+]\s+", re.M)
_TABLE_ROW = re.compile(r"^\|.*\|\s*$", re.M)
_PATH_REF = re.compile(r"\S+\.(?:py|md|toml|yml|yaml|json|sh|txt):\d+(?:-\d+)?")
_WS = re.compile(r"[ \t]+")


def clean_for_speech(text: str) -> str:
    """Strip markdown so TTS reads prose, not punctuation soup.

    Code fences and tables are summarized away rather than read; inline
    formatting keeps its content.
    """
    text = _FENCE.sub(" code omitted. ", text)
    text = _TABLE_ROW.sub("", text)
    text = _LINK.sub(r"\1", text)
    text = _INLINE_CODE.sub(r"\1", text)
    text = _BOLD_ITALIC.sub(r"\2", text)
    text = _HEADER.sub("", text)
    text = _BULLET.sub("", text)
    text = _PATH_REF.sub(lambda m: m.group(0).split(":")[0], text)
    text = _WS.sub(" ", text)
    text = re.sub(r"\n{2,}", ". ", text)
    text = text.replace("\n", " ")
    return re.sub(r"\s{2,}", " ", text).strip()
