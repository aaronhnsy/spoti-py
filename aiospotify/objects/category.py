# Future
from __future__ import annotations

# My stuff
from aiospotify import objects
from aiospotify.typings.objects import CategoryData


__all__ = (
    "Category",
)


class Category:

    def __init__(self, data: CategoryData) -> None:
        self.href = data["href"]
        self.icons = [objects.Image(image) for image in data["icons"]]
        self.id = data["id"]
        self.name = data["name"]

    def __repr__(self) -> str:
        return f"<aiospotify.Category id='{self.id}' name='{self.name}'>"
