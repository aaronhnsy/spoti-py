# Future
from __future__ import annotations

# My stuff
from aiospotify import objects


class SearchResult:

    def __init__(self, data: dict) -> None:

        self._albums_paging = objects.PagingObject(data.get('albums', {}))
        self._artists_paging = objects.PagingObject(data.get('artists', {}))
        self._playlists_paging = objects.PagingObject(data.get('playlists', {}))
        self._tracks_paging = objects.PagingObject(data.get('tracks', {}))

        self.albums = [objects.SimpleAlbum(album_data) for album_data in self._albums_paging.items] if self._albums_paging.items else None
        self.artists = [objects.Artist(artist_data) for artist_data in self._artists_paging.items] if self._artists_paging.items else None
        self.playlists = [objects.SimplePlaylist(playlist_data) for playlist_data in self._playlists_paging.items] if self._playlists_paging.items else None
        self.tracks = [objects.Track(track_data) for track_data in self._tracks_paging.items] if self._tracks_paging.items else None

    def __repr__(self) -> str:
        return f'<spotify.SearchResult albums={self.albums} artists={self.artists} playlists={self.playlists} tracks={self.tracks}>'
