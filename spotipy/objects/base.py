from __future__ import annotations

from typing import TypedDict, Any


__all__ = (
    "BaseObjectData",
    "BaseObject",
    "PagingObjectData",
    "PagingObject",
    "AlternativePagingObjectData",
    "AlternativePagingObject",
)


class BaseObjectData(TypedDict):
    href: str
    id: str
    name: str
    type: str
    uri: str


class BaseObject:

    def __init__(self, data: BaseObjectData) -> None:
        self.href = data["href"]
        self.id = data["id"]
        self.name = data.get("name")
        self.type = data["type"]
        self.uri = data["uri"]

    def __repr__(self) -> str:
        return f"<spotipy.BaseObject id='{self.id}', name='{self.name}'>"


class PagingObjectData(TypedDict):
    href: str
    items: list[Any]
    limit: int
    next: str | None
    offset: int
    previous: str | None
    total: int


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


class AlternativePagingObjectData(TypedDict):
    href: str
    items: list[Any]
    limit: int
    next: str | None
    before: str
    after: str


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
