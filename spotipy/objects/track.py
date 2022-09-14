from __future__ import annotations

import enum
from typing import TypedDict, Any, Literal

from typing_extensions import NotRequired

from . import album
from .artist import SimpleArtist, SimpleArtistData
from .base import BaseObject, BaseObjectData
from .common import ExternalURLs, ExternalIDs
from .user import User, UserData
from .restrictions import Restrictions, RestrictionsData


__all__ = (
    "Key",
    "Mode",
    "AudioFeaturesData",
    "AudioFeatures",
    "TrackLinkData",
    "TrackLink",
    "SimpleTrackData",
    "SimpleTrack",
    "TrackData",
    "Track",
    "PlaylistTrackData",
    "PlaylistTrack",
)


class Key(enum.Enum):
    UNKNOWN = -1
    C = 0
    C_SHARP = 1
    D = 2
    D_SHARP = 3
    E = 4
    E_SHARP = 5
    F = 5
    F_SHARP = 6
    G = 7
    G_SHARP = 8
    A = 9
    A_SHARP = 10
    B = 11


class Mode(enum.Enum):
    MINOR = 0
    MAJOR = 1


class AudioFeaturesData(TypedDict):
    acousticness: float
    analysis_url: str
    danceability: float
    duration_ms: int
    energy: float
    id: str
    instrumentalness: float
    key: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -1]
    liveness: float
    loudness: float
    mode: Literal[1, 2]
    speechiness: float
    tempo: float
    time_signature: Literal[3, 4, 5, 6, 7]
    track_href: str
    type: Literal["audio_features"]
    uri: str
    valence: float


class AudioFeatures:

    def __init__(self, data: AudioFeaturesData) -> None:
        self.acousticness: float = data["acousticness"]
        self.analysis_url: str = data["analysis_url"]
        self.danceability: float = data["danceability"]
        self.duration_ms: int = data["duration_ms"]
        self.energy: float = data["energy"]
        self.id: str = data["id"]
        self.instrumentalness: float = data["instrumentalness"]
        self.key: Key = Key(data["key"])
        self.liveness: float = data["liveness"]
        self.loudness: float = data["loudness"]
        self.mode: Mode = Mode(data["mode"])
        self.speechiness: float = data["speechiness"]
        self.tempo: float = data["tempo"]
        self.time_signature: int = data["time_signature"]
        self.track_href: str = data["track_href"]
        self.type: str = data["type"]
        self.uri: str = data["uri"]
        self.valence: float = data["valence"]

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: id='{self.id}'>"


class TrackLinkData(BaseObjectData):
    external_urls: ExternalURLs


class TrackLink(BaseObject):

    def __init__(self, data: TrackLinkData) -> None:
        super().__init__(data)
        self.external_urls: ExternalURLs = data["external_urls"]

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class SimpleTrackData(BaseObjectData):
    artists: list[SimpleArtistData]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalURLs
    is_local: bool
    preview_url: str
    track_number: int
    available_markets: NotRequired[list[str]]
    is_playable: NotRequired[bool]
    linked_from: NotRequired[TrackLinkData]
    restrictions: NotRequired[RestrictionsData]


class SimpleTrack(BaseObject):

    def __init__(self, data: SimpleTrackData) -> None:
        super().__init__(data)

        self.artists: list[SimpleArtist] = [SimpleArtist(artist_data) for artist_data in data["artists"]]
        self.disc_number: int = data["disc_number"]
        self.duration_ms: int = data["duration_ms"]
        self.explicit: bool = data["explicit"]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.is_local: bool = data["is_local"]
        self.preview_url: str = data["preview_url"]
        self.track_number: int = data["track_number"]

        self.available_markets: list[str] | None = data.get("available_markets")
        self.is_playable: bool | None = data.get("is_playable")
        self.linked_from: TrackLink | None = TrackLink(linked_from) if (linked_from := data.get("linked_from")) else None
        self.restriction: Restrictions | None = Restrictions(restriction) if (restriction := data.get("restrictions")) else None

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class TrackData(BaseObjectData):
    album: album.SimpleAlbumData
    artists: list[SimpleArtistData]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIDs
    external_urls: ExternalURLs
    is_local: bool
    popularity: int
    preview_url: str
    track_number: int
    available_markets: NotRequired[list[str]]
    is_playable: NotRequired[bool]
    linked_from: NotRequired[TrackLinkData]
    restrictions: NotRequired[RestrictionsData]


class Track(BaseObject):

    def __init__(self, data: TrackData) -> None:
        super().__init__(data)

        self.album: album.SimpleAlbum = album.SimpleAlbum(data["album"])
        self.artists: list[SimpleArtist] = [SimpleArtist(artist_data) for artist_data in data["artists"]]
        self.disc_number: int = data["disc_number"]
        self.duration_ms: int = data["duration_ms"]
        self.explicit: bool = data["explicit"]
        self.external_ids: ExternalIDs = data["external_ids"]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.is_local: bool = data["is_local"]
        self.popularity: int = data["popularity"]
        self.preview_url: str = data["preview_url"]
        self.track_number: int = data["track_number"]

        self.available_markets: list[str] | None = data.get("available_markets")
        self.is_playable: bool | None = data.get("is_playable")
        self.linked_from: TrackLink | None = TrackLink(linked_from) if (linked_from := data.get("linked_from")) else None
        self.restriction: Restrictions | None = Restrictions(restriction) if (restriction := data.get("restrictions")) else None

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class PlaylistTrackData(BaseObjectData):
    added_at: str
    added_by: UserData
    is_local: bool
    primary_color: Any
    video_thumbnail: Any
    track: TrackData


class PlaylistTrack(BaseObject):

    def __init__(self, data: PlaylistTrackData) -> None:
        super().__init__(data["track"])

        self.added_at: str = data["added_at"]
        self.added_by: User = User(data["added_by"])
        self.is_local: bool = data["is_local"]
        self.primary_colour: Any = data["primary_color"]
        self.video_thumbnail: Any = data["video_thumbnail"]["url"]

        track = data["track"]
        self.album: album.SimpleAlbum = album.SimpleAlbum(track["album"])
        self.artists: list[SimpleArtist] = [SimpleArtist(artist_data) for artist_data in track["artists"]]
        self.disc_number: int = track["disc_number"]
        self.duration_ms: int = track["duration_ms"]
        self.explicit: bool = track["explicit"]
        self.external_ids: ExternalIDs = track["external_ids"]
        self.external_urls: ExternalURLs = track["external_urls"]
        self.is_local: bool = track["is_local"]
        self.popularity: int = track["popularity"]
        self.preview_url: str = track["preview_url"]
        self.track_number: int = track["track_number"]

        self.available_markets: list[str] | None = track.get("available_markets")
        self.is_playable: bool | None = track.get("is_playable")
        self.linked_from: TrackLink | None = TrackLink(linked_from) if (linked_from := track.get("linked_from")) else None
        self.restriction: Restrictions | None = Restrictions(restriction) if (restriction := track.get("restrictions")) else None

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
