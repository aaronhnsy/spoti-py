# Future
from __future__ import annotations

# Standard Library
from typing import Literal, Optional

# My stuff
from aiospotify import objects


class AlbumRestriction:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.reason: Literal['market', 'product', 'explicit'] = data.get('reason')

    def __repr__(self) -> str:
        return f'<spotify.AlbumRestriction reason=\'{self.reason}\'>'


class SimpleAlbum(objects.BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.album_type: Literal['album', 'single', 'compilation', 'unknown'] = data.get('album_type', 'unknown')
        self.artists: list[Optional[objects.SimpleArtist]] = [objects.SimpleArtist(artist_data) for artist_data in data.get('artists', [])]
        self.available_markets: list[Optional[str]] = data.get('available_markets', [])
        self.external_urls: dict[Optional[str], Optional[str]] = data.get('external_urls', {})
        self.images: list[Optional[objects.Image]] = [objects.Image(image_data) for image_data in data.get('images', [])]
        self.release_date: Optional[str] = data.get('release_date')
        self.release_data_precision: Literal['year', 'month', 'day', 'unknown'] = data.get('release_date_precision', 'unknown')
        self.total_tracks: int = data.get('total_tracks', 0)

    def __repr__(self) -> str:
        return f'<spotify.SimpleAlbum name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\' total_tracks=\'{self.total_tracks}\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')

    @property
    def restriction(self) -> Optional[AlbumRestriction]:
        if (restriction_data := self.data.get('restrictions')) is None:
            return None
        return AlbumRestriction(restriction_data)


class Album(objects.BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.album_type: Literal['album', 'single', 'compilation', 'unknown'] = data.get('album_type', 'unknown')
        self.artists: list[Optional[objects.SimpleArtist]] = [objects.SimpleArtist(artist_data) for artist_data in data.get('artists', [])]
        self.available_markets: list[Optional[str]] = data.get('available_markets', [])
        self.copyrights: list[Optional[objects.Copyright]] = [objects.Copyright(copyright_data) for copyright_data in data.get('copyrights', {})]
        self.external_ids: dict[Optional[str], Optional[str]] = data.get('external_ids', {})
        self.external_urls: dict[Optional[str], Optional[str]] = data.get('external_urls', {})
        self.genres: list[Optional[str]] = data.get('genres', [])
        self.images: list[Optional[objects.Image]] = [objects.Image(image_data) for image_data in data.get('images', [])]
        self.label: Optional[str] = data.get('label')
        self.popularity: int = data.get('popularity', 0)
        self.release_date: Optional[str] = data.get('release_date')
        self.release_data_precision: Literal['year', 'month', 'day', 'unknown'] = data.get('release_date_precision', 'unknown')
        self.total_tracks: int = data.get('total_tracks', 0)

        self._tracks_paging = objects.PagingObject(data.get('tracks', []))
        self.tracks: list[Optional[objects.SimpleTrack]] = [objects.SimpleTrack(track_data) for track_data in self._tracks_paging.items]

    def __repr__(self) -> str:
        return f'<spotify.Album name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\' total_tracks=\'{self.total_tracks}\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')
