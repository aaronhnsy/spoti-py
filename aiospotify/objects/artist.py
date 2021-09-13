# Future
from __future__ import annotations

# My stuff
from aiospotify import objects


__all__ = (
    "SimpleArtist",
    "Artist",
)


class SimpleArtist(objects.BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.external_urls: dict[str | None, str | None] = data.get("external_urls", {})

    def __repr__(self) -> str:
        return f"<spotify.SimpleArtist name=\"{self.name}\" id=\"{self.id}\" url=\"<{self.url}>\">"

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class Artist(objects.BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.external_urls: dict[str | None, str | None] = data.get("external_urls", {})
        self.followers: objects.Followers = objects.Followers(data.get("followers"))
        self.genres: list[str | None] = data.get("genres", [])
        self.images: list[objects.Image | None] = [objects.Image(image_data) for image_data in data.get("images", [])]
        self.popularity: int = data.get("popularity", 0)

    def __repr__(self) -> str:
        return f"<spotify.Artist name=\"{self.name}\" id=\"{self.id}\" url=\"<{self.url}>\">"

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
