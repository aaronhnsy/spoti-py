# Future
from __future__ import annotations

# Standard Library
from typing import Any, Optional, TypedDict


# COMMON

class BaseObjectData(TypedDict):
    href: str
    id: str
    name: str
    type: str
    uri: str


class PagingObjectData(TypedDict):
    href: str
    items: list[Any]  # type: ignore
    limit: int
    next: Optional[str | None]
    offset: int
    previous: Optional[str | None]
    total: int


class ImageData(TypedDict):
    url: str
    width: int
    height: int


class FollowersData(TypedDict):
    href: Optional[str]
    total: int


class CopyrightData(TypedDict):
    text: str
    type: str


# ALBUMS API

class AlbumRestrictionData(TypedDict):
    reason: str


class SimpleAlbumData(BaseObjectData):
    album_type: str
    artists: list[SimpleArtistData]
    available_markets: list[str]
    external_urls: dict[str, Any]
    images: list[ImageData]
    release_date: str
    release_date_precision: str
    restrictions: AlbumRestrictionData
    total_tracks: int


class AlbumData(BaseObjectData):
    album_type: str
    artists: list[SimpleArtistData]
    available_markets: list[str]
    copyrights: list[CopyrightData]
    external_ids: dict[str, Any]
    external_urls: dict[str, Any]
    genres: list[str]
    images: list[ImageData]
    label: str
    popularity: int
    release_date: str
    release_date_precision: str
    restrictions: AlbumRestrictionData
    total_tracks: int
    tracks: PagingObjectData


# ARTISTS API

class SimpleArtistData(BaseObjectData):
    external_urls: dict[str, Any]


class ArtistData(SimpleArtistData):
    followers: FollowersData
    genres: list[str]
    images: list[ImageData]
    popularity: int


# BROWSE API

class CategoryData(TypedDict):
    href: str
    icons: list[ImageData]
    id: str
    name: str


class RecommendationSeedData(TypedDict):
    initialPoolSize: int
    afterFilteringSize: int
    afterRelinkingSize: int
    id: str
    type: str
    href: str


class RecommendationData(TypedDict):
    tracks: list[TrackData]
    seeds: list[RecommendationSeedData]


# EPISODE API

class EpisodeRestrictionData(TypedDict):
    reason: str


class EpisodeResumePointData(TypedDict):
    fully_played: bool
    resume_position_ms: int


class SimpleEpisodeData(BaseObjectData):
    audio_preview_url: Optional[str]
    description: str
    duration_ms: int
    explicit: bool
    external_urls: dict[str, Any]
    html_description: str
    images: list[ImageData]
    is_externally_hosted: bool
    is_playable: bool
    languages: list[str]
    release_date: str
    release_date_precision: str
    restrictions: EpisodeRestrictionData
    resume_point: EpisodeResumePointData


class EpisodeData(BaseObjectData):
    audio_preview_url: Optional[str]
    description: str
    duration_ms: int
    explicit: bool
    external_urls: dict[str, Any]
    html_description: str
    images: list[ImageData]
    is_externally_hosted: bool
    is_playable: bool
    languages: list[str]
    release_date: str
    release_date_precision: str
    restrictions: EpisodeRestrictionData
    resume_point: EpisodeResumePointData
    show: ShowData


# FOLLOW API

...


# LIBRARY API

...


# MARKETS API

...


# PERSONALIZATION API

...


# PLAYER API

class DeviceData(TypedDict):
    id: str
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    type: str
    volume_percent: int


class DisallowsData(TypedDict):
    interrupting_playback: bool
    pausing: bool
    resuming: bool
    seeking: bool
    skipping_next: bool
    skipping_prev: bool
    toggling_repeat_context: bool
    toggling_repeat_track: bool
    toggling_shuffle: bool
    transferring_playback: bool


class ContextData(TypedDict):
    external_urls: dict[str, Any]
    href: str
    type: str
    uri: str


class CurrentlyPlayingContextData(TypedDict):
    actions: DisallowsData
    context: ContextData
    currently_playing_type: str
    device: DeviceData
    is_playing: bool
    item: Optional[TrackData]
    progress_ms: int
    repeat_state: str
    shuffle_state: str
    timestamp: int


class CurrentlyPlayingData(TypedDict):
    context: ContextData
    currently_playing_type: str
    is_playing: bool
    item: Optional[TrackData]
    progress_ms: int
    timestamp: int


# PLAYLISTS API


class PlaylistTrackData(BaseObjectData):
    added_at: str
    added_by: dict[str, Any]
    is_local: bool
    primary_color: Any
    video_thumbnail: Any
    track: TrackData


class PlaylistTrackRefData(TypedDict):
    href: str
    total: int


class SimplePlaylistData(BaseObjectData):
    collaborative: bool
    description: Optional[str]
    external_urls: dict[str, Any]
    images: list[ImageData]
    owner: dict[str, Any]
    primary_color: Optional[str]
    public: Optional[bool]
    snapshot_id: str
    tracks: PlaylistTrackRefData


class PlaylistData(BaseObjectData):
    collaborative: bool
    description: Optional[str]
    external_urls: dict[str, Any]
    followers: FollowersData
    images: list[ImageData]
    owner: dict[str, Any]
    primary_color: Optional[str]
    public: Optional[bool]
    snapshot_id: str
    tracks: PagingObjectData


# SEARCH API

...


# SHOWS API

class ShowData(BaseObjectData):
    available_markets: list[str]
    copyrights: list[CopyrightData]
    description: str
    explicit: bool
    external_urls: dict[str, Any]
    html_description: str
    images: list[ImageData]
    is_externally_hosted: bool
    languages: list[str]
    media_type: str
    publisher: str
    total_episodes: int


# TRACKS API


class TrackRestrictionData(TypedDict):
    reason: str


class SimpleTrackData(BaseObjectData):
    artists: list[SimpleArtistData]
    available_markets: list[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: dict[str, Any]
    is_local: bool
    is_playable: bool
    #  linked_from: LinkedTrackData
    preview_url: str
    restrictions: TrackRestrictionData
    track_number: int


class TrackData(BaseObjectData):
    album: SimpleAlbumData
    artists: list[SimpleArtistData]
    available_markets: list[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: dict[str, Any]
    external_urls: dict[str, Any]
    is_local: bool
    is_playable: bool
    #  linked_from: LinkedTrackData
    popularity: int
    preview_url: str
    restrictions: TrackRestrictionData
    track_number: int


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


# USERS API

class ExplicitContentSettingsData(TypedDict):
    filter_enabled: bool
    filter_locked: bool


# TOKENS

class ClientCredentialsData(TypedDict):
    access_token: str
    token_type: str
    expires_in: int


class UserCredentialsData(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: str
