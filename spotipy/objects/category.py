from __future__ import annotations

from typing import TypedDict

from .image import Image, ImageData


__all__ = (
    "CategoryData",
    "Category",
)


class CategoryData(TypedDict):
    href: str
    icons: list[ImageData]
    id: str
    name: str


class Category:

    def __init__(self, data: CategoryData) -> None:
        self.href: str = data["href"]
        self.icons: list[Image] = [Image(image) for image in data["icons"]]
        self.id: str = data["id"]
        self.name: str = data["name"]

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: id='{self.id}', name='{self.name}'>"
