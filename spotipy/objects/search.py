from __future__ import annotations

from typing import TypedDict

from .album import SimpleAlbum, SimpleAlbumData
from .artist import Artist, ArtistData
from .base import PagingObject, PagingObjectData
from .playlist import SimplePlaylist, SimplePlaylistData
from .track import Track, TrackData
from .show import ShowData, Show
from .episode import SimpleEpisodeData, SimpleEpisode


__all__ = (
    "SearchResultData",
    "SearchResult",
)


class SearchResultData(TypedDict):
    albums: PagingObjectData[SimpleAlbumData]
    artists: PagingObjectData[ArtistData]
    playlists: PagingObjectData[SimplePlaylistData]
    tracks: PagingObjectData[TrackData]
    shows: PagingObjectData[ShowData]
    episodes: PagingObjectData[SimpleEpisodeData]


class SearchResult:

    def __init__(self, data: SearchResultData) -> None:

        self.albums: list[SimpleAlbum] = [SimpleAlbum(album) for album in PagingObject(data["albums"]).items]
        self.artists: list[Artist] = [Artist(artist) for artist in PagingObject(data["artists"]).items]
        self.playlists: list[SimplePlaylist] = [SimplePlaylist(playlist) for playlist in PagingObject(data["playlists"]).items]
        self.tracks: list[Track] = [Track(track) for track in PagingObject(data["tracks"]).items]
        self.shows: list[Show] = [Show(show) for show in PagingObject(data["shows"]).items]
        self.episodes: list[SimpleEpisode] = [SimpleEpisode(episode) for episode in PagingObject(data["episodes"]).items]

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: " \
               f"albums={len(self.albums)}, artists={len(self.artists)}, playlists={len(self.playlists)}, " \
               f"tracks={len(self.tracks)}, shows={len(self.shows)}, episodes={len(self.episodes)}>"
