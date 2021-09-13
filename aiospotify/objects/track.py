# Future
from __future__ import annotations

# Standard Library
from typing import Literal

# My stuff
from aiospotify.objects import BaseObject, Image, SimpleAlbum, SimpleArtist, User


__all__ = (
    "TrackRestriction",
    "SimpleTrack",
    "Track",
    "PlaylistTrack"
)


class TrackRestriction:

    def __init__(self, data: dict) -> None:

        self.data = data

        self.reason: Literal['market', 'product', 'explicit'] = data.get('reason')

    def __repr__(self) -> str:
        return f'spotify.TrackRestriction reason=\'{self.reason}\''


class SimpleTrack(BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.artists: list[SimpleArtist | None] = [SimpleArtist(artist_data) for artist_data in data.get('artists', [])]
        self.available_markets: list[str | None] = data.get('available_markets', [])
        self.disc_number: int = data.get('disc_number', 0)
        self.duration: int = data.get('duration_ms', 0)
        self.is_explicit: bool = data.get('explicit', False)
        self.external_urls: dict[str | None, str | None] = data.get('external_urls', {})
        self.is_local: bool = data.get('is_local', False)
        self.preview_url: str | None = data.get('preview_url')
        self.track_number: int = data.get('track_number', 0)

    def __repr__(self) -> str:
        return f'<spotify.SimpleTrack name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\'>'

    @property
    def url(self) -> str | None:
        return self.external_urls.get('spotify')

    @property
    def restriction(self) -> TrackRestriction | None:

        if restriction := (self.data.get('restrictions') is None):
            return None
        return TrackRestriction(restriction)


class Track(BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.album: SimpleAlbum = SimpleAlbum(data.get('album'))
        self.artists: list[SimpleArtist | None] = [SimpleArtist(artist_data) for artist_data in data.get('artists', [])]
        self.available_markets: list[str | None] = data.get('available_markets', [])
        self.disc_number: int = data.get('disc_number', 0)
        self.duration: int = data.get('duration_ms', 0)
        self.is_explicit: bool = data.get('explicit', False)
        self.external_ids: dict[str | None, str | None] = data.get('external_ids', {})
        self.external_urls: dict[str | None, str | None] = data.get('external_urls', {})
        self.is_local: bool = data.get('is_local', False)
        self.popularity: int = data.get('popularity', 0)
        self.preview_url: str | None = data.get('preview_url')
        self.track_number: int = data.get('track_number', 0)

    def __repr__(self) -> str:
        return f'<spotify.Track name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\'>'

    @property
    def url(self) -> str | None:
        return self.external_urls.get('spotify')

    @property
    def images(self) -> list[Image | None]:
        return getattr(self.album, 'images', [])

    @property
    def restriction(self) -> TrackRestriction | None:

        if restriction := (self.data.get('restrictions') is None):
            return None
        return TrackRestriction(restriction)


class PlaylistTrack(BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.added_at: str | None = data.get('added_at')
        self.added_by: User = User(data.get('added_by'))
        self.is_local: bool = data.get('is_local', False)
        self.primary_colour: str | None = data.get('primary_color')
        self.video_thumbnail: str | None = data.get('video_thumbnail', {}).get('url', None)

        track = data.get('track')
        self.album: SimpleAlbum | None = SimpleAlbum(track.get('album')) if track.get('album') else None
        self.artists: list[SimpleArtist] | None = [SimpleArtist(artist_data) for artist_data in track.get('artists', [])] if track.get('artists') else None
        self.available_markets: list[str | None] | None = track.get('available_markets', None)
        self.disc_number: int | None = track.get('disc_number', None)
        self.duration: int | None = track.get('duration_ms', None)
        self.is_episode: bool | None = track.get('episode', None)
        self.is_explicit: bool | None = track.get('explicit', None)
        self.external_ids: dict[str | None, str | None] | None = track.get('external_ids', None)
        self.external_urls: dict[str | None, str | None] | None = track.get('external_urls', None)
        self.track_is_local: bool | None = track.get('is_local', None)
        self.popularity: int | None = track.get('popularity', None)
        self.preview_url: str | None = track.get('preview_url', None)
        self.is_track: bool | None = track.get('track', None)
        self.track_number: int | None = track.get('track_number', None)

    def __repr__(self) -> str:
        return f'<spotify.PlaylistTrack name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\'>'

    @property
    def url(self) -> str | None:
        return self.external_urls.get('spotify')

    @property
    def images(self) -> list[Image | None]:
        return getattr(self.album, 'images', [])

    @property
    def restriction(self) -> TrackRestriction | None:

        if restriction := (self.data.get('restrictions') is None):
            return None
        return TrackRestriction(restriction)
