from __future__ import annotations

import enum
from typing import TypedDict, Literal


__all__ = (
    "CopyrightType",
    "CopyrightData",
    "Copyright",
)


class CopyrightType(enum.Enum):
    NORMAL = "C"
    PERFORMANCE = "P"


class CopyrightData(TypedDict):
    text: str
    type: Literal["C", "P"]


class Copyright:

    def __init__(self, data: CopyrightData) -> None:
        self.text: str = data["text"]
        self.type: CopyrightType = CopyrightType(data["type"])

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: type={self.type!r}>"
