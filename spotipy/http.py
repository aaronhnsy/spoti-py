from __future__ import annotations

import asyncio
import base64
import logging
from collections.abc import Sequence
from typing import ClassVar, Any, Literal
from urllib.parse import quote

import aiohttp

from .errors import RequestEntityTooLarge, HTTPError, SpotipyError, SpotifyServerError, HTTPErrorMapping
from .objects.album import AlbumData, SimpleAlbumData
from .objects.artist import ArtistData
from .objects.base import PagingObjectData, AlternativePagingObjectData
from .objects.category import CategoryData
from .objects.credentials import ClientCredentials, UserCredentials
from .objects.enums import IncludeGroup, SearchType, TimeRange, RepeatMode
from .objects.episode import EpisodeData
from .objects.image import ImageData
from .objects.playback import PlaybackStateData, CurrentlyPlayingData
from .objects.playlist import PlaylistData, PlaylistSnapshotID, SimplePlaylistData
from .objects.recommendation import RecommendationsData
from .objects.search import SearchResultData
from .objects.show import ShowData
from .objects.track import SimpleTrackData, TrackData, AudioFeaturesData, PlaylistTrackData
from .objects.user import UserData
from .types.common import AnyCredentials
from .types.http import (
    HTTPMethod, Headers,
    FeaturedPlaylistsData, CategoryPlaylistsData,
    MultipleCategoriesData, RecommendationGenresData, MultipleDevicesData, AvailableMarketsData,
)
from .utilities import to_json, limit_value, json_or_text
from .values import VALID_RECOMMENDATION_SEED_KWARGS


__all__ = (
    "Route",
    "HTTPClient"
)

LOG: logging.Logger = logging.getLogger("spotipy.http")


class Route:

    BASE: ClassVar[str] = "https://api.spotify.com/v1"

    def __init__(
        self,
        method: HTTPMethod,
        path: str,
        /,
        **parameters: Any
    ) -> None:

        self.method: HTTPMethod = method
        self.path: str = path
        self.parameters: dict[str, Any] = parameters

        url = self.BASE + path
        if parameters:
            url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})

        self.url: str = url

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: method='{self.method}', url='{self.url}'>"


