from __future__ import annotations

from typing import TypeVar, Generic

from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BaseObjectData",
    "BaseObject",
    "PagingObjectData",
    "PagingObject",
    "AlternativePagingObjectData",
    "AlternativePagingObject",
)


T = TypeVar("T")


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


class PagingObjectData(TypedDict, Generic[T]):
    href: str
    items: list[T]
    limit: int
    next: str | None
    offset: int
    previous: str | None
    total: int


class PagingObject(Generic[T]):

    def __init__(self, data: PagingObjectData[T]) -> None:
        self.href: str = data["href"]
        self.items: list[T] = data["items"]
        self.limit: int = data["limit"]
        self.next: str | None = data["next"]
        self.offset: int = data["offset"]
        self.previous: str | None = data["previous"]
        self.total: int = data["total"]

    def __repr__(self) -> str:
        return f"<spotify.PagingObject total={self.total}, limit={self.limit}, offset={self.offset}>"


class AlternativePagingObjectData(TypedDict, Generic[T]):
    href: str
    items: list[T]
    limit: int
    next: str | None
    before: NotRequired[str]
    after: str


class AlternativePagingObject(Generic[T]):

    def __init__(self, data: AlternativePagingObjectData[T]) -> None:
        self.href: str = data["href"]
        self.items: list[T] = data["items"]
        self.limit: int = data["limit"]
        self.next: str | None = data["next"]
        self.before: str | None = data.get("before")
        self.after: str = data["after"]

    def __repr__(self) -> str:
        return f"<spotify.AlternativePagingObject limit={self.limit}, before={self.before}, after={self.after}>"
