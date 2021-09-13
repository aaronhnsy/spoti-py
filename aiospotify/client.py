# Future
from __future__ import annotations

# Standard Library
import asyncio
import json
import math
import urllib.parse
from typing import Any, ClassVar, Literal

# Packages
import aiohttp

# My stuff
from aiospotify import objects, utils, values


__all__ = (
    "Route",
    "Client"
)


class Route:

    BASE: ClassVar[str] = f"{values.API_BASE}/v1"

    def __init__(self, method: Literal["GET", "POST", "DELETE", "PATCH"], path: str, /, **parameters):

        self.method = method
        self.path = path

        url = self.BASE + self.path
        if parameters:
            url = url.format_map({key: urllib.parse.quote(value) if isinstance(value, str) else value for key, value in parameters.items()})

        self.url: str = url


class Client:

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: aiohttp.ClientSession | None = None
    ) -> None:

        self._client_id: str = client_id
        self._client_secret: str = client_secret

        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession()

        self._client_credentials: objects.ClientCredentials | None = None

    def __repr__(self) -> str:
        return "<aiospotify.Client>"

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def client_secret(self) -> str:
        return self._client_secret

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    #

    async def _get_token(self) -> objects.ClientCredentials:

        if not self._client_credentials:
            self._client_credentials = await objects.ClientCredentials.create(self.session, client_id=self.client_id, client_secret=self.client_secret)

        token = self._client_credentials

        if token.has_expired:
            await token.refresh(self.session, client_id=self.client_id, client_secret=self.client_secret)

        return self._client_credentials

    async def _request(self, route: Route, parameters: dict[str, Any] | None = None):
        token = await self._get_token()

        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {token.access_token}"
        }

        for tries in range(5):

            try:

                async with self.session.request(method=route.method, url=route.url, headers=headers, params=parameters) as response:
                    data = await utils.json_or_text(response)

                    if 300 > response.status >= 200:
                        print(json.dumps(data, indent=4))
                        return data

                    # TODO: Implement some kind of ratelimit handling.

                    if response.status in {500, 502, 503}:
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    if data.get("error"):
                        raise values.EXCEPTION_MAPPING.get(response.status)(data)

            except OSError as e:
                if tries < 4 and e.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

    # SEARCH API

    async def search(self, query, search_types=None, market=None, limit=50, offset=0, include_external=False):

        if search_types is None:
            search_types = [objects.SearchType.ALBUM, objects.SearchType.ARTIST, objects.SearchType.PLAYLIST, objects.SearchType.TRACK]

        parameters = {"query": query.replace(" ", "+"), "limit": limit, "offset": offset, "type": ",".join(search_type.value for search_type in search_types)}
        if market:
            parameters["market"] = market
        if include_external is True:
            parameters["include_external"] = "audio"

        paging_response = await self._request(Route("GET", "/search"), parameters=parameters)
        return objects.SearchResult(paging_response)

    # BROWSE API

    async def get_new_releases(self, *, country=None, limit=50, offset=0):
        pass

    async def get_featured_playlists(self):
        pass

    async def get_all_categories(self):
        pass

    async def get_category(self):
        pass

    async def get_category_playlist(self):
        pass

    async def get_recommendations(self, seed, *, limit=50, market=None):

        seed.parameters.update({"limit": limit})
        if market:
            seed.parameters["market"] = market

        response = await self._request(Route("GET", "/recommendations"), parameters=seed.parameters)
        return objects.Recommendation(response)

    async def get_recommendation_genres(self):

        response = await self._request(Route("GET", "/recommendations/available-genre-seeds"))
        return response

    # PLAYLIST API

    ...

    # ARTISTS API

    async def get_artists(self, artist_ids, *, market=None):

        if len(artist_ids) > 50:
            raise ValueError("\"get_artists\" can only take a maximum of 50 artists ids.")

        parameters = {"ids": ",".join(artist_ids)}
        if market:
            parameters["market"] = market

        response = await self._request(Route("GET", "/artists"), parameters=parameters)
        return dict(zip(artist_ids, [objects.Artist(data) if data is not None else None for data in response.get("artists")]))

    async def get_artist(self, artist_id, *, market=None):
        response = await self._request(Route("GET", "/artists/{artist_id}", artist_id=artist_id), parameters={"market": market} if market else None)
        return objects.Artist(response)

    async def get_artist_top_tracks(self, artist_id, *, market="GB"):
        request = Route("GET", "/artists/{artist_id}/top-tracks", artist_id=artist_id)
        response = await self._request(request, parameters={"market": market} if market else None)
        return [objects.Track(data) for data in response.get("tracks")]

    async def get_related_artists(self, artist_id, *, market=None):
        request = Route("GET", "/artists/{artist_id}/related-artists", artist_id=artist_id)
        response = await self._request(request, parameters={"market": market} if market else None)
        return [objects.Artist(data) for data in response.get("artists")]

    async def get_artist_albums(self, artist_id, *, market=None, include_groups=None, limit=50, offset=0):

        if include_groups is None:
            include_groups = [objects.IncludeGroups.album]

        parameters = {"limit": limit, "offset": offset, "include_groups": ",".join(include_group.value for include_group in include_groups)}
        if market:
            parameters["market"] = market

        paging_response = await self._request(Route("GET", "/artists/{artist_id}/albums", artist_id=artist_id), parameters=parameters)
        return [objects.SimpleAlbum(data) for data in objects.PagingObject(paging_response).items]

    async def get_all_artist_albums(self, artist_id, *, market=None, include_groups=None):

        if include_groups is None:
            include_groups = [objects.IncludeGroups.album]

        parameters = {"limit": 50, "offset": 0, "include_groups": ",".join(include_group.value for include_group in include_groups)}
        if market:
            parameters["market"] = market

        paging_response = await self._request(Route("GET", "/artists/{artist_id}/albums", artist_id=artist_id), parameters=parameters)
        paging = objects.PagingObject(paging_response)
        albums = [objects.SimpleAlbum(data) for data in paging.items]

        if paging.total <= 50:  # We already have the first 50, so we can just return the albums we have so far.
            return albums

        for _ in range(1, math.ceil(paging.total / 50)):
            parameters["offset"] = _ * 50
            paging_response = await self._request(Route("GET", "/artists/{artist_id}/albums", artist_id=artist_id), parameters=parameters)
            albums.extend([objects.SimpleAlbum(data) for data in objects.PagingObject(paging_response).items])

        return albums

    # PLAYER API

    async def get_user_current_playback(self, *, market=None):

        response = await self._request(Route("GET", "/me/player"), parameters={"market": market} if market else None)
        print(response)
        if response is None:
            return None

        return objects.CurrentlyPlayingContext(response)

    # ALBUMS API

    async def get_albums(self, album_ids, *, market=None):

        if len(album_ids) > 20:
            raise ValueError("\"get_albums\" can only take a maximum of 20 album ids.")

        parameters = {"ids": ",".join(album_ids)}
        if market:
            parameters["market"] = market

        response = await self._request(Route("GET", "/albums"), parameters=parameters)
        return dict(zip(album_ids, [objects.Album(data) if data is not None else None for data in response.get("albums")]))

    async def get_album(self, album_id, *, market=None):
        response = await self._request(Route("GET", "/albums/{album_id}", album_id=album_id), parameters={"market": market} if market else None)
        return objects.Album(response)

    async def get_full_album(self, album_id, *, market=None):

        album = await self.get_album(album_id=album_id, market=market)
        if album._tracks_paging.total <= 50:
            return album

        parameters = {"limit": 50, "offset": 50}
        if market:
            parameters["market"] = market

        for _ in range(1, math.ceil(album._tracks_paging.total / 50)):
            parameters["offset"] = _ * 50
            paging_response = await self._request(Route("GET", "/albums/{album_id}/tracks", album_id=album.id), parameters=parameters)
            album.tracks.extend([objects.SimpleTrack(data) for data in objects.PagingObject(paging_response).items])

        return album

    async def get_album_tracks(self, album_id, *, market=None, limit=50, offset=0):

        parameters = {"limit": limit, "offset": offset}
        if market:
            parameters["market"] = market

        paging_response = await self._request(Route("GET", "/albums/{album_id}/tracks", album_id=album_id), parameters=parameters)
        return [objects.SimpleTrack(data) for data in objects.PagingObject(paging_response).items]

    async def get_all_album_tracks(self, album_id, *, market=None):

        parameters = {"limit": 50, "offset": 0}
        if market:
            parameters["market"] = market

        paging_response = await self._request(Route("GET", "/albums/{album_id}/tracks", album_id=album_id), parameters=parameters)
        paging = objects.PagingObject(paging_response)
        tracks = [objects.SimpleTrack(data) for data in paging.items]

        if paging.total <= 50:  # We already have the first 50, so we can just return the tracks we have so far.
            return tracks

        for _ in range(1, math.ceil(paging.total / 50)):
            parameters["offset"] = _ * 50
            paging_response = await self._request(Route("GET", "/albums/{album_id}/tracks", album_id=album_id), parameters=parameters)
            tracks.extend([objects.SimpleTrack(data) for data in objects.PagingObject(paging_response).items])

        return tracks

    # TRACKS API

    async def get_tracks(self, track_ids, *, market=None):

        if len(track_ids) > 50:
            raise ValueError("\"get_tracks\" can only take a maximum of 50 track ids.")

        parameters = {"ids": ",".join(track_ids)}
        if market:
            parameters["market"] = market

        response = await self._request(Route("GET", "/tracks"), parameters=parameters)
        return dict(zip(track_ids, [objects.Track(data) if data is not None else None for data in response.get("tracks")]))

    async def get_track(self, track_id, market=None):
        response = await self._request(Route("GET", "/tracks/{track_id}", track_id=track_id), parameters={"market": market} if market else None)
        return objects.Track(response)

    async def get_tracks_audio_features(self, track_ids):

        if len(track_ids) > 100:
            raise ValueError("\"get_tracks_audio_features\" can only take a maximum of 100 track ids.")

        response = await self._request(Route("GET", "/audio-features"), parameters={"ids": ",".join(track_ids)})
        features = [objects.AudioFeatures(data) if data is not None else None for data in response.get("audio_features")]
        return dict(zip(track_ids, features))

    async def get_track_audio_features(self, track_id):
        response = await self._request(Route("GET", "/audio-features/{track_id}", track_id=track_id))
        return objects.AudioFeatures(response)
