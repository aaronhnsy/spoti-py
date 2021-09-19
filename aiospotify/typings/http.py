# Future
from __future__ import annotations

# Standard Library
from typing import TypedDict

# My stuff
from aiospotify.typings.objects import AlbumData, ArtistData, EpisodeData, PagingObjectData, ShowData, TrackData


# ALBUMS API

class MultipleAlbumsData(TypedDict):
    albums: list[AlbumData | None]


# ARTISTS API

class MultipleArtistsData(TypedDict):
    artists: list[ArtistData | None]


class ArtistTopTracksData(TypedDict):
    tracks: list[TrackData]


class ArtistRelatedArtistsData(TypedDict):
    artists: list[ArtistData]


# BROWSE API

class NewReleasesData(TypedDict):
    albums: PagingObjectData


class FeaturedPlaylistsData(TypedDict):
    message: str
    playlists: PagingObjectData


class MultipleCategoriesData(TypedDict):
    categories: PagingObjectData


class CategoryPlaylistsData(TypedDict):
    playlists: PagingObjectData


class RecommendationGenresData(TypedDict):
    genres: list[str]


# EPISODE API

class MultipleEpisodesData(TypedDict):
    episodes: list[EpisodeData | None]


# FOLLOW API

...


# LIBRARY API

...


# MARKETS API

class AvailableMarketsData(TypedDict):
    markets: list[str]


# PERSONALIZATION API

...


# PLAYER API

...


# PLAYLISTS API

...


# SEARCH API

class SearchResultData(TypedDict):
    albums: PagingObjectData
    artists: PagingObjectData
    tracks: PagingObjectData
    playlists: PagingObjectData
    shows: PagingObjectData
    episodes: PagingObjectData


# SHOWS API

class MultipleShowsData(TypedDict):
    shows: list[ShowData | None]


# TRACKS API #

...


# USERS API

...
