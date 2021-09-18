# Future
from __future__ import annotations

# Standard Library
import math
from collections.abc import Sequence
from typing import TypeVar

# Packages
import aiohttp

# My stuff
from aiospotify import http, objects, utils


__all__ = (
    "Client",
)


ID = TypeVar("ID", bound=str)


class Client:

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: aiohttp.ClientSession = utils.MISSING
    ) -> None:

        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._session: aiohttp.ClientSession = session

        self.http = http.HTTPClient(client_id=self._client_id, client_secret=self._client_secret, session=self._session)

    def __repr__(self) -> str:
        return "<aiospotify.Client>"

    #

    async def close(self) -> None:

        if not self.http._session:
            return

        await self.http.close()

    # ALBUMS API

    async def get_albums(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = None
    ) -> dict[ID, objects.Album | None]:

        response = await self.http.get_albums(ids=ids, market=market)
        return dict(zip(ids, [objects.Album(data) if data else None for data in response["albums"]]))

    async def get_album(
        self,
        _id: str,
        /,
        *,
        market: str | None = None
    ) -> objects.Album:

        response = await self.http.get_album(_id, market=market)
        return objects.Album(response)

    async def get_album_tracks(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[objects.SimpleTrack]:

        response = await self.http.get_album_tracks(_id, market=market, limit=limit, offset=offset)
        return [objects.SimpleTrack(data) for data in objects.PagingObject(response).items]

    async def get_all_album_tracks(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
    ) -> list[objects.SimpleTrack]:

        response = await self.http.get_album_tracks(_id, market=market, limit=50, offset=0)
        paging = objects.PagingObject(response)

        tracks = [objects.SimpleTrack(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or less tracks and we already have them so just return them
            return tracks

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_album_tracks(_id, market=market, limit=50, offset=_ * 50)
            tracks.extend([objects.SimpleTrack(data) for data in objects.PagingObject(response).items])

        return tracks

    async def get_full_album(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
    ) -> objects.Album:

        album = await self.get_album(_id, market=market)

        if album._tracks_paging.total <= 50:  # The album has 50 or less tracks already so we can just return it now.
            return album

        for _ in range(2, math.ceil(album._tracks_paging.total / 50)):
            response = await self.http.get_album_tracks(_id, market=market, limit=50, offset=_ * 50)
            album.tracks.extend([objects.SimpleTrack(data) for data in objects.PagingObject(response).items])

        return album

    # ARTISTS API

    async def get_artists(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = None
    ) -> dict[ID, objects.Artist | None]:

        response = await self.http.get_artists(ids=ids, market=market)
        return dict(zip(ids, [objects.Artist(data) if data else None for data in response["artists"]]))

    async def get_artist(
        self,
        _id: str,
        /,
        *,
        market: str | None = None
    ) -> objects.Artist:

        response = await self.http.get_artist(_id, market=market)
        return objects.Artist(response)

    async def get_artist_top_tracks(
        self,
        _id: str,
        /,
        *,
        market: str = "GB"
    ) -> list[objects.Track]:

        response = await self.http.get_artist_top_tracks(_id, market=market)
        return [objects.Track(data) for data in response["tracks"]]

    async def get_related_artists(
        self,
        _id: str,
        /,
        *,
        market: str | None = None
    ) -> list[objects.Artist]:

        response = await self.http.get_related_artists(_id, market=market)
        return [objects.Artist(data) for data in response["artists"]]

    async def get_artist_albums(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        include_groups: Sequence[objects.IncludeGroup] | None = [objects.IncludeGroup.ALBUM],
        limit: int | None = None,
        offset: int | None = None
    ) -> list[objects.SimpleAlbum]:

        response = await self.http.get_artist_albums(_id, market=market, include_groups=include_groups, limit=limit, offset=offset)
        return [objects.SimpleAlbum(data) for data in objects.PagingObject(response).items]

    async def get_all_artist_albums(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        include_groups: Sequence[objects.IncludeGroup] | None = [objects.IncludeGroup.ALBUM],
    ) -> list[objects.SimpleAlbum]:

        response = await self.http.get_artist_albums(_id, market=market, include_groups=include_groups, limit=50, offset=0)
        paging = objects.PagingObject(response)

        albums = [objects.SimpleAlbum(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or less tracks and we already have them so just return them
            return albums

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_artist_albums(_id, market=market, include_groups=include_groups, limit=50, offset=_ * 50)
            albums.extend([objects.SimpleAlbum(data) for data in objects.PagingObject(response).items])

        return albums

    # BROWSE API

    ...

    async def get_recommendations(
        self,
        *,
        seed_artist_ids: Sequence[str] | None = None,
        seed_genres: Sequence[str] | None = None,
        seed_track_ids: Sequence[str] | None = None,
        limit: int | None = None,
        market: str | None = None,
        **kwargs
    ) -> objects.Recommendation:

        response = await self.http.get_recommendations(
            seed_artist_ids=seed_artist_ids,
            seed_genres=seed_genres,
            seed_track_ids=seed_track_ids,
            limit=limit,
            market=market,
            **kwargs
        )
        return objects.Recommendation(response)

    async def get_recommendation_genres(
        self
    ) -> list[str]:

        response = await self.http.get_recommendation_genres()
        return response["genres"]

    # EPISODE API

    ...

    # FOLLOW API

    ...

    # LIBRARY API

    ...

    # MARKETS API

    async def get_available_markets(
        self
    ) -> list[str]:

        response = await self.http.get_available_markets()
        return response["markets"]

    # PERSONALIZATION API

    ...

    # PLAYLISTS API

    async def get_playlist(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        fields: str | None = None
    ) -> objects.Playlist:

        response = await self.http.get_playlist(_id, market=market, fields=fields)
        return objects.Playlist(response)

    async def get_playlist_items(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        fields: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[objects.PlaylistTrack]:

        response = await self.http.get_playlist_items(_id, market=market, fields=fields, limit=limit, offset=offset)
        return [objects.PlaylistTrack(data) for data in objects.PagingObject(response).items]

    async def get_all_playlist_items(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        fields: str | None = None,
    ) -> list[objects.PlaylistTrack]:

        response = await self.http.get_playlist_items(_id, market=market, fields=fields, limit=50, offset=0)
        paging = objects.PagingObject(response)

        items = [objects.PlaylistTrack(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or less tracks and we already have them so just return them
            return items

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_playlist_items(_id, market=market, fields=fields, limit=50, offset=_ * 50)
            items.extend([objects.PlaylistTrack(data) for data in objects.PagingObject(response).items])

        return items

    async def get_full_playlist(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        fields: str | None = None,
    ) -> objects.Playlist:

        playlist = await self.get_playlist(_id, market=market, fields=fields)

        if playlist._tracks_paging.total <= 50:  # The playlist has 50 or less tracks already so we can just return it now.
            return playlist

        for _ in range(2, math.ceil(playlist._tracks_paging.total / 50)):
            response = await self.http.get_playlist_items(_id, market=market, fields=fields, limit=50, offset=_ * 50)
            playlist.tracks.extend([objects.PlaylistTrack(data) for data in objects.PagingObject(response).items])

        return playlist

    # SEARCH API

    async def search(
        self,
        query: str,
        /,
        *,
        search_types: Sequence[objects.SearchType] | None = None,
        market: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        include_external: bool = False
    ) -> objects.SearchResult:

        response = await self.http.search(query, search_types=search_types, market=market, limit=limit, offset=offset, include_external=include_external)
        return objects.SearchResult(response)

    # SHOWS API

    ...

    # TRACKS API #

    async def get_tracks(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = None,
    ) -> dict[ID, objects.Track | None]:

        response = await self.http.get_tracks(ids=ids, market=market)
        return dict(zip(ids, [objects.Track(data) if data else None for data in response["tracks"]]))

    async def get_track(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
    ) -> objects.Track:

        response = await self.http.get_track(_id, market=market)
        return objects.Track(response)

    async def get_several_tracks_audio_features(
        self,
        ids: Sequence[ID]
    ) -> dict[ID, objects.AudioFeatures | None]:

        response = await self.http.get_several_tracks_audio_features(ids)
        return dict(zip(ids, [objects.AudioFeatures(data) if data else None for data in response["audio_features"]]))

    async def get_track_audio_features(
        self,
        _id: str,
        /
    ) -> objects.AudioFeatures:

        response = await self.http.get_track_audio_features(_id)
        return objects.AudioFeatures(response)

    ...

    # USERS API

    ...
