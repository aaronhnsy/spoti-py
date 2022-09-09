from __future__ import annotations

from typing import Any, Literal, TypedDict

from typing_extensions import NotRequired

from ..objects import (
    AlbumData, ArtistData, PagingObjectData, TrackData, ShowData, EpisodeData, AudioFeaturesData,
    DeviceData,
)


__all__ = (
    "HTTPMethod",
    "Query",
    "Body",
    "Data",
    "Headers",
    "MultipleAlbumsData",
    "NewReleasesData",
    "MultipleArtistsData",
    "ArtistTopTracksData",
    "ArtistRelatedArtistsData",
    "MultipleShowsData",
    "MultipleEpisodesData",
    "MultipleTracksData",
    "SeveralAudioFeaturesData",
    "FeaturedPlaylistsData",
    "CategoryPlaylistsData",
    "MultipleCategoriesData",
    "RecommendationGenresData",
    "MultipleDevicesData",
    "AvailableMarketsData",
)


HTTPMethod = Literal["GET", "POST", "DELETE", "PATCH", "PUT"]

Query = dict[str, Any]
Body = dict[str, Any]
Data = dict[str, Any]

Headers = TypedDict(
    "Headers",
    {
        "Authorization": str,
        "Content-Type":  NotRequired[str]
    }
)


class MultipleAlbumsData(TypedDict):
    albums: list[AlbumData | None]


class NewReleasesData(TypedDict):
    albums: PagingObjectData


class MultipleArtistsData(TypedDict):
    artists: list[ArtistData | None]


class ArtistTopTracksData(TypedDict):
    tracks: list[TrackData]


class ArtistRelatedArtistsData(TypedDict):
    artists: list[ArtistData]


class MultipleShowsData(TypedDict):
    shows: list[ShowData | None]


class MultipleEpisodesData(TypedDict):
    episodes: list[EpisodeData | None]


class MultipleTracksData(TypedDict):
    tracks: list[TrackData | None]


class SeveralAudioFeaturesData(TypedDict):
    audio_features: list[AudioFeaturesData | None]


class FeaturedPlaylistsData(TypedDict):
    message: str
    playlists: PagingObjectData


class CategoryPlaylistsData(TypedDict):
    playlists: PagingObjectData


class MultipleCategoriesData(TypedDict):
    categories: PagingObjectData


class RecommendationGenresData(TypedDict):
    genres: list[str]


class MultipleDevicesData(TypedDict):
    devices: list[DeviceData]


class AvailableMarketsData(TypedDict):
    markets: list[str]
