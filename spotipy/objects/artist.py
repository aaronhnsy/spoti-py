from __future__ import annotations

from spotipy import objects
from spotipy.typings.objects import ArtistData, SimpleArtistData


__all__ = (
    "SimpleArtist",
    "Artist",
)


class SimpleArtist(objects.BaseObject):

    def __init__(self, data: SimpleArtistData) -> None:
        super().__init__(data)

        self.external_urls = data["external_urls"]

    def __repr__(self) -> str:
        return f"<spotipy.SimpleArtist id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class Artist(SimpleArtist):

    def __init__(self, data: ArtistData) -> None:
        super().__init__(data)

        self.external_urls = data["external_urls"]
        self.followers = objects.Followers(data["followers"])
        self.genres = data["genres"]
        self.images = [objects.Image(image) for image in data["images"]]
        self.popularity = data["popularity"]

    def __repr__(self) -> str:
        return f"<spotipy.Artist id='{self.id}', name='{self.name}'>"
