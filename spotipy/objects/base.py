from __future__ import annotations

from spotipy.typings.objects import AlternativePagingObjectData, BaseObjectData, PagingObjectData


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
        return f"<spotipy.BaseObject id='{self.id}', name='{self.name}'>"


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


class AlternativePagingObject:

    def __init__(self, data: AlternativePagingObjectData) -> None:
        self.href = data["href"]
        self.items = data["items"]
        self.limit = data["limit"]
        self.next = data["next"]
        self.after = data["after"]
        self.before = data.get("before")

    def __repr__(self) -> str:
        return f"<spotify.AlternativePagingObject limit={self.limit}, before={self.before}, after={self.after}>"
