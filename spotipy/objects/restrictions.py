from __future__ import annotations

import enum
from typing import TypedDict, Literal


__all__ = (
    "RestrictionsReason",
    "RestrictionsData",
    "Restrictions"
)


class RestrictionsReason(enum.Enum):
    MARKET = "market"
    PRODUCT = "product"
    EXPLICIT = "explicit"


class RestrictionsData(TypedDict):
    reason: Literal["market", "product", "explicit"]


class Restrictions:

    def __init__(self, data: RestrictionsData) -> None:
        self.reason: RestrictionsReason = RestrictionsReason(data["reason"])

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: reason={self.reason}>"
