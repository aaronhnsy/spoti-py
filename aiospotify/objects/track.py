# Future
from __future__ import annotations

# Standard Library
from typing import Literal, Optional

# My stuff
from aiospotify.objects import album, artist, base, image, user


class TrackRestriction:

    __slots__ = 'data', 'reason'

    def __init__(self, data: dict) -> None:

        self.data = data

        self.reason: Literal['market', 'product', 'explicit'] = data.get('reason')

    def __repr__(self) -> str:
        return f'spotify.TrackRestriction reason=\'{self.reason}\''


class SimpleTrack(base.BaseObject):

    __slots__ = 'artists', 'available_markets', 'disc_number', 'duration', 'is_explicit', 'external_urls', 'is_local', 'preview_url', 'track_number'

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.artists: list[Optional[artist.SimpleArtist]] = [artist.SimpleArtist(artist_data) for artist_data in data.get('artists', [])]
        self.available_markets: list[Optional[str]] = data.get('available_markets', [])
        self.disc_number: int = data.get('disc_number', 0)
        self.duration: int = data.get('duration_ms', 0)
        self.is_explicit: bool = data.get('explicit', False)
        self.external_urls: dict[Optional[str], Optional[str]] = data.get('external_urls', {})
        self.is_local: bool = data.get('is_local', False)
        self.preview_url: Optional[str] = data.get('preview_url')
        self.track_number: int = data.get('track_number', 0)

    def __repr__(self) -> str:
        return f'<spotify.SimpleTrack name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')

    @property
    def restriction(self) -> Optional[TrackRestriction]:

        if restriction := (self.data.get('restrictions') is None):
            return None
        return TrackRestriction(restriction)


class Track(base.BaseObject):

    __slots__ = 'album', 'artists', 'available_markets', 'disc_number', 'duration', 'is_explicit', 'external_urls', 'external_ids', 'is_local', 'popularity', 'preview_url', \
                'track_number'

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.album: album.SimpleAlbum = album.SimpleAlbum(data.get('album'))
        self.artists: list[Optional[artist.SimpleArtist]] = [artist.SimpleArtist(artist_data) for artist_data in data.get('artists', [])]
        self.available_markets: list[Optional[str]] = data.get('available_markets', [])
        self.disc_number: int = data.get('disc_number', 0)
        self.duration: int = data.get('duration_ms', 0)
        self.is_explicit: bool = data.get('explicit', False)
        self.external_ids: dict[Optional[str], Optional[str]] = data.get('external_ids', {})
        self.external_urls: dict[Optional[str], Optional[str]] = data.get('external_urls', {})
        self.is_local: bool = data.get('is_local', False)
        self.popularity: int = data.get('popularity', 0)
        self.preview_url: Optional[str] = data.get('preview_url')
        self.track_number: int = data.get('track_number', 0)

    def __repr__(self) -> str:
        return f'<spotify.Track name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')

    @property
    def images(self) -> list[Optional[image.Image]]:
        return getattr(self.album, 'images', [])

    @property
    def restriction(self) -> Optional[TrackRestriction]:

        if restriction := (self.data.get('restrictions') is None):
            return None
        return TrackRestriction(restriction)


class PlaylistTrack(base.BaseObject):

    __slots__ = 'added_at', 'added_by', 'primary_colour', 'video_thumbnail', 'album', 'artists', 'available_markets', 'disc_number', 'duration', 'is_explicit', 'external_urls', \
                'external_ids', 'is_local', 'popularity', 'preview_url', 'track_number', 'is_episode', 'track_is_local', 'is_track'

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.added_at: Optional[str] = data.get('added_at')
        self.added_by: user.User = user.User(data.get('added_by'))
        self.is_local: bool = data.get('is_local', False)
        self.primary_colour: Optional[str] = data.get('primary_color')
        self.video_thumbnail: Optional[str] = data.get('video_thumbnail', {}).get('url', None)

        track = data.get('track')
        self.album: Optional[album.SimpleAlbum] = album.SimpleAlbum(track.get('album')) if track.get('album') else None
        self.artists: Optional[list[artist.SimpleArtist]] = [artist.SimpleArtist(artist_data) for artist_data in track.get('artists', [])] if track.get('artists') else None
        self.available_markets: Optional[list[Optional[str]]] = track.get('available_markets', None)
        self.disc_number: Optional[int] = track.get('disc_number', None)
        self.duration: Optional[int] = track.get('duration_ms', None)
        self.is_episode: Optional[bool] = track.get('episode', None)
        self.is_explicit: Optional[bool] = track.get('explicit', None)
        self.external_ids: Optional[dict[Optional[str], Optional[str]]] = track.get('external_ids', None)
        self.external_urls: Optional[dict[Optional[str], Optional[str]]] = track.get('external_urls', None)
        self.track_is_local: Optional[bool] = track.get('is_local', None)
        self.popularity: Optional[int] = track.get('popularity', None)
        self.preview_url: Optional[str] = track.get('preview_url', None)
        self.is_track: Optional[bool] = track.get('track', None)
        self.track_number: Optional[int] = track.get('track_number', None)

    def __repr__(self) -> str:
        return f'<spotify.PlaylistTrack name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')

    @property
    def images(self) -> list[Optional[image.Image]]:
        return getattr(self.album, 'images', [])

    @property
    def restriction(self) -> Optional[TrackRestriction]:

        if restriction := (self.data.get('restrictions') is None):
            return None
        return TrackRestriction(restriction)
