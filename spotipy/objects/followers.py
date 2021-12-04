# Future
from __future__ import annotations

# My stuff
from spotipy.typings.objects import FollowersData


__all__ = (
    "Followers",
)


class Followers:

    def __init__(self, data: FollowersData) -> None:
        self.href = data["href"]
        self.total = data["total"]

    def __repr__(self) -> str:
        return f"<spotipy.Followers total={self.total}>"
