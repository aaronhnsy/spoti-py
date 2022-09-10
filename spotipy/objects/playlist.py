from __future__ import annotations

from typing import TypedDict

from .base import BaseObject, BaseObjectData, PagingObjectData, PagingObject
from .common import ExternalURLs
from .followers import Followers, FollowersData
from .image import Image, ImageData
from .track import PlaylistTrack, PlaylistTrackData
from .user import User, UserData


__all__ = (
    "PlaylistSnapshotID",
    "PlaylistTrackRefData",
    "SimplePlaylistData",
    "SimplePlaylist",
    "PlaylistData",
    "Playlist"
)


class PlaylistSnapshotID(TypedDict):
    snapshot_id: str


class PlaylistTrackRefData(TypedDict):
    href: str
    total: int


class SimplePlaylistData(BaseObjectData):
    collaborative: bool
    description: str | None
    external_urls: ExternalURLs
    images: list[ImageData]
    owner: UserData
    primary_color: str | None
    public: bool | None
    snapshot_id: str
    tracks: PlaylistTrackRefData


class SimplePlaylist(BaseObject):

    def __init__(self, data: SimplePlaylistData) -> None:
        super().__init__(data)

        self.collaborative: bool = data["collaborative"]
        self.description: str | None = data["description"]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.images: list[Image] = [Image(image) for image in data["images"]]
        self.owner: User = User(data["owner"])
        self.primary_color: str | None = data["primary_color"]
        self.public: bool | None = data["public"]
        self.snapshot_id: str = data["snapshot_id"]
        self.tracks_href: str = data["tracks"]["href"]
        self.total_tracks: int = data["tracks"]["total"]

    def __repr__(self) -> str:
        return f"<spotipy.SimplePlaylist id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class PlaylistData(BaseObjectData):
    collaborative: bool
    description: str | None
    external_urls: ExternalURLs
    followers: FollowersData
    images: list[ImageData]
    owner: UserData
    primary_color: str | None
    public: bool | None
    snapshot_id: str
    tracks: PagingObjectData[PlaylistTrackData]


class Playlist(BaseObject):

    def __init__(self, data: PlaylistData) -> None:
        super().__init__(data)

        self.collaborative: bool = data["collaborative"]
        self.description: str | None = data["description"]
        self.external_urls: ExternalURLs = data["external_urls"]
        self.followers: Followers = Followers(data["followers"])
        self.images: list[Image] = [Image(image) for image in data["images"]]
        self.owner: User = User(data["owner"])
        self.primary_color: str | None = data["primary_color"]
        self.public: bool | None = data["public"]
        self.snapshot_id: str = data["snapshot_id"]
        self.total_tracks: int = data["tracks"]["total"]

        self._tracks_paging = PagingObject(data["tracks"])
        self.tracks: list[PlaylistTrack] = [PlaylistTrack(track) for track in self._tracks_paging.items]

    def __repr__(self) -> str:
        return f"<spotipy.Playlist id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
