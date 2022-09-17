from __future__ import annotations

from typing import Literal, TypedDict

from typing_extensions import NotRequired

from ..objects.base import PagingObjectData
from ..objects.playlist import SimplePlaylistData


__all__ = (
    "HTTPMethod",
    "Headers",
    "FeaturedPlaylistsData",
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
