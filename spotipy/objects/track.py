from __future__ import annotations

from typing import TypedDict, Any

from . import album
from .artist import SimpleArtist, SimpleArtistData
from .base import BaseObject, BaseObjectData
from .common import ExternalURLs, ExternalIDs
from .enums import Key, Mode
from .user import User, UserData


__all__ = (
    "AudioFeaturesData",
    "AudioFeatures",
    "TrackRestrictionData",
    "TrackRestriction",
    "SimpleTrackData",
    "SimpleTrack",
    "TrackData",
    "Track",
    "PlaylistTrackData",
    "PlaylistTrack",
)


class AudioFeaturesData(TypedDict):
    acousticness: float
    analysis_url: str
    danceability: float
    duration_ms: int
    energy: float
    id: str
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    time_signature: int
    track_href: str
    type: str
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
        return f"<spotipy.AudioFeatures id='{self.id}'>"


class TrackRestrictionData(TypedDict):
    reason: str


class TrackRestriction:

    def __init__(self, data: TrackRestrictionData) -> None:
        self.reason: str = data["reason"]

    def __repr__(self) -> str:
        return f"<spotipy.TrackRestriction reason='{self.reason}'>"


class SimpleTrackData(BaseObjectData):
    artists: list[SimpleArtistData]
    available_markets: list[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalURLs
    is_local: bool
    is_playable: bool
    #  linked_from: LinkedTrackData
    preview_url: str
    restrictions: TrackRestrictionData
    track_number: int


class SimpleTrack(BaseObject):

    def __init__(self, data: SimpleTrackData) -> None:
        super().__init__(data)

        self.artists: list[SimpleArtist] = [SimpleArtist(artist_data) for artist_data in data["artists"]]
        self.available_markets: list[str] = data["available_markets"]
        self.disc_number: int = data["disc_number"]
        self.duration_ms: int = data["duration_ms"]
        self.explicit: bool = data["explicit"]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.is_local: bool = data["is_local"]
        self.is_playable: bool = data["is_playable"]
        self.preview_url: str = data["preview_url"]
        self.restriction: TrackRestriction | None = TrackRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.track_number: int = data["track_number"]

    def __repr__(self) -> str:
        return f"<spotipy.SimpleTrack id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class TrackData(BaseObjectData):
    album: album.SimpleAlbumData
    artists: list[SimpleArtistData]
    available_markets: list[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIDs
    external_urls: ExternalURLs
    is_local: bool
    is_playable: bool
    #  linked_from: LinkedTrackData
    popularity: int
    preview_url: str
    restrictions: TrackRestrictionData
    track_number: int


class Track(BaseObject):

    def __init__(self, data: TrackData) -> None:
        super().__init__(data)

        self.album: album.SimpleAlbum = album.SimpleAlbum(data["album"])
        self.artists: list[SimpleArtist] = [SimpleArtist(artist_data) for artist_data in data["artists"]]
        self.available_markets: list[str] = data["available_markets"]
        self.disc_number: int = data["disc_number"]
        self.duration_ms: int = data["duration_ms"]
        self.explicit: bool = data["explicit"]
        self.external_ids: ExternalIDs = data["external_ids"]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.is_local: bool = data["is_local"]
        self.is_playable: bool = data["is_playable"]
        self.popularity: int = data["popularity"]
        self.preview_url: str = data["preview_url"]
        self.restriction: TrackRestriction | None = TrackRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.track_number: int = data["track_number"]

    def __repr__(self) -> str:
        return f"<spotipy.Track id='{self.id}', name='{self.name}'>"

    #

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
        self.available_markets: list[str] = track["available_markets"]
        self.disc_number: int = track["disc_number"]
        self.duration_ms: int = track["duration_ms"]
        self.explicit: bool = track["explicit"]
        self.external_ids: ExternalIDs = track["external_ids"]
        self.external_urls: ExternalURLs = track["external_urls"]
        self.is_local: bool = track["is_local"]
        self.is_playable: bool = track["is_playable"]
        self.popularity: int = track["popularity"]
        self.preview_url: str = track["preview_url"]
        self.restriction: TrackRestriction | None = TrackRestriction(restriction) if (restriction := track.get("restrictions")) else None
        self.track_number: int = track["track_number"]

    def __repr__(self) -> str:
        return f"<spotipy.PlaylistTrack id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
