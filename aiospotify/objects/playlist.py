# Future
from __future__ import annotations

# My stuff
from aiospotify import objects
from typings.objects import PlaylistData, SimplePlaylistData


__all__ = (
    "SimplePlaylist",
    "Playlist"
)


class SimplePlaylist(objects.BaseObject):

    def __init__(self, data: SimplePlaylistData) -> None:
        super().__init__(data)

        self.collaborative = data["collaborative"]
        self.description = data["description"]
        self.external_urls = data["external_urls"]
        self.images = [objects.Image(image) for image in data["images"]]
        self.owner = objects.User(data["owner"])
        self.primary_color = data["primary_color"]
        self.public = data["public"]
        self.snapshot_id = data["snapshot_id"]
        self.tracks_href = data["tracks"]["href"]
        self.total_tracks = data["tracks"]["total"]

    def __repr__(self) -> str:
        return f"<aiospotify.SimplePlaylist id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class Playlist(objects.BaseObject):

    def __init__(self, data: PlaylistData) -> None:
        super().__init__(data)

        self.collaborative = data["collaborative"]
        self.description = data["description"]
        self.external_urls = data["external_urls"]
        self.followers = objects.Followers(data["followers"])
        self.images = [objects.Image(image) for image in data["images"]]
        self.owner = objects.User(data["owner"])
        self.primary_color = data["primary_color"]
        self.public = data["public"]
        self.snapshot_id = data["snapshot_id"]
        self.total_tracks = data["tracks"]["total"]

        self._tracks_paging = objects.PagingObject(data["tracks"])
        self.tracks = [objects.PlaylistTrack(track) for track in self._tracks_paging.items]

    def __repr__(self) -> str:
        return f"<aiospotify.Playlist id='{self.id}', name='{self.name}', total_tracks={self.total_tracks}>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
