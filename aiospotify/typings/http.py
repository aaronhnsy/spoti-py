# Future
from __future__ import annotations

# Standard Library
from typing import TypedDict

# My stuff
from aiospotify.typings.objects import (
    AlbumData,
    ArtistData,
    AudioFeaturesData,
    EpisodeData,
    PagingObjectData,
    ShowData,
    TrackData,
)


# ALBUMS API

class MultipleAlbumsData(TypedDict):
    albums: list[AlbumData | None]


class NewReleasesData(TypedDict):
    albums: PagingObjectData


# ARTISTS API

class MultipleArtistsData(TypedDict):
    artists: list[ArtistData | None]


class ArtistTopTracksData(TypedDict):
    tracks: list[TrackData]


class RelatedArtistsData(TypedDict):
    artists: list[ArtistData]


# SHOWS API

class MultipleShowsData(TypedDict):
    shows: list[ShowData | None]


# EPISODE API

class MultipleEpisodesData(TypedDict):
    episodes: list[EpisodeData | None]


# TRACKS API

class MultipleTracksData(TypedDict):
    tracks: list[TrackData | None]


class SeveralTracksAudioFeaturesData(TypedDict):
    audio_features: list[AudioFeaturesData | None]


# SEARCH API

class SearchResultData(TypedDict):
    albums: PagingObjectData
    artists: PagingObjectData
    tracks: PagingObjectData
    playlists: PagingObjectData
    shows: PagingObjectData
    episodes: PagingObjectData


# USERS API

...


# PLAYLISTS API

class FeaturedPlaylistsData(TypedDict):
    message: str
    playlists: PagingObjectData


class CategoryPlaylistsData(TypedDict):
    playlists: PagingObjectData


# CATEGORY API

class MultipleCategoriesData(TypedDict):
    categories: PagingObjectData


# GENRE API

class RecommendationGenresData(TypedDict):
    genres: list[str]


# PLAYER API

...


# MARKETS API

class AvailableMarketsData(TypedDict):
    markets: list[str]
