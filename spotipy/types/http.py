from __future__ import annotations

from typing import Literal, TypedDict

from typing_extensions import NotRequired

from ..objects.album import AlbumData, SimpleAlbumData
from ..objects.artist import ArtistData
from ..objects.base import PagingObjectData
from ..objects.category import CategoryData
from ..objects.device import DeviceData
from ..objects.episode import EpisodeData
from ..objects.playlist import SimplePlaylistData
from ..objects.show import ShowData
from ..objects.track import AudioFeaturesData, TrackData


__all__ = (
    "HTTPMethod",
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
    albums: PagingObjectData[SimpleAlbumData]


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
    playlists: PagingObjectData[SimplePlaylistData]


class CategoryPlaylistsData(TypedDict):
    playlists: PagingObjectData[SimplePlaylistData]


class MultipleCategoriesData(TypedDict):
    categories: PagingObjectData[CategoryData]


class RecommendationGenresData(TypedDict):
    genres: list[str]


class MultipleDevicesData(TypedDict):
    devices: list[DeviceData]


class AvailableMarketsData(TypedDict):
    markets: list[str]
