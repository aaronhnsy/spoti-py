from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired

from .artist import SimpleArtistData, SimpleArtist
from .base import BaseObjectData, BaseObject, PagingObjectData, PagingObject
from .common import ExternalURLs, ExternalIDs
from .copyright import CopyrightData, Copyright
from .enums import ReleaseDatePrecision, RestrictionReason
from .image import ImageData, Image
from .track import SimpleTrack, SimpleTrackData


__all__ = (
    "AlbumRestrictionData",
    "AlbumRestriction",
    "SimpleAlbumData",
    "SimpleAlbum",
    "AlbumData",
    "Album"
)


class AlbumRestrictionData(TypedDict):
    reason: str


class AlbumRestriction:

    def __init__(self, data: AlbumRestrictionData) -> None:
        self.reason: RestrictionReason = RestrictionReason(data["reason"])

    def __repr__(self) -> str:
        return f"<spotipy.AlbumRestriction reason='{self.reason}'>"


class SimpleAlbumData(BaseObjectData):
    album_type: str
    artists: list[SimpleArtistData]
    external_urls: ExternalURLs
    images: list[ImageData]
    release_date: str
    release_date_precision: str
    total_tracks: NotRequired[int]
    available_markets: NotRequired[list[str]]
    restrictions: NotRequired[AlbumRestrictionData]


class SimpleAlbum(BaseObject):

    def __init__(self, data: SimpleAlbumData) -> None:
        super().__init__(data)

        self.album_type: str = data["album_type"]
        self.artists: list[SimpleArtist] = [SimpleArtist(artist) for artist in data["artists"]]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.images: list[Image] = [Image(image) for image in data["images"]]
        self.release_date: str = data["release_date"]
        self.release_data_precision: ReleaseDatePrecision = ReleaseDatePrecision(data["release_date_precision"])
        self.total_tracks: int = data.get("total_tracks", -1)

        self.available_markets: list[str] | None = data.get("available_markets")
        self.restriction: AlbumRestriction | None = AlbumRestriction(restriction) if (restriction := data.get("restrictions")) else None

    def __repr__(self) -> str:
        return f"<spotipy.SimpleAlbum id='{self.id}', name='{self.name}', artists={self.artists}, total_tracks={self.total_tracks}>"

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class AlbumData(BaseObjectData):
    album_type: str
    artists: list[SimpleArtistData]
    copyrights: list[CopyrightData]
    external_ids: ExternalIDs
    external_urls: ExternalURLs
    genres: list[str]
    images: list[ImageData]
    label: str
    popularity: int
    release_date: str
    release_date_precision: str
    total_tracks: int
    tracks: PagingObjectData[SimpleTrackData]
    available_markets: NotRequired[list[str]]
    restrictions: NotRequired[AlbumRestrictionData]


class Album(BaseObject):

    def __init__(self, data: AlbumData) -> None:
        super().__init__(data)

        self.album_type: str = data["album_type"]
        self.artists: list[SimpleArtist] = [SimpleArtist(artist) for artist in data["artists"]]
        self.copyrights: list[Copyright] = [Copyright(copyright) for copyright in data["copyrights"]]
        self.external_ids: ExternalIDs = data["external_ids"]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.genres: list[str] = data["genres"]
        self.images: list[Image] = [Image(image) for image in data["images"]]
        self.label: str = data["label"]
        self.popularity: int = data["popularity"]
        self.release_date: str = data["release_date"]
        self.release_data_precision: ReleaseDatePrecision = ReleaseDatePrecision(data["release_date_precision"])
        self.total_tracks: int = data["total_tracks"]

        self.available_markets: list[str] | None = data.get("available_markets")
        self.restriction: AlbumRestriction | None = AlbumRestriction(restriction) if (restriction := data.get("restrictions")) else None

        self._tracks_paging = PagingObject(data["tracks"])
        self.tracks: list[SimpleTrack] = [SimpleTrack(track) for track in self._tracks_paging.items]

    def __repr__(self) -> str:
        return f"<spotipy.Album id='{self.id}', name='{self.name}', artists={self.artists}, total_tracks={self.total_tracks}>"

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
