from __future__ import annotations

from typing import TypedDict, Any

from typing_extensions import NotRequired


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
    name: NotRequired[str]
    type: str
    uri: str


class BaseObject:

    def __init__(self, data: BaseObjectData) -> None:
        self.href: str = data["href"]
        self.id: str = data["id"]
        self.name: str | None = data.get("name")
        self.type: str = data["type"]
        self.uri: str = data["uri"]

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
        self.href: str = data["href"]
        self.items: list[Any] = data["items"]
        self.limit: int = data["limit"]
        self.next: str | None = data["next"]
        self.offset: int = data["offset"]
        self.previous: str | None = data["previous"]
        self.total: int = data["total"]

    def __repr__(self) -> str:
        return f"<spotify.PagingObject total={self.total}, limit={self.limit}, offset={self.offset}>"


class AlternativePagingObjectData(TypedDict):
    href: str
    items: list[Any]
    limit: int
    next: str | None
    before: NotRequired[str]
    after: str


class AlternativePagingObject:

    def __init__(self, data: AlternativePagingObjectData) -> None:
        self.href: str = data["href"]
        self.items: list[Any] = data["items"]
        self.limit: int = data["limit"]
        self.next: str | None = data["next"]
        self.before: str | None = data.get("before")
        self.after: str = data["after"]

    def __repr__(self) -> str:
        return f"<spotify.AlternativePagingObject limit={self.limit}, before={self.before}, after={self.after}>"
