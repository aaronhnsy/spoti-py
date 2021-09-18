# Future
from __future__ import annotations

# My stuff
from aiospotify import objects
from typings.objects import SearchResultData


__all__ = (
    "SearchResult",
)


class SearchResult:

    def __init__(self, data: SearchResultData) -> None:

        self._albums_paging: objects.PagingObject | None = objects.PagingObject(paging) if (paging := data["albums"]) else None
        self._artists_paging: objects.PagingObject | None = objects.PagingObject(paging) if (paging := data["artists"]) else None
        self._playlists_paging: objects.PagingObject | None = objects.PagingObject(paging) if (paging := data["playlists"]) else None
        self._tracks_paging: objects.PagingObject | None = objects.PagingObject(paging) if (paging := data["tracks"]) else None
        self._shows_paging: objects.PagingObject | None = objects.PagingObject(paging) if (paging := data["shows"]) else None
        self._episodes_paging: objects.PagingObject | None = objects.PagingObject(paging) if (paging := data["episodes"]) else None

        self.albums: list[objects.SimpleAlbum | None] = [
            objects.SimpleAlbum(album) for album in self._albums_paging.items
        ] if self._albums_paging else []

        self.artists: list[objects.Artist | None] = [
            objects.Artist(artist) for artist in self._artists_paging.items
        ] if self._artists_paging else []

        self.playlists: list[objects.SimplePlaylist | None] = [
            objects.SimplePlaylist(playlist) for playlist in self._playlists_paging.items
        ] if self._playlists_paging else []

        self.tracks: list[objects.Track | None] = [
            objects.Track(track) for track in self._tracks_paging.items
        ] if self._tracks_paging else []

        #  self.shows = ...

        #  self.episodes = ...

    def __repr__(self) -> str:
        return f"<aiospotify.SearchResult albums={len(self.albums)}, artists={len(self.artists)}, playlists={len(self.playlists)}, tracks={len(self.tracks)}>"
