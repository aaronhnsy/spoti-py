# Future
from __future__ import annotations

# My stuff
from spotipy import objects
from spotipy.typings.objects import ShowData


__all__ = (
    "Show",
)


class Show(objects.BaseObject):

    def __init__(self, data: ShowData) -> None:
        super().__init__(data)

        self.available_markets = data.get("available_markets")
        self.copyrights = [objects.Copyright(copyright) for copyright in data["copyrights"]]
        self.description = data["description"]
        self.explicit = data["explicit"]
        self.external_urls = data["external_urls"]
        self.html_description = data["html_description"]
        self.images = [objects.Image(image) for image in data["images"]]
        self.is_externally_hosted = data["is_externally_hosted"]
        self.languages = data["languages"]
        self.media_type = data["media_type"]
        self.publisher = data["publisher"]
        self.total_episodes = data["total_episodes"]

    def __repr__(self) -> str:
        return f"<spotipy.Show id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
