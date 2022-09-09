from __future__ import annotations

from typing import TypedDict

from .base import BaseObject, BaseObjectData, PagingObjectData, PagingObject
from .common import ExternalUrlsData
from .followers import Followers, FollowersData
from .image import Image, ImageData
from .track import PlaylistTrack
from .user import User, UserData


__all__ = (
    "PlaylistSnapshotId",
    "PlaylistTrackRefData",
    "SimplePlaylistData",
    "SimplePlaylist",
    "PlaylistData",
    "Playlist"
)


class PlaylistSnapshotId(TypedDict):
    snapshot_id: str


class PlaylistTrackRefData(TypedDict):
    href: str
    total: int


class SimplePlaylistData(BaseObjectData):
    collaborative: bool
    description: str | None
    external_urls: ExternalUrlsData
    images: list[ImageData]
    owner: UserData
    primary_color: str | None
    public: bool | None
    snapshot_id: str
    tracks: PlaylistTrackRefData


class SimplePlaylist(BaseObject):

    def __init__(self, data: SimplePlaylistData) -> None:
        super().__init__(data)

        self.collaborative = data["collaborative"]
        self.description = data["description"]
        self.external_urls = data["external_urls"]
        self.images = [Image(image) for image in data["images"]]
        self.owner = User(data["owner"])
        self.primary_color = data["primary_color"]
        self.public = data["public"]
        self.snapshot_id = data["snapshot_id"]
        self.tracks_href = data["tracks"]["href"]
        self.total_tracks = data["tracks"]["total"]

    def __repr__(self) -> str:
        return f"<spotipy.SimplePlaylist id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class PlaylistData(BaseObjectData):
    collaborative: bool
    description: str | None
    external_urls: ExternalUrlsData
    followers: FollowersData
    images: list[ImageData]
    owner: UserData
    primary_color: str | None
    public: bool | None
    snapshot_id: str
    tracks: PagingObjectData


class Playlist(BaseObject):

    def __init__(self, data: PlaylistData) -> None:
        super().__init__(data)

        self.collaborative = data["collaborative"]
        self.description = data["description"]
        self.external_urls = data["external_urls"]
        self.followers = Followers(data["followers"])
        self.images = [Image(image) for image in data["images"]]
        self.owner = User(data["owner"])
        self.primary_color = data["primary_color"]
        self.public = data["public"]
        self.snapshot_id = data["snapshot_id"]
        self.total_tracks = data["tracks"]["total"]

        self._tracks_paging = PagingObject(data["tracks"])
        self.tracks = [PlaylistTrack(track) for track in self._tracks_paging.items]

    def __repr__(self) -> str:
        return f"<spotipy.Playlist id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
