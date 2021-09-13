# Future
from __future__ import annotations

# Standard Library
from typing import Optional

# My stuff
from aiospotify import objects


class SimpleArtist(objects.BaseObject):

    __slots__ = ('external_urls', )

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.external_urls: dict[Optional[str], Optional[str]] = data.get('external_urls', {})

    def __repr__(self) -> str:
        return f'<spotify.SimpleArtist name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')


class Artist(objects.BaseObject):

    __slots__ = 'external_urls', 'followers', 'genres', 'images', 'popularity'

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.external_urls: dict[Optional[str], Optional[str]] = data.get('external_urls', {})
        self.followers: objects.Followers = objects.Followers(data.get('followers'))
        self.genres: list[Optional[str]] = data.get('genres', [])
        self.images: list[Optional[objects.Image]] = [objects.Image(image_data) for image_data in data.get('images', [])]
        self.popularity: int = data.get('popularity', 0)

    def __repr__(self) -> str:
        return f'<spotify.Artist name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')
