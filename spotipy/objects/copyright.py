from __future__ import annotations

from typing import TypedDict

from .enums import CopyrightType


__all__ = (
    "CopyrightData",
    "Copyright",
)


class CopyrightData(TypedDict):
    text: str
    type: str


class Copyright:

    def __init__(self, data: CopyrightData) -> None:
        self.text = data["text"]
        self.type = CopyrightType(data["type"])

    def __repr__(self) -> str:
        return f"<spotipy.Copyright type={self.type!r}>"
