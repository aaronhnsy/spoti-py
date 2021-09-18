# Future
from __future__ import annotations

# My stuff
from typings.objects import BaseObjectData, PagingObjectData


__all__ = (
    "BaseObject",
    "PagingObject",
)


class BaseObject:

    def __init__(self, data: BaseObjectData) -> None:

        self.href = data["href"]
        self.id = data["id"]
        self.name = data.get("name")
        self.type = data["type"]
        self.uri = data["uri"]

    def __repr__(self) -> str:
        return f"<aiospotify.BaseObject id='{self.id}', name='{self.name}'>"


class PagingObject:

    def __init__(self, data: PagingObjectData) -> None:

        self.href = data["href"]
        self.items = data["items"]
        self.limit = data["limit"]
        self.next = data["next"]
        self.offset = data["offset"]
        self.previous = data["previous"]
        self.total = data["total"]

    def __repr__(self) -> str:
        return f"<spotify.PagingObject total={self.total}, limit={self.limit}, offset={self.offset}>"
