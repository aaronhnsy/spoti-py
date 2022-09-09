from __future__ import annotations

from typing import TypedDict

from .artist import SimpleArtistData, SimpleArtist
from .base import BaseObjectData, BaseObject, PagingObjectData, PagingObject
from .common import ExternalUrlsData, ExternalIdsData
from .copyright import CopyrightData, Copyright
from .image import ImageData, Image
from .track import SimpleTrack


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
        self.reason = data["reason"]

    def __repr__(self) -> str:
        return f"<spotipy.AlbumRestriction reason='{self.reason}'>"


class SimpleAlbumData(BaseObjectData):
    album_type: str
    artists: list[SimpleArtistData]
    available_markets: list[str]
    external_urls: ExternalUrlsData
    images: list[ImageData]
    release_date: str
    release_date_precision: str
    restrictions: AlbumRestrictionData
    total_tracks: int


class SimpleAlbum(BaseObject):

    def __init__(self, data: SimpleAlbumData) -> None:
        super().__init__(data)

        self.album_type = data["album_type"]
        self.artists = [SimpleArtist(artist) for artist in data["artists"]]
        self.available_markets = data.get("available_markets")
        self.external_urls = data["external_urls"]
        self.images = [Image(image) for image in data["images"]]
        self.release_date = data["release_date"]
        self.release_data_precision = data["release_date_precision"]
        self.restriction = AlbumRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.total_tracks = data.get("total_tracks")

    def __repr__(self) -> str:
        return f"<spotipy.SimpleAlbum id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class AlbumData(BaseObjectData):
    album_type: str
    artists: list[SimpleArtistData]
    available_markets: list[str]
    copyrights: list[CopyrightData]
    external_ids: ExternalIdsData
    external_urls: ExternalUrlsData
    genres: list[str]
    images: list[ImageData]
    label: str
    popularity: int
    release_date: str
    release_date_precision: str
    restrictions: AlbumRestrictionData
    total_tracks: int
    tracks: PagingObjectData


class Album(BaseObject):

    def __init__(self, data: AlbumData) -> None:
        super().__init__(data)

        self.album_type = data["album_type"]
        self.artists = [SimpleArtist(artist) for artist in data["artists"]]
        self.available_markets = data.get("available_markets")
        self.copyrights = [Copyright(copyright) for copyright in data["copyrights"]]
        self.external_ids = data["external_ids"]
        self.external_urls = data["external_urls"]
        self.genres = data["genres"]
        self.images = [Image(image) for image in data["images"]]
        self.label = data["label"]
        self.popularity = data["popularity"]
        self.release_date = data["release_date"]
        self.release_data_precision = data["release_date_precision"]
        self.restriction = AlbumRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.total_tracks = data["total_tracks"]

        self._tracks_paging = PagingObject(data["tracks"])
        self.tracks = [SimpleTrack(track) for track in self._tracks_paging.items]

    def __repr__(self) -> str:
        return f"<spotipy.Album id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
