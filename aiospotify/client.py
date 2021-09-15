# Future
from __future__ import annotations

# Standard Library
import math
from collections import Sequence
from typing import Any, TypeVar

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

        for _ in range(1, math.ceil(album._tracks_paging.total / 50)):
            response = await self.http.get_album_tracks(_id, market=market, limit=50, offset=_ * 50)
            album.tracks.extend([objects.SimpleTrack(data) for data in objects.PagingObject(response).items])

        return album
