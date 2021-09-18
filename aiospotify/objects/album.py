# Future
from __future__ import annotations

# My stuff
from aiospotify import objects
from typings.objects import AlbumData, AlbumRestrictionData, SimpleAlbumData


__all__ = (
    "AlbumRestriction",
    "SimpleAlbum",
    "Album"
)


class AlbumRestriction:

    def __init__(self, data: AlbumRestrictionData) -> None:

        self.reason = data["reason"]

    def __repr__(self) -> str:
        return f"<aiospotify.AlbumRestriction reason='{self.reason}'>"


class SimpleAlbum(objects.BaseObject):

    def __init__(self, data: SimpleAlbumData) -> None:
        super().__init__(data)

        self.album_type = data["album_type"]
        self.artists = [objects.SimpleArtist(artist) for artist in data["artists"]]
        self.available_markets = data.get("available_markets")
        self.external_urls = data["external_urls"]
        self.images = [objects.Image(image) for image in data["images"]]
        self.release_date = data["release_date"]
        self.release_data_precision = data["release_date_precision"]
        self.restriction = AlbumRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.total_tracks = data["total_tracks"]

    def __repr__(self) -> str:
        return f"<aiospotify.SimpleAlbum id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class Album(objects.BaseObject):

    def __init__(self, data: AlbumData) -> None:
        super().__init__(data)

        self.album_type = data["album_type"]
        self.artists = [objects.SimpleArtist(artist) for artist in data["artists"]]
        self.available_markets = data.get("available_markets")
        self.copyrights = [objects.Copyright(copyright) for copyright in data["copyrights"]]
        self.external_ids = data["external_ids"]
        self.external_urls = data["external_urls"]
        self.genres = data["genres"]
        self.images = [objects.Image(image) for image in data["images"]]
        self.label = data["label"]
        self.popularity = data["popularity"]
        self.release_date = data["release_date"]
        self.release_data_precision = data["release_date_precision"]
        self.restriction = AlbumRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.total_tracks = data["total_tracks"]

        self._tracks_paging = objects.PagingObject(data["tracks"])
        self.tracks = [objects.SimpleTrack(track) for track in self._tracks_paging.items]

    def __repr__(self) -> str:
        return f"<aiospotify.Album id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
