from __future__ import annotations

from typing import TypedDict

from .album import SimpleAlbum, SimpleAlbumData
from .artist import Artist, ArtistData
from .base import PagingObject, PagingObjectData
from .playlist import SimplePlaylist, SimplePlaylistData
from .track import Track, TrackData
# from .show import ShowData
# from .episode import SimpleEpisodeData


__all__ = (
    "SearchResultData",
    "SearchResult",
)


class SearchResultData(TypedDict):
    albums: PagingObjectData[SimpleAlbumData]
    artists: PagingObjectData[ArtistData]
    playlists: PagingObjectData[SimplePlaylistData]
    tracks: PagingObjectData[TrackData]
    # shows: PagingObjectData[ShowData]
    # episodes: PagingObjectData[SimpleEpisodeData]


class SearchResult:

    def __init__(self, data: SearchResultData) -> None:
        self._albums_paging: PagingObject[SimpleAlbumData] | None = PagingObject(paging) if (paging := data["albums"]) else None
        self._artists_paging: PagingObject[ArtistData] | None = PagingObject(paging) if (paging := data["artists"]) else None
        self._playlists_paging: PagingObject[SimplePlaylistData] | None = PagingObject(paging) if (paging := data["playlists"]) else None
        self._tracks_paging: PagingObject[TrackData] | None = PagingObject(paging) if (paging := data["tracks"]) else None
        # self._shows_paging: PagingObject | None = PagingObject(paging) if (paging := data["shows"]) else None
        # self._episodes_paging: PagingObject | None = PagingObject(paging) if (paging := data["episodes"]) else None

        self.albums: list[SimpleAlbum] = [
            SimpleAlbum(album) for album in self._albums_paging.items
        ] if self._albums_paging else []

        self.artists: list[Artist] = [
            Artist(artist) for artist in self._artists_paging.items
        ] if self._artists_paging else []

        self.playlists: list[SimplePlaylist] = [
            SimplePlaylist(playlist) for playlist in self._playlists_paging.items
        ] if self._playlists_paging else []

        self.tracks: list[Track] = [
            Track(track) for track in self._tracks_paging.items
        ] if self._tracks_paging else []

        #  self.shows = ...
        #  self.episodes = ...

    def __repr__(self) -> str:
        return f"<spotipy.SearchResult albums={len(self.albums)}, artists={len(self.artists)}, playlists=" \
               f"{len(self.playlists)}, tracks={len(self.tracks)}>"
