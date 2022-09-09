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
        self.href = data["href"]
        self.icons = [Image(image) for image in data["icons"]]
        self.id = data["id"]
        self.name = data["name"]

    def __repr__(self) -> str:
        return f"<spotipy.Category id='{self.id}' name='{self.name}'>"
