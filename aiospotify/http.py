# Future
from __future__ import annotations

# Standard Library
import asyncio
import urllib.parse
from collections.abc import Sequence
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

    BASE_URL: ClassVar[str] = f"https://api.spotify.com/v1"

    def __init__(
        self,
        method: Literal["GET", "POST", "DELETE", "PATCH", "PUT"],
        path: str,
        /,
        **parameters
    ) -> None:

        self.method = method
        self.path = path

        url = self.BASE_URL + self.path
        if parameters:
            url = url.format_map({key: urllib.parse.quote(value) if isinstance(value, str) else value for key, value in parameters.items()})

        self.url: str = url

    def __repr__(self) -> str:
        return f"<aiospotify.Route method={self.method} url={self.url}>"


class HTTPClient:

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

    async def request(
        self,
        route: Route,
        /,
        *,
        parameters: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None
    ) -> Any:

        if not self._session:
            self._session = aiohttp.ClientSession()

        if not self._client_credentials:
            self._client_credentials = await objects.ClientCredentials.create(self._client_id, self._client_secret, session=self._session)

        if self._client_credentials.is_expired():
            await self._client_credentials.refresh(session=self._session)

        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {self._client_credentials.access_token}"
        }

        for tries in range(5):

            try:

                async with self._session.request(
                        method=route.method,
                        url=route.url,
                        headers=headers,
                        params=parameters,
                        data=data
                ) as response:

                    response_data = await utils.json_or_text(response)

                    if isinstance(response_data, str):
                        raise exceptions.SpotifyException("Something went wrong, the Spotify API returned text.")

                    if 200 <= response.status < 300:
                        return response_data

                    if response.status >= 500:
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    if error := response_data.get("error"):
                        raise values.EXCEPTION_MAPPING[response.status](error)

            except OSError as error:
                if tries < 4 and error.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        if response and response.status >= 500:
            raise values.EXCEPTION_MAPPING[response.status](response_data["error"])

        raise RuntimeError("This shouldn't happen.")

    async def close(self) -> None:

        if not self._session:
            return

        await self._session.close()

    # ALBUMS API

    async def get_albums(
        self,
        ids: Sequence[str],
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

        return await self.request(Route("GET", "/albums/{id}/tracks", id=_id), parameters=parameters)

    # ARTISTS API

    async def get_artists(
        self,
        ids: Sequence[str],
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
        include_groups: Sequence[objects.IncludeGroup] | None,
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

    # BROWSE API

    async def get_new_releases(
        self,
        *,
        country: str | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:

        parameters = {}
        if country:
            parameters["country"] = country
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/browse/new-releases"), parameters=parameters)

    async def get_featured_playlists(
        self,
        *,
        country: str | None,
        locale: str | None,
        timestamp: str | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:

        parameters = {}
        if country:
            parameters["country"] = country
        if locale:
            parameters["locale"] = locale
        if timestamp:
            parameters["timestamp"] = timestamp
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/browse/featured-playlists"), parameters=parameters)

    async def get_categories(
        self,
        *,
        country: str | None,
        locale: str | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:

        parameters = {}
        if country:
            parameters["country"] = country
        if locale:
            parameters["locale"] = locale
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/browse/categories"), parameters=parameters)

    async def get_category(
        self,
        _id: str,
        /,
        *,
        country: str | None,
        locale: str | None,
    ) -> dict[str, Any]:

        parameters = {}
        if country:
            parameters["country"] = country
        if locale:
            parameters["locale"] = locale

        return await self.request(Route("GET", "/browse/categories/{id}", id=_id), parameters=parameters)

    async def get_category_playlists(
        self,
        _id: str,
        /,
        *,
        country: str | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, Any]:

        parameters = {}
        if country:
            parameters["country"] = country
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/browse/categories/{id}/playlists", id=_id), parameters=parameters)

    async def get_recommendations(
        self,
        *,
        seed_artist_ids: Sequence[str] | None,
        seed_genres: Sequence[str] | None,
        seed_track_ids: Sequence[str] | None,
        limit: int | None,
        market: str | None,
        **kwargs
    ) -> dict[str, Any]:

        seeds = len([seed for seeds in [seed_artist_ids or [], seed_genres or [], seed_track_ids or []] for seed in seeds])
        if seeds <= 0 or seeds > 5:
            raise ValueError("Too many or no seed values provided. Minimum 1, Maximum 5.")

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

    # EPISODE API

    ...

    # FOLLOW API

    ...

    # LIBRARY API

    ...

    # MARKETS API

    async def get_available_markets(
        self
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/markets"))

    # PERSONALIZATION API

    async def get_current_users_top_artists(
        self,
        *,
        time_range: objects.TimeRange | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, None]:

        parameters = {}
        if time_range:
            parameters["time_range"] = time_range.value
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/me/top/artists"), parameters=parameters)

    async def get_current_users_top_tracks(
        self,
        *,
        time_range: objects.TimeRange | None,
        limit: int | None,
        offset: int | None
    ) -> dict[str, None]:

        parameters = {}
        if time_range:
            parameters["time_range"] = time_range.value
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/me/top/tracks"), parameters=parameters)

    # PLAYER API

    async def get_current_user_playback(
        self,
        *,
        market: str | None,
    ) -> dict[str, Any]:

        parameters = {"additional_types": "track"}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/me/player"), parameters=parameters)

    async def transfer_current_user_playback(
        self,
        *,
        device_id: str,
        play: bool | None
    ) -> None:

        data: dict[str, Any] = {"device_ids": [device_id]}
        if play:
            data["play"] = play

        return await self.request(Route("PUT", "/me/player"), data=data)

    async def get_current_user_available_devices(
        self,
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/me/player/devices"))

    async def get_current_user_playing_track(
        self,
        *,
        market: str | None,
    ) -> dict[str, Any]:

        parameters = {"additional_types": "track"}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/me/player/currently-playing"), parameters=parameters)

    async def start_current_user_playback(
        self,
    ) -> ...:
        raise NotImplementedError

    async def pause_current_user_playback(
        self,
        *,
        device_id: str | None
    ) -> None:

        parameters = {}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/pause"), parameters=parameters)

    async def skip_forward_current_user_playback(
        self,
        *,
        device_id: str | None
    ) -> None:

        parameters = {}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("POST", "/me/player/next"), parameters=parameters)

    async def skip_backward_current_user_playback(
        self,
        *,
        device_id: str | None
    ) -> None:

        parameters = {}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("POST", "/me/player/previous"), parameters=parameters)

    async def seek_current_user_playback(
        self,
        *,
        position_ms: int,
        device_id: str | None
    ) -> None:

        parameters: dict[str, Any] = {"position_ms": position_ms}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/seek"), parameters=parameters)

    async def set_current_user_repeat_mode(
        self,
        *,
        repeat_mode: objects.RepeatMode,
        device_id: str | None
    ) -> None:

        parameters = {"state": repeat_mode.value}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/repeat"), parameters=parameters)

    async def set_current_user_volume(
        self,
        *,
        volume_percent: int,
        device_id: str | None
    ) -> None:

        if volume_percent < 0 or volume_percent > 100:
            raise ValueError("'volume_percent' must between 1 and 100 inclusive.")

        parameters: dict[str, Any] = {"volume_percent": volume_percent}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/volume"), parameters=parameters)

    async def set_current_user_shuffle_state(
        self,
        *,
        state: bool,
        device_id: str | None
    ) -> None:

        parameters: dict[str, Any] = {"state": state}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/shuffle"), parameters=parameters)

    async def get_current_users_recently_played_tracks(
        self,
        *,
        limit: int | None,
        before: int | None,
        after: int | None,
    ) -> dict[str, Any]:

        if before and after:
            raise ValueError("'before' and 'after' can not both be specified.")

        parameters = {}
        if limit:
            parameters["limit"] = limit
        if before:
            parameters["before"] = before
        if after:
            parameters["after"] = after

        return await self.request(Route("GET", "/me/player/recently-played"), parameters=parameters)

    async def add_item_to_current_user_queue(
        self,
        *,
        uri: str,
        device_id: str | None
    ) -> None:

        parameters = {"uri": uri}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("POST", "/me/player/queue"), parameters=parameters)

    # PLAYLISTS API

    async def get_current_user_playlists(
        self,
        *,
        limit: int | None,
        offset: int | None,
    ) -> dict[str, Any]:

        parameters = {}
        if limit:
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/me/playlists"), parameters=parameters)

    async def get_user_playlists(
        self,
        _id: str,
        /,
        *,
        limit: int | None,
        offset: int | None,
    ) -> dict[str, Any]:

        parameters = {}
        if limit:
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/users/{id}/playlists", id=_id), parameters=parameters)

    async def create_playlist(
        self,
        *,
        user_id: str,
        name: str,
        public: bool | None,
        collaborative: bool | None,
        description: str | None
    ) -> dict[str, Any]:

        if collaborative and public:
            raise ValueError("collaborative playlists must not be public.")

        data: dict[str, Any] = {"name": name}
        if public:
            data["public"] = public
        if collaborative:
            data["collaborative"] = collaborative
        if description:
            data["description"] = description

        return await self.request(Route("POST", "/users/{user_id}/playlists", user_id=user_id), data=data)

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

    async def change_playlist_details(
        self,
        _id: str,
        /,
        *,
        name: str | None,
        public: bool | None,
        collaborative: bool | None,
        description: str | None
    ) -> None:

        if collaborative and public:
            raise ValueError("collaborative playlists must not be public.")

        data = {}
        if name:
            data["name"] = name
        if public:
            data["public"] = public
        if collaborative:
            data["collaborative"] = collaborative
        if description:
            data["description"] = description

        return await self.request(Route("PUT", "/playlists/{id}", id=_id), data=data)

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

        parameters: dict[str, Any] = {"additional_types": "track"}
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

        return await self.request(Route("GET", "/playlists/{id}/tracks", id=_id), parameters=parameters)

    async def add_items_to_playlist(
        self,
        _id: str,
        /,
        *,
        position: int | None,
        uris: Sequence[str],
    ) -> dict[str, Any]:

        data: dict[str, Any] = {"uris": uris}
        if position:
            data["position"] = position

        return await self.request(Route("POST", "/playlists/{id}/tracks", id=_id), data=data)

    async def reorder_playlist_items(
        self,
        _id: str,
        /,
        *,
        range_start: int,
        insert_before: int,
        range_length: int | None,
        snapshot_id: str | None,
    ) -> dict[str, Any]:

        data: dict[str, Any] = {
            "range_start": range_start,
            "insert_before": insert_before
        }
        if range_length:
            data["range_length"] = range_length
        if snapshot_id:
            data["snapshot_id"] = snapshot_id

        return await self.request(Route("PUT", "/playlists/{id}/tracks", id=_id), data=data)

    async def replace_playlist_items(
        self,
        _id: str,
        /,
        *,
        uris: Sequence[str] | None
    ) -> None:

        data: dict[str, Any] = {"uris": None}
        if uris:
            if len(uris) > 100:
                raise ValueError("'uris' must be less than 100 uris.")
            data["uris"] = uris

        return await self.request(Route("PUT", "/playlists/{id}/tracks", id=_id), data=data)

    async def remove_items_from_playlist(
        self,
        _id: str,
        /,
        *,
        uris: Sequence[str],
        snapshot_id: str | None,
    ) -> dict[str, Any]:

        data: dict[str, Any] = {"tracks": [{"uri": uri} for uri in uris]}
        if snapshot_id:
            data["snapshot_id"] = snapshot_id

        return await self.request(Route("DELETE", "/playlists/{id}/tracks", id=_id), data=data)

    async def get_playlist_cover_image(
        self,
        _id: str,
        /,
    ) -> Sequence[dict[str, Any]]:
        return await self.request(Route("GET", "/playlists/{id}/images", id=_id))

    async def upload_playlist_cover_image(
        self
    ) -> ...:
        raise NotImplementedError

    # SEARCH API

    async def search(
        self,
        query: str,
        /,
        *,
        search_types: Sequence[objects.SearchType] | None,
        market: str | None,
        limit: int | None,
        offset: int | None,
        include_external: bool = False
    ) -> dict[str, Any]:

        if not search_types:
            search_types = [objects.SearchType.ALL]

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

    # SHOWS API

    async def get_shows(
        self,
        ids: Sequence[str],
        *,
        market: str | None
    ) -> dict[str, Any]:

        if len(ids) > 50:
            raise ValueError("'get_shows' can only take a maximum of 50 show ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/shows"), parameters=parameters)

    async def get_show(
        self,
        _id: str,
        /,
        *,
        market: str | None
    ) -> dict[str, Any]:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/shows/{id}", id=_id), parameters=parameters)

    async def get_show_episodes(
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

        return await self.request(Route("GET", "/shows/{id}/episodes", id=_id), parameters=parameters)

    # TRACKS API #

    async def get_tracks(
        self,
        ids: Sequence[str],
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

    async def get_several_tracks_audio_features(
        self,
        ids: Sequence[str]
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

    # USERS API

    async def get_current_user_profile(
        self
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/me"))

    async def get_user_profile(
        self,
        _id: str,
        /,
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/users/{id}", id=_id))
