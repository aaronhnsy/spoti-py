# Future
from __future__ import annotations

# Standard Library
from typing import Optional

# My stuff
from aiospotify import objects


class SimplePlaylist(objects.BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.collaborative: bool = data.get('collaborative', False)
        self.description: Optional[str] = data.get('description')
        self.external_urls: dict[Optional[str], Optional[str]] = data.get('external_urls', {})
        self.images: list[Optional[objects.Image]] = [objects.Image(image_data) for image_data in data.get('images', [])]
        self.owner: objects.User = objects.User(data.get('owner', {}))
        self.primary_colour: Optional[str] = data.get('primary_color')
        self.is_public: bool = data.get('public', False)
        self.snapshot_id: Optional[str] = data.get('snapshot_id')
        self.total_tracks: int = data.get('tracks', {}).get('total', 0)

    def __repr__(self) -> str:
        return f'<spotify.SimplePlaylist name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\' total_tracks=\'{self.total_tracks}\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')


class Playlist(objects.BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.collaborative: bool = data.get('collaborative', False)
        self.description: Optional[str] = data.get('description')
        self.external_urls: dict[Optional[str], Optional[str]] = data.get('external_urls', {})
        self.followers: objects.Followers = objects.Followers(data.get('followers', {}))
        self.images: list[Optional[objects.Image]] = [objects.Image(image_data) for image_data in data.get('images', [])]
        self.owner: objects.User = objects.User(data.get('owner', {}))
        self.primary_colour: Optional[str] = data.get('primary_color')
        self.is_public: bool = data.get('public', False)
        self.snapshot_id: Optional[str] = data.get('snapshot_id')
        self.total_tracks: int = data.get('tracks', {}).get('total', 0)

        self._tracks_paging = objects.PagingObject(data.get('tracks', []))
        self.tracks: list[Optional[objects.PlaylistTrack]] = [objects.PlaylistTrack(track_data) for track_data in self._tracks_paging.items]

    def __repr__(self) -> str:
        return f'<spotify.Playlist name=\'{self.name}\' id=\'{self.id}\' url=\'<{self.url}>\' total_tracks=\'{self.total_tracks}\'>'

    @property
    def url(self) -> Optional[str]:
        return self.external_urls.get('spotify')
