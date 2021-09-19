# Future
from __future__ import annotations

# Standard Library
from typing import TypedDict, Union

# My stuff
from aiospotify.typings.objects import AlbumData, ArtistData, PagingObjectData, TrackData


__all__ = (
    "MultipleAlbumsData",
    "MultipleArtistsData",
    "ArtistTopTracksData",
    "ArtistRelatedArtistsData",
    "NewReleasesData",
    "FeaturedPlaylistsData",
    "MultipleCategoriesData",
    "CategoryPlaylistsData",
)


class MultipleAlbumsData(TypedDict):
    albums: list[Union[AlbumData | None]]


class MultipleArtistsData(TypedDict):
    artists: list[Union[ArtistData | None]]


class ArtistTopTracksData(TypedDict):
    tracks: list[TrackData]


class ArtistRelatedArtistsData(TypedDict):
    artists: list[ArtistData]


class NewReleasesData(TypedDict):
    albums: PagingObjectData


class FeaturedPlaylistsData(TypedDict):
    message: str
    playlists: PagingObjectData


class MultipleCategoriesData(TypedDict):
    categories: PagingObjectData


class CategoryPlaylistsData(TypedDict):
    playlists: PagingObjectData