class HTTPClient:

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        session: aiohttp.ClientSession | None = None,
    ) -> None:

        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._session: aiohttp.ClientSession | None = session

        self._credentials: ClientCredentials | None = None

        self._request_lock: asyncio.Event = asyncio.Event()
        self._request_lock.set()

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}>"

    # internal methods

    async def _get_session(self) -> aiohttp.ClientSession:

        if self._session is None:
            self._session = aiohttp.ClientSession()

        return self._session

    async def _get_credentials(self, credentials: AnyCredentials | None) -> AnyCredentials:

        session = await self._get_session()

        if not self._credentials:
            self._credentials = await ClientCredentials.from_client_details(
                self._client_id, self._client_secret,
                session=session
            )

        credentials = credentials or self._credentials
        if credentials.is_expired():
            await credentials.refresh(session)

        return credentials

    # public methods

    async def close(self) -> None:

        if self._session is None:
            return

        await self._session.close()

    async def request(
        self,
        route: Route,
        /, *,
        credentials: AnyCredentials | None = None,
        query: dict[str, Any] | None = None,
        body: str | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:

        session = await self._get_session()
        credentials = await self._get_credentials(credentials)

        headers: Headers = {
            "Authorization": f"Bearer {credentials.access_token}"
        }
        if json is not None:
            headers["Content-Type"] = "application/json"
            body = to_json(json)

        if self._request_lock.is_set() is False:
            await self._request_lock.wait()

        response: aiohttp.ClientResponse | None = None
        data: dict[str, Any] | str | None = None

        for tries in range(4):
            try:
                async with session.request(
                        route.method, route.url, headers=headers, params=query, data=body
                ) as response:

                    status = response.status
                    LOG.debug(f"'{route.method}' @ '{response.url}' -> '{status}'.")

                    data = await json_or_text(response)

                    if 200 <= status < 300:
                        return data

                    if status in {400, 401, 403, 404}:
                        raise HTTPErrorMapping[status](response, data)  # type: ignore

                    elif status == 413:
                        # special case handler for playlist image uploads.
                        raise RequestEntityTooLarge(
                            response,
                            data={"error": {"status": 413, "message": "Playlist image was too large."}}
                        )

                    elif status == 429:
                        # sleep for 'Retry-After' seconds before making new requests.
                        self._request_lock.clear()
                        await asyncio.sleep(int(response.headers["Retry-After"]))
                        self._request_lock.set()
                        continue

                    elif status in {500, 502, 503}:
                        # retry request for specific 5xx status codes.
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    elif status >= 500:
                        # raise an exception for any other 5xx status code.
                        raise SpotifyServerError(response, data)  # type: ignore

                    raise HTTPError(response, data)  # type: ignore

            except OSError as error:
                # retry request for the 'connection reset by peer' error.
                if tries < 3 and error.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        if response is not None:
            # raise an exception when we run out of retries.
            if response.status >= 500:
                raise SpotifyServerError(response, data)  # type: ignore
            raise HTTPError(response, data)  # type: ignore

        raise RuntimeError("This shouldn't happen.")

    # ALBUMS API

    async def get_album(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> AlbumData:

        query: dict[str, Any] = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/albums/{id}", id=_id),
            query=query, credentials=credentials
        )

    async def get_multiple_albums(
        self,
        ids: Sequence[str],
        /, *,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["albums"], list[AlbumData | None]]:

        if len(ids) > 20:
            raise ValueError("'ids' can not contain more than 20 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/albums"),
            query=query, credentials=credentials
        )

    async def get_album_tracks(
        self,
        _id: str,
        /, *,
        limit: int | None,
        offset: int | None,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> PagingObjectData[SimpleTrackData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/albums/{id}/tracks", id=_id),
            query=query, credentials=credentials
        )

    async def get_saved_albums(
        self,
        *,
        limit: int | None,
        offset: int | None,
        market: str | None,
        credentials: UserCredentials,
    ) -> PagingObjectData[AlbumData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/me/albums"),
            query=query, credentials=credentials
        )

    async def save_albums(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials,
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/albums"),
            query=query, credentials=credentials
        )

    async def remove_albums(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials,
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/albums"),
            query=query, credentials=credentials
        )

    async def check_saved_albums(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials,
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/albums/contains"),
            query=query, credentials=credentials
        )

    async def get_new_releases(
        self,
        *,
        country: str | None,
        limit: int | None,
        offset: int | None,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["albums"], PagingObjectData[SimpleAlbumData]]:

        query: dict[str, Any] = {}
        if country:
            query["country"] = country
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/browse/new-releases"),
            query=query, credentials=credentials
        )

    # ARTISTS API

    async def get_artist(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> ArtistData:

        query: dict[str, Any] = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/artists/{id}", id=_id),
            query=query, credentials=credentials
        )

    async def get_multiple_artists(
        self,
        ids: Sequence[str],
        /, *,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["artists"], list[ArtistData | None]]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/artists"),
            query=query, credentials=credentials
        )

    async def get_artist_albums(
        self,
        _id: str,
        /, *,
        include_groups: list[IncludeGroup] | None,
        limit: int | None,
        offset: int | None,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> PagingObjectData[SimpleAlbumData]:

        query: dict[str, Any] = {}
        if include_groups:
            query["include_groups"] = ",".join(include_group.value for include_group in include_groups)
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/artists/{id}/albums", id=_id),
            query=query, credentials=credentials
        )

    async def get_artist_top_tracks(
        self,
        _id: str,
        /, *,
        market: str,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["tracks"], list[TrackData]]:

        query: dict[str, Any] = {
            "market": market
        }
        return await self.request(
            Route("GET", "/artists/{id}/top-tracks", id=_id),
            query=query, credentials=credentials
        )

    async def get_related_artists(
        self,
        _id: str,
        /, *,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["artists"], list[ArtistData]]:
        return await self.request(
            Route("GET", "/artists/{id}/related-artists", id=_id),
            credentials=credentials
        )

    # SHOWS API

    async def get_show(
        self,
        _id: str,
        /, *,
        market: str,
        credentials: AnyCredentials | None = None
    ) -> ShowData:

        query: dict[str, Any] = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/shows/{id}", id=_id),
            query=query, credentials=credentials
        )

    async def get_multiple_shows(
        self,
        ids: Sequence[str],
        /, *,
        market: str,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["shows"], list[ShowData | None]]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/shows"),
            query=query, credentials=credentials
        )

    async def get_show_episodes(
        self,
        _id: str,
        /, *,
        limit: int | None,
        offset: int | None,
        market: str,
        credentials: AnyCredentials | None = None
    ) -> PagingObjectData[EpisodeData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/shows/{id}/episodes", id=_id),
            query=query, credentials=credentials
        )

    async def get_saved_shows(
        self,
        *,
        limit: int | None,
        offset: int | None,
        credentials: UserCredentials,
    ) -> PagingObjectData[ShowData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/me/shows"),
            query=query, credentials=credentials
        )

    async def save_shows(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials,
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/shows"),
            query=query, credentials=credentials
        )

    async def remove_shows(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials,
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/shows"),
            query=query, credentials=credentials
        )

    async def check_saved_shows(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials,
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/shows/contains"),
            query=query, credentials=credentials
        )

    # EPISODE API

    async def get_episode(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> EpisodeData:

        query: dict[str, Any] = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/episodes/{id}", id=_id),
            query=query, credentials=credentials
        )

    async def get_multiple_episodes(
        self,
        ids: Sequence[str],
        /, *,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["episodes"], list[EpisodeData | None]]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/episodes"),
            query=query, credentials=credentials
        )

    async def get_saved_episodes(
        self,
        *,
        limit: int | None,
        offset: int | None,
        market: str | None,
        credentials: UserCredentials,
    ) -> PagingObjectData[EpisodeData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/me/episodes"),
            query=query, credentials=credentials
        )

    async def save_episodes(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/episodes"),
            query=query, credentials=credentials
        )

    async def remove_episodes(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/episodes"),
            query=query, credentials=credentials
        )

    async def check_saved_episodes(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/episodes/contains"),
            query=query, credentials=credentials
        )

    # TRACKS API

    async def get_track(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> TrackData:

        query: dict[str, Any] = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/tracks/{id}", id=_id),
            query=query, credentials=credentials
        )

    async def get_multiple_tracks(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["tracks"], list[TrackData | None]]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/tracks"),
            query=query, credentials=credentials
        )

    async def get_saved_tracks(
        self,
        *,
        limit: int | None,
        offset: int | None,
        market: str | None,
        credentials: UserCredentials
    ) -> PagingObjectData[TrackData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/me/tracks"),
            query=query, credentials=credentials
        )

    async def save_tracks(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/tracks"),
            query=query, credentials=credentials
        )

    async def remove_tracks(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/tracks"),
            query=query, credentials=credentials
        )

    async def check_saved_tracks(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/tracks/contains"),
            query=query, credentials=credentials
        )

    async def get_track_audio_features(
        self,
        _id: str,
        /, *,
        credentials: AnyCredentials | None = None
    ) -> AudioFeaturesData:
        return await self.request(
            Route("GET", "/audio-features/{id}", id=_id),
            credentials=credentials
        )

    async def get_multiple_tracks_audio_features(
        self,
        ids: Sequence[str],
        /, *,
        credentials: AnyCredentials | None = None
    ) -> dict[Literal["audio_features"], list[AudioFeaturesData | None]]:

        if len(ids) > 100:
            raise ValueError("'ids' can not contain more than 100 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/audio-features"),
            query=query, credentials=credentials
        )

    async def get_track_audio_analysis(
        self,
        _id: str,
        /, *,
        credentials: AnyCredentials | None = None
    ) -> dict[str, Any]:  # TODO: create TypedDict for this monstrosity
        return await self.request(
            Route("GET", "/audio-analysis/{id}", id=_id),
            credentials=credentials
        )

    async def get_recommendations(
        self,
        *,
        seed_artist_ids: list[str] | None,
        seed_track_ids: list[str] | None,
        seed_genres: list[str] | None,
        limit: int | None,
        market: str | None,
        credentials: AnyCredentials | None = None,
        **kwargs: int
    ) -> RecommendationsData:

        count = len(seed_artist_ids or []) + len(seed_track_ids or []) + len(seed_genres or [])
        if count < 1 or count > 5:
            raise ValueError("too many or not enough seed values provided. minimum 1, maximum 5.")

        query: dict[str, Any] = {}
        if seed_artist_ids:
            query["seed_artists"] = ",".join(seed_artist_ids)
        if seed_track_ids:
            query["seed_tracks"] = ",".join(seed_track_ids)
        if seed_genres:
            query["seed_genres"] = ",".join(seed_genres)

        for key, value in kwargs.items():
            if key not in VALID_RECOMMENDATION_SEED_KWARGS:
                raise ValueError(f"'{key}' is not a valid keyword argument for this method.")
            query[key] = value

        if limit:
            limit_value("limit", limit, 1, 100)
            query["limit"] = limit
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/recommendations"),
            query=query, credentials=credentials
        )

    # SEARCH API

    async def search(
        self,
        _query: str,
        /, *,
        search_types: list[SearchType],
        include_external: bool,
        limit: int | None,
        offset: int | None,
        market: str | None,
        credentials: AnyCredentials | None = None
    ) -> SearchResultData:

        query: dict[str, Any] = {
            "q":    _query.replace(" ", "+"),
            "type": ",".join(search_type.value for search_type in search_types)
        }
        if include_external:
            query["include_external"] = "audio"
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/search"),
            query=query, credentials=credentials
        )

    # USERS API

    async def get_current_user_profile(
        self,
        *,
        credentials: UserCredentials
    ) -> UserData:
        return await self.request(
            Route("GET", "/me"),
            credentials=credentials
        )

    async def get_current_user_top_artists(
        self,
        *,
        limit: int | None,
        offset: int | None,
        time_range: TimeRange | None,
        credentials: UserCredentials
    ) -> PagingObjectData[ArtistData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if time_range:
            query["time_range"] = time_range.value

        return await self.request(
            Route("GET", "/me/top/artists"),
            query=query, credentials=credentials
        )

    async def get_current_user_top_tracks(
        self,
        *,
        limit: int | None,
        offset: int | None,
        time_range: TimeRange | None,
        credentials: UserCredentials
    ) -> PagingObjectData[TrackData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if time_range:
            query["time_range"] = time_range.value

        return await self.request(
            Route("GET", "/me/top/tracks"),
            query=query, credentials=credentials
        )

    async def get_user_profile(
        self,
        _id: str,
        /, *,
        credentials: AnyCredentials | None = None
    ) -> UserData:
        return await self.request(
            Route("GET", "/users/{id}", id=_id),
            credentials=credentials
        )

    async def follow_playlist(
        self,
        _id: str,
        /, *,
        public: bool,
        credentials: UserCredentials
    ) -> None:

        body: dict[str, Any] = {}
        if public:
            body["public"] = public

        return await self.request(
            Route("PUT", "playlists/{id}/followers", id=_id),
            json=body, credentials=credentials
        )

    async def unfollow_playlist(
        self,
        _id: str,
        /, *,
        credentials: UserCredentials
    ) -> None:
        return await self.request(
            Route("DELETE", "playlists/{id}/followers", id=_id),
            credentials=credentials
        )

    async def check_if_users_follow_playlist(
        self,
        _id: str,
        /, *,
        user_ids: list[str],
        credentials: AnyCredentials | None = None
    ) -> None:

        if len(user_ids) > 5:
            raise ValueError("'user_ids' can not contain more than 5 ids.")

        query: dict[str, Any] = {
            "ids": ",".join(user_ids)
        }
        return await self.request(
            Route("GET", "/playlists/{id}/followers/contains", id=_id),
            query=query, credentials=credentials
        )

    async def get_followed_artists(
        self,
        *,
        limit: int | None,
        after: str | None,
        credentials: UserCredentials
    ) -> AlternativePagingObjectData[ArtistData]:

        query: dict[str, Any] = {
            "type": "artist"
        }
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if after:
            query["after"] = after

        return await self.request(
            Route("GET", "/me/following"),
            query=query, credentials=credentials
        )

    async def follow_artists(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "type": "artist",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/following"),
            query=query, credentials=credentials
        )

    async def unfollow_artists(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "type": "artist",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/following"),
            query=query, credentials=credentials
        )

    async def check_followed_artists(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "type": "artist",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/following/contains"),
            query=query, credentials=credentials
        )

    async def follow_users(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "type": "user",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/following"),
            query=query, credentials=credentials
        )

    async def unfollow_users(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "type": "user",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/following"),
            query=query, credentials=credentials
        )

    async def check_followed_users(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: dict[str, Any] = {
            "type": "user",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/following/contains"),
            query=query, credentials=credentials
        )

    # PLAYLISTS API
    # TODO: Check through docs to make sure every parameter is accounted for

    async def get_playlist(
        self,
        _id: str,
        /, *,
        market: str | None,
        fields: str | None,
        credentials: AnyCredentials | None = None
    ) -> PlaylistData:

        query: dict[str, Any] = {
            "additional_types": "track"
        }
        # TODO: Support all additional types
        if market:
            query["market"] = market
        if fields:
            query["fields"] = fields

        return await self.request(
            Route("GET", "/playlists/{id}", id=_id),
            query=query,
            credentials=credentials
        )

    async def change_playlist_details(
        self,
        _id: str,
        /, *,
        name: str | None,
        public: bool | None,
        collaborative: bool | None,
        description: str | None,
        credentials: UserCredentials
    ) -> None:

        if collaborative and public:
            raise ValueError("collaborative playlists can not be public.")

        body: dict[str, Any] = {}
        if name:
            body["name"] = name
        if public:
            body["public"] = public
        if collaborative:
            body["collaborative"] = collaborative
        if description:
            body["description"] = description

        return await self.request(
            Route("PUT", "/playlists/{id}", id=_id),
            json=body,
            credentials=credentials
        )

    async def get_playlist_items(
        self,
        _id: str,
        /, *,
        market: str | None,
        fields: str | None,
        limit: int | None,
        offset: int | None,
        credentials: AnyCredentials | None = None
    ) -> PagingObjectData[PlaylistTrackData]:

        query: dict[str, Any] = {
            "additional_types": "track"
        }
        # TODO: Support all additional types
        if market:
            query["market"] = market
        if fields:
            query["fields"] = fields
        if limit:
            limit_value("limit", limit, 1, 100)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/playlists/{id}/tracks", id=_id),
            query=query,
            credentials=credentials
        )

    async def add_items_to_playlist(
        self,
        _id: str,
        /, *,
        uris: list[str],
        position: int | None,
        credentials: UserCredentials
    ) -> PlaylistSnapshotID:

        if len(uris) > 100:
            raise ValueError("'uris' can not contain more than 100 URI's.")

        body: dict[str, Any] = {
            "uris": uris
        }
        if position:
            body["position"] = position

        return await self.request(
            Route("POST", "/playlists/{id}/tracks", id=_id),
            json=body,
            credentials=credentials
        )

    async def reorder_playlist_items(
        self,
        _id: str,
        /, *,
        range_start: int,
        insert_before: int,
        range_length: int | None,
        snapshot_id: str | None,
        credentials: UserCredentials
    ) -> PlaylistSnapshotID:

        body: dict[str, Any] = {
            "range_start":   range_start,
            "insert_before": insert_before
        }
        if range_length:
            body["range_length"] = range_length
        if snapshot_id:
            body["snapshot_id"] = snapshot_id

        return await self.request(
            Route("PUT", "/playlists/{id}/tracks", id=_id),
            json=body,
            credentials=credentials
        )

    async def replace_playlist_items(
        self,
        _id: str,
        /, *,
        uris: list[str],
        credentials: UserCredentials
    ) -> None:

        if len(uris) > 100:
            raise ValueError("'uris' can not contain more than 100 URI's.")

        body: dict[str, Any] = {
            "uris": uris
        }
        return await self.request(
            Route("PUT", "/playlists/{id}/tracks", id=_id),
            json=body,
            credentials=credentials
        )

    async def remove_items_from_playlist(
        self,
        _id: str,
        /, *,
        uris: list[str],
        snapshot_id: str | None,
        credentials: UserCredentials
    ) -> PlaylistSnapshotID:

        if len(uris) > 100:
            raise ValueError("'uris' can not contain more than 100 URI's.")

        body: dict[str, Any] = {
            "tracks": [{"uri": uri} for uri in uris]
        }
        if snapshot_id:
            body["snapshot_id"] = snapshot_id

        return await self.request(
            Route("DELETE", "/playlists/{id}/tracks", id=_id),
            json=body,
            credentials=credentials
        )

    async def get_current_user_playlists(
        self,
        *,
        limit: int | None,
        offset: int | None,
        credentials: UserCredentials
    ) -> PagingObjectData[SimplePlaylistData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/me/playlists"),
            query=query,
            credentials=credentials
        )

    async def get_user_playlists(
        self,
        _id: str,
        /, *,
        limit: int | None,
        offset: int | None,
        credentials: AnyCredentials | None = None
    ) -> PagingObjectData[SimplePlaylistData]:

        query: dict[str, Any] = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/users/{id}/playlists", id=_id),
            query=query,
            credentials=credentials
        )

    async def create_playlist(
        self,
        *,
        user_id: str,
        name: str,
        public: bool | None,
        collaborative: bool | None,
        description: str | None,
        credentials: UserCredentials
    ) -> PlaylistData:

        if collaborative and public:
            raise ValueError("collaborative playlists can not be public.")

        body: dict[str, Any] = {
            "name": name
        }
        if public:
            body["public"] = public
        if collaborative:
            body["collaborative"] = collaborative
        if description:
            body["description"] = description

        return await self.request(
            Route("POST", "/users/{user_id}/playlists", user_id=user_id),
            json=body,
            credentials=credentials
        )

    async def get_featured_playlists(
        self,
        *,
        country: str | None,
        locale: str | None,
        timestamp: str | None,
        limit: int | None,
        offset: int | None,
        credentials: AnyCredentials | None = None
    ) -> FeaturedPlaylistsData:

        query: dict[str, Any] = {}
        if country:
            query["country"] = country
        if locale:
            query["locale"] = locale
        if timestamp:
            query["timestamp"] = timestamp
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/browse/featured-playlists"),
            query=query,
            credentials=credentials
        )

    async def get_category_playlists(
        self,
        _id: str,
        /, *,
        country: str | None,
        limit: int | None,
        offset: int | None,
        credentials: AnyCredentials | None = None
    ) -> CategoryPlaylistsData:

        query: dict[str, Any] = {}
        if country:
            query["country"] = country
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/browse/categories/{id}/playlists", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_playlist_cover_image(
        self,
        _id: str,
        /, *,
        credentials: AnyCredentials | None = None
    ) -> list[ImageData]:
        return await self.request(
            Route("GET", "/playlists/{id}/images", id=_id),
            credentials=credentials
        )

    async def upload_playlist_cover_image(
        self,
        _id: str,
        /, *,
        url: str,
        credentials: UserCredentials
    ) -> None:

        session = await self._get_session()
        async with session.get(url) as request:

            if request.status != 200:
                raise SpotipyError("There was a problem while uploading that image.")

            image_bytes = await request.read()
            body = base64.b64encode(image_bytes).decode("utf-8")

        return await self.request(
            Route("PUT", "/playlists/{id}/images", id=_id),
            body=body,
            credentials=credentials
        )

    # CATEGORY API

    async def get_categories(
        self,
        *,
        country: str | None,
        locale: str | None,
        limit: int | None,
        offset: int | None,
        credentials: AnyCredentials | None = None
    ) -> MultipleCategoriesData:

        query: dict[str, Any] = {}
        if country:
            query["country"] = country
        if locale:
            query["locale"] = locale
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/browse/categories"),
            query=query,
            credentials=credentials
        )

    async def get_category(
        self,
        _id: str,
        /, *,
        country: str | None,
        locale: str | None,
        credentials: AnyCredentials | None = None
    ) -> CategoryData:

        query: dict[str, Any] = {}
        if country:
            query["country"] = country
        if locale:
            query["locale"] = locale

        return await self.request(
            Route("GET", "/browse/categories/{id}", id=_id),
            query=query,
            credentials=credentials
        )

    # GENRE API

    async def get_available_genre_seeds(
        self,
        *,
        credentials: AnyCredentials | None = None
    ) -> RecommendationGenresData:
        return await self.request(
            Route("GET", "/recommendations/available-genre-seeds"),
            credentials=credentials
        )

    # PLAYER API

    async def get_playback_state(
        self,
        *,
        market: str | None,
        credentials: UserCredentials
    ) -> PlaybackStateData:

        query: dict[str, Any] = {
            "additional_types": "track"
        }
        # TODO: Support all additional types
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/me/player"),
            query=query,
            credentials=credentials
        )

    async def transfer_playback(
        self,
        *,
        device_id: str,
        ensure_playback: bool | None,
        credentials: UserCredentials
    ) -> None:

        body: dict[str, Any] = {
            "device_ids": [device_id]
        }
        if ensure_playback:
            body["play"] = ensure_playback

        return await self.request(
            Route("PUT", "/me/player"),
            json=body,
            credentials=credentials
        )

    async def get_available_devices(
        self,
        *,
        credentials: UserCredentials
    ) -> MultipleDevicesData:
        return await self.request(
            Route("GET", "/me/player/devices"),
            credentials=credentials
        )

    async def get_currently_playing_track(
        self,
        *,
        market: str | None,
        credentials: UserCredentials
    ) -> CurrentlyPlayingData:

        query: dict[str, Any] = {
            "additional_types": "track"
        }
        # TODO: Support all additional types
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/me/player/currently-playing"),
            query=query,
            credentials=credentials
        )

    async def start_playback(
        self,
        *,
        device_id: str | None,
        context_uri: str | None,
        uris: list[str] | None,
        offset: int | str | None,
        position_ms: int | None,
        credentials: UserCredentials
    ) -> None:

        if context_uri and uris:
            raise ValueError("'context_uri' and 'uris' can not both be specified.")

        query: dict[str, Any] = {}
        if device_id:
            query["device_id"] = device_id

        body: dict[str, Any] = {}

        if context_uri or uris:
            if context_uri:
                body["context_uri"] = context_uri
            if uris:
                body["uris"] = uris
            if offset:
                body["offset"] = {}
                if isinstance(offset, int):
                    body["offset"]["position"] = offset
                else:
                    body["offset"]["uri"] = offset
            if position_ms:
                body["position_ms"] = position_ms

        return await self.request(
            Route("PUT", "/me/player/play"),
            query=query,
            json=body,
            credentials=credentials
        )

    async def resume_playback(
        self,
        *,
        device_id: str | None,
        offset: int | str | None,
        position_ms: int | None,
        credentials: UserCredentials
    ) -> None:

        # TODO: wtf is happening here

        return await self.start_playback(
            device_id=device_id,
            context_uri=None,
            uris=None,
            offset=offset,
            position_ms=position_ms,
            credentials=credentials
        )

    async def pause_playback(
        self,
        *,
        device_id: str | None,
        credentials: UserCredentials
    ) -> None:

        query: dict[str, Any] = {}
        if device_id:
            query["device_id"] = device_id

        return await self.request(
            Route("PUT", "/me/player/pause"),
            query=query,
            credentials=credentials
        )

    async def skip_to_next(
        self,
        *,
        device_id: str | None,
        credentials: UserCredentials
    ) -> None:

        query: dict[str, Any] = {}
        if device_id:
            query["device_id"] = device_id

        return await self.request(
            Route("POST", "/me/player/next"),
            query=query,
            credentials=credentials
        )

    async def skip_to_previous(
        self,
        *,
        device_id: str | None,
        credentials: UserCredentials
    ) -> None:

        query: dict[str, Any] = {}
        if device_id:
            query["device_id"] = device_id

        return await self.request(
            Route("POST", "/me/player/previous"),
            query=query,
            credentials=credentials
        )

    async def seek_to_position(
        self,
        *,
        position_ms: int,
        device_id: str | None,
        credentials: UserCredentials
    ) -> None:

        query: dict[str, Any] = {
            "position_ms": position_ms
        }
        if device_id:
            query["device_id"] = device_id

        return await self.request(
            Route("PUT", "/me/player/seek"),
            query=query,
            credentials=credentials
        )

    async def set_repeat_mode(
        self,
        *,
        repeat_mode: RepeatMode,
        device_id: str | None,
        credentials: UserCredentials
    ) -> None:

        query: dict[str, Any] = {
            "state": repeat_mode.value
        }
        if device_id:
            query["device_id"] = device_id

        return await self.request(
            Route("PUT", "/me/player/repeat"),
            query=query,
            credentials=credentials
        )

    async def set_playback_volume(
        self,
        *,
        volume_percent: int,
        device_id: str | None,
        credentials: UserCredentials
    ) -> None:

        limit_value("volume_percent", volume_percent, 0, 100)

        query: dict[str, Any] = {
            "volume_percent": volume_percent
        }
        if device_id:
            query["device_id"] = device_id

        return await self.request(
            Route("PUT", "/me/player/volume"),
            query=query,
            credentials=credentials
        )

    async def toggle_playback_shuffle(
        self,
        *,
        state: bool,
        device_id: str | None,
        credentials: UserCredentials
    ) -> None:

        query: dict[str, Any] = {
            "state": "true" if state else "false"
        }
        if device_id:
            query["device_id"] = device_id

        return await self.request(
            Route("PUT", "/me/player/shuffle"),
            query=query,
            credentials=credentials
        )

    async def get_recently_played_tracks(
        self,
        *,
        limit: int | None,
        before: int | None,
        after: int | None,
        credentials: UserCredentials
    ) -> AlternativePagingObjectData[SimpleTrackData]:

        if before and after:
            raise ValueError("'before' and 'after' can not both be specified.")

        query: dict[str, Any] = {}
        if limit:
            query["limit"] = limit
        if before:
            query["before"] = before
        if after:
            query["after"] = after

        return await self.request(
            Route("GET", "/me/player/recently-played"),
            query=query,
            credentials=credentials
        )

    async def add_item_to_playback_queue(
        self,
        *,
        uri: str,
        device_id: str | None,
        credentials: UserCredentials
    ) -> None:

        query: dict[str, Any] = {
            "uri": uri
        }
        if device_id:
            query["device_id"] = device_id

        return await self.request(
            Route("POST", "/me/player/queue"),
            query=query,
            credentials=credentials
        )

    # MARKETS API

    async def get_available_markets(
        self,
        *,
        credentials: AnyCredentials | None = None
    ) -> AvailableMarketsData:
        return await self.request(
            Route("GET", "/markets"),
            credentials=credentials
        )
