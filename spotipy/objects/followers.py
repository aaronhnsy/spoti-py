from __future__ import annotations

from typing import TypedDict


__all__ = (
    "FollowersData",
    "Followers",
)


class FollowersData(TypedDict):
    href: str | None
    total: int


class Followers:

    def __init__(self, data: FollowersData) -> None:
        self.href: str | None = data["href"]
        self.total: int = data["total"]

    def __repr__(self) -> str:
        return f"<spotipy.Followers total={self.total}>"
