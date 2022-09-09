from __future__ import annotations

from .base import BaseObject, BaseObjectData
from .common import ExternalURLs
from .copyright import Copyright, CopyrightData
from .image import Image, ImageData


__all__ = (
    "ShowData",
    "Show",
)


class ShowData(BaseObjectData):
    available_markets: list[str]
    copyrights: list[CopyrightData]
    description: str
    explicit: bool
    external_urls: ExternalURLs
    html_description: str
    images: list[ImageData]
    is_externally_hosted: bool
    languages: list[str]
    media_type: str
    publisher: str
    total_episodes: int


class Show(BaseObject):

    def __init__(self, data: ShowData) -> None:
        super().__init__(data)

        self.available_markets: list[str] = data.get("available_markets")
        self.copyrights: list[Copyright] = [Copyright(copyright) for copyright in data["copyrights"]]
        self.description: str = data["description"]
        self.explicit: bool = data["explicit"]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.html_description: str = data["html_description"]
        self.images: list[Image] = [Image(image) for image in data["images"]]
        self.is_externally_hosted: bool = data["is_externally_hosted"]
        self.languages: list[str] = data["languages"]
        self.media_type: str = data["media_type"]
        self.publisher: str = data["publisher"]
        self.total_episodes: int = data["total_episodes"]

    def __repr__(self) -> str:
        return f"<spotipy.Show id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
