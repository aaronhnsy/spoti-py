from __future__ import annotations

from .base import BaseObject, BaseObjectData
from .common import ExternalUrlsData
from .followers import Followers, FollowersData
from .image import Image, ImageData


__all__ = (
    "SimpleArtistData",
    "SimpleArtist",
    "ArtistData",
    "Artist",
)


class SimpleArtistData(BaseObjectData):
    external_urls: ExternalUrlsData


class SimpleArtist(BaseObject):

    def __init__(self, data: SimpleArtistData) -> None:
        super().__init__(data)

        self.external_urls = data["external_urls"]

    def __repr__(self) -> str:
        return f"<spotipy.SimpleArtist id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class ArtistData(SimpleArtistData):
    followers: FollowersData
    genres: list[str]
    images: list[ImageData]
    popularity: int


class Artist(SimpleArtist):

    def __init__(self, data: ArtistData) -> None:
        super().__init__(data)

        self.external_urls = data["external_urls"]
        self.followers = Followers(data["followers"])
        self.genres = data["genres"]
        self.images = [Image(image) for image in data["images"]]
        self.popularity = data["popularity"]

    def __repr__(self) -> str:
        return f"<spotipy.Artist id='{self.id}', name='{self.name}'>"
