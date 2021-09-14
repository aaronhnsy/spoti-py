# Future
from __future__ import annotations

# Standard Library
import asyncio
import urllib.parse
from typing import Any, ClassVar, Literal

# Packages
import aiohttp

# My stuff
from aiospotify import exceptions, objects, utils, values


__all__ = (
    "Route",
    "HTTPClient"
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


class HTTPClient:

    HEADERS = {
        "Content-Type": "application/json",
    }

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        session: aiohttp.ClientSession
    ) -> None:

        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._session: aiohttp.ClientSession = session

        self._client_credentials: objects.ClientCredentials | None = None

    def __repr__(self) -> str:
        return "<aiospotify.HTTPClient>"

    #

    async def get_token(self) -> objects.ClientCredentials:

        if not self._client_credentials:
            self._client_credentials = await objects.ClientCredentials.create(self._session, client_id=self._client_id, client_secret=self._client_secret)

        token = self._client_credentials
        if token.has_expired:
            await token.refresh(self._session, client_id=self._client_id, client_secret=self._client_secret)

        return self._client_credentials

    async def request(self, route: Route, parameters: dict[str, Any] | None = None) -> Any:

        if self._session is None:
            self._session = aiohttp.ClientSession()

        token = await self.get_token()
        self.HEADERS["Authorization"] = f"Bearer {token.access_token}"

        for tries in range(5):

            try:

                async with self._session.request(method=route.method, url=route.url, headers=self.HEADERS, params=parameters) as response:

                    data = await utils.json_or_text(response)

                    if isinstance(data, str):
                        raise exceptions.SpotifyException("Something went wrong, the Spotify API returned text.")

                    print(utils.to_json(data, indent=4))

                    if 200 <= response.status < 300:
                        return data

                    if response.status >= 500:
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    if error := data.get("error"):
                        raise values.EXCEPTION_MAPPING[response.status](error)

            except OSError as error:
                if tries < 4 and error.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        if response and response.status >= 500:
            raise values.EXCEPTION_MAPPING[response.status](data["error"])

        raise RuntimeError("This shouldn't happen.")

    async def close(self) -> None:
        if self._session:
            await self._session.close()

    ##############
    # ALBUMS API #
    ##############

    async def get_albums(
        self,
        ids: list[str],
        *,
        market: str | None
    ) -> dict[str, Any]:

        if len(ids) > 20:
            raise ValueError("'get_albums' can only take a maximum of 20 album ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/albums"), parameters=parameters)

    async def get_album(
        self,
        _id: str,
        /,
        *,
        market: str | None
    ) -> dict[str, Any]:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/albums/{id}", id=_id), parameters=parameters)

    async def get_album_tracks(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        limit: int | None,
        offset: int | None,
    ) -> dict[str, Any]:

        parameters = {}
        if market:
            parameters["market"] = market
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route('GET', '/albums/{id}/tracks', id=_id), parameters=parameters)

    ###############
    # ARTISTS API #
    ###############

    async def get_artists(
        self,
        ids: list[str],
        *,
        market: str | None
    ) -> dict[str, Any]:

        if len(ids) > 50:
            raise ValueError("'get_artists' can only take a maximum of 50 artist ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/artists"), parameters=parameters)

    async def get_artist(
        self,
        _id: str,
        /,
        *,
        market: str | None
    ) -> dict[str, Any]:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/artists/{id}", id=_id), parameters=parameters)

    async def get_artist_top_tracks(
        self,
        _id: str,
        /,
        *,
        market: str = "GB"
    ) -> dict[str, Any]:

        parameters = {"market": market}
        return await self.request(Route("GET", "/artists/{id}/top-tracks", id=_id), parameters=parameters)

    async def get_related_artists(
        self,
        _id: str,
        /,
        *,
        market: str | None
    ) -> dict[str, Any]:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/artists/{id}/related-artists", id=_id), parameters=parameters)

    async def get_artist_albums(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        include_groups: list[objects.IncludeGroups] | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:

        parameters = {}
        if market:
            parameters["market"] = market
        if include_groups:
            parameters["include_groups"] = ",".join(include_group.value for include_group in include_groups)
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/artists/{id}/albums", id=_id), parameters=parameters)

    ##############
    # BROWSE API #
    ##############

    async def get_new_releases(
        self,
        *,
        country: str | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:
        raise NotImplementedError

    async def get_featured_playlists(
        self,
        *,
        country: str | None,
        locale: str | None,
        timestamp: str | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:
        raise NotImplementedError

    async def get_all_categories(
        self,
        *,
        country: str | None,
        locale: str | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:
        raise NotImplementedError

    async def get_category(
        self,
        _id: str,
        /,
        *,
        country: str | None,
        locale: str | None,
    ) -> dict[str, Any]:
        raise NotImplementedError

    async def get_category_playlists(
        self,
        _id: str,
        /,
        *,
        country: str | None,
        locale: str | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:
        raise NotImplementedError

    async def get_recommendations(
        self,
        *,
        seed_artist_ids: list[str] | None,
        seed_genres: list[str] | None,
        seed_track_ids: list[str] | None,
        limit: int | None,
        market: str | None,
        **kwargs
    ) -> dict[str, Any]:

        if len([seed for seeds in [seed_artist_ids or [], seed_genres or [], seed_track_ids or []] for seed in seeds]) > 5:
            raise ValueError("Too many seed values provided, maximum of 5.")

        parameters = {}
        if seed_artist_ids:
            parameters["seed_artists"] = ",".join(seed_artist_ids)
        if seed_genres:
            parameters["seed_genres"] = ",".join(seed_genres)
        if seed_track_ids:
            parameters["seed_tracks"] = ",".join(seed_track_ids)

        for key, value in kwargs.items():
            if key not in values.VALID_SEED_KWARGS:
                raise ValueError(f"'{key}' was not a valid kwarg.")
            parameters[key] = value

        if limit:
            if limit < 1 or limit > 100:
                raise ValueError("'limit' must be between 1 and 100 inclusive.")
            parameters["limit"] = limit

        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/recommendations"), parameters=parameters)

    async def get_recommendation_genres(
        self
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/recommendations/available-genre-seeds"))

    ###############
    # EPISODE API #
    ###############

    ...

    ##############
    # FOLLOW API #
    ##############

    ...

    ###############
    # LIBRARY API #
    ###############

    ...

    ###############
    # MARKETS API #
    ###############

    async def get_available_markets(
        self
    ) -> list[str]:
        return await self.request(Route("GET", "/markets"))

    #######################
    # PERSONALIZATION API #
    #######################

    ...

    ##############
    # PLAYER API #
    ##############

    async def get_user_current_playback(
        self,
        *,
        market: str | None,
    ) -> dict[str, Any]:

        parameters = {"additional_types": "track"}
        if market:
            parameters["market"] = market

        return await self.request(Route('GET', '/me/player'), parameters=parameters)

    ...

    #################
    # PLAYLISTS API #
    #################

    async def get_playlist(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        fields: str | None,
    ) -> dict[str, Any]:

        parameters = {"additional_types": "track"}
        if market:
            parameters["market"] = market
        if fields:
            parameters["fields"] = fields

        return await self.request(Route("GET", "/playlists/{id}", id=_id), parameters=parameters)

    async def get_playlist_items(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        fields: str | None,
        limit: int | None,
        offset: int | None,
    ) -> dict[str, Any]:

        parameters = {"additional_types": "track"}
        if market:
            parameters["market"] = market
        if fields:
            parameters["fields"] = fields
        if limit:
            if limit < 1 or limit > 100:
                raise ValueError("'limit' must be between 1 and 100 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route('GET', '/playlists/{id}/tracks', id=_id), parameters=parameters)

    ##############
    # SEARCH API #
    ##############

    async def search(
        self,
        query: str,
        search_types: list[objects.SearchType],
        market: str | None,
        limit: int | None,
        offset: int | None,
        include_external: bool = False
    ) -> dict[str, Any]:

        parameters: dict[str, Any] = {
            "q": query.replace(" ", "+"),
            "type": ",".join(search_type.value for search_type in search_types)
        }

        if market:
            parameters["market"] = market
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset
        if include_external:
            parameters["include_external"] = "audio"

        return await self.request(Route("GET", "/search"), parameters=parameters)

    #############
    # SHOWS API #
    #############

    ...

    ##############
    # TRACKS API #
    ##############

    async def get_tracks(
        self,
        ids: list[str],
        *,
        market: str | None
    ) -> dict[str, Any]:

        if len(ids) > 50:
            raise ValueError("'get_tracks' can only take a maximum of 50 track ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/tracks"), parameters=parameters)

    async def get_track(
        self,
        _id: str,
        /,
        *,
        market: str | None
    ) -> dict[str, Any]:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/tracks/{id}", id=_id), parameters=parameters)

    async def get_several_track_audio_features(
        self,
        ids: list[str]
    ) -> dict[str, Any]:

        if len(ids) > 100:
            raise ValueError("'get_several_track_audio_features' can only take a maximum of 100 track ids.")

        return await self.request(Route("GET", "/audio-features"), parameters={"ids": ",".join(ids)})

    async def get_track_audio_features(
        self,
        _id: str,
        /
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/audio-features/{id}", id=_id))

    async def get_track_audio_analysis(
        self,
        _id: str,
        /,
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/audio-analysis/{id}", id=_id))

    #############
    # USERS API #
    #############

    ...
