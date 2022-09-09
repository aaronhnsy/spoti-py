from __future__ import annotations

from typing import TypedDict


__all__ = (
    "ImageData",
    "Image",
)


class ImageData(TypedDict):
    url: str
    width: int
    height: int


class Image:

    def __init__(self, data: ImageData) -> None:
        self.url: str = data["url"]
        self.width: int = data["width"]
        self.height: int = data["height"]

    def __repr__(self) -> str:
        return f"<spotipy.Image url='<{self.url}>', width={self.width}, height={self.height}>"
