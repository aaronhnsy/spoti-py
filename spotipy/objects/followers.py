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
        self.href = data["href"]
        self.total = data["total"]

    def __repr__(self) -> str:
        return f"<spotipy.Followers total={self.total}>"
