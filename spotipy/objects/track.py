from __future__ import annotations

from typing import TypedDict, Any

from . import album
from .artist import SimpleArtist, SimpleArtistData
from .base import BaseObject, BaseObjectData
from .common import ExternalUrlsData, ExternalIdsData
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
        self.acousticness = data["acousticness"]
        self.analysis_url = data["analysis_url"]
        self.danceability = data["danceability"]
        self.duration_ms = data["duration_ms"]
        self.energy = data["energy"]
        self.id = data["id"]
        self.instrumentalness = data["instrumentalness"]
        self.key = Key(data["key"])
        self.liveness = data["liveness"]
        self.loudness = data["loudness"]
        self.mode = Mode(data["mode"])
        self.speechiness = data["speechiness"]
        self.tempo = data["tempo"]
        self.time_signature = data["time_signature"]
        self.track_href = data["track_href"]
        self.type = data["type"]
        self.uri = data["uri"]
        self.valence = data["valence"]

    def __repr__(self) -> str:
        return f"<spotipy.AudioFeatures id='{self.id}'>"


class TrackRestrictionData(TypedDict):
    reason: str


class TrackRestriction:

    def __init__(self, data: TrackRestrictionData) -> None:
        self.reason = data["reason"]

    def __repr__(self) -> str:
        return f"<spotipy.TrackRestriction reason='{self.reason}'>"


class SimpleTrackData(BaseObjectData):
    artists: list[SimpleArtistData]
    available_markets: list[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrlsData
    is_local: bool
    is_playable: bool
    #  linked_from: LinkedTrackData
    preview_url: str
    restrictions: TrackRestrictionData
    track_number: int


class SimpleTrack(BaseObject):

    def __init__(self, data: SimpleTrackData) -> None:
        super().__init__(data)

        self.artists = [SimpleArtist(artist_data) for artist_data in data["artists"]]
        self.available_markets = data["available_markets"]
        self.disc_number = data["disc_number"]
        self.duration_ms = data["duration_ms"]
        self.explicit = data["explicit"]
        self.external_urls = data["external_urls"]
        self.is_local = data["is_local"]
        self.preview_url = data["preview_url"]
        self.restriction = TrackRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.track_number = data["track_number"]

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
    external_ids: ExternalIdsData
    external_urls: ExternalUrlsData
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

        self.album = album.SimpleAlbum(data["album"])
        self.artists = [SimpleArtist(artist_data) for artist_data in data["artists"]]
        self.available_markets = data.get("available_markets")
        self.disc_number = data["disc_number"]
        self.duration_ms = data["duration_ms"]
        self.explicit = data["explicit"]
        self.external_ids = data["external_ids"]
        self.external_urls = data["external_urls"]
        self.is_local = data["is_local"]
        self.popularity = data["popularity"]
        self.preview_url = data["preview_url"]
        self.restriction = TrackRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.track_number = data["track_number"]

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

        self.added_at = data["added_at"]
        self.added_by = User(data["added_by"])
        self.is_local = data["is_local"]
        self.primary_colour = data["primary_color"]
        self.video_thumbnail = data["video_thumbnail"]["url"]

        track = data["track"]
        self.album = album.SimpleAlbum(track["album"])
        self.artists = [SimpleArtist(artist_data) for artist_data in track["artists"]]
        self.available_markets = track.get("available_markets")
        self.disc_number = track["disc_number"]
        self.duration_ms = track["duration_ms"]
        self.explicit = track["explicit"]
        self.external_ids = track["external_ids"]
        self.external_urls = track["external_urls"]
        self.is_local = track["is_local"]
        self.popularity = track["popularity"]
        self.preview_url = track["preview_url"]
        self.restriction = TrackRestriction(restriction) if (restriction := track.get("restrictions")) else None
        self.track_number = track["track_number"]

    def __repr__(self) -> str:
        return f"<spotipy.PlaylistTrack id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
