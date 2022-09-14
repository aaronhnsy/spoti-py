from __future__ import annotations

from typing import Literal, TypedDict

from typing_extensions import NotRequired

from ..objects.base import PagingObjectData
from ..objects.category import CategoryData
from ..objects.device import DeviceData
from ..objects.playlist import SimplePlaylistData


__all__ = (
    "HTTPMethod",
    "Headers",
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
