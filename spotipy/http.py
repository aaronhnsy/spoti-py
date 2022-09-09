from __future__ import annotations

import asyncio
import base64
from collections.abc import Sequence
from typing import ClassVar, Any
from urllib.parse import quote

import aiohttp

from .exceptions import (
    BadRequest, Unauthorized, Forbidden, NotFound, RequestEntityTooLarge, SpotifyServerError,
    HTTPError, SpotifyException,
)
from .objects import (
    ClientCredentials, UserCredentials, AlbumData, PagingObjectData, ArtistData,
    IncludeGroup, ShowData, EpisodeData, TrackData, AudioFeaturesData, RecommendationData,
    SearchType, SearchResultData, UserData, TimeRange, AlternativePagingObjectData,
    PlaylistData, ImageData, CategoryData, PlaybackStateData, CurrentlyPlayingData,
    RepeatMode, PlaylistSnapshotId,
)
from .types.http import (
    HTTPMethod, Query, Body, Headers, Data, MultipleAlbumsData, NewReleasesData,
    MultipleArtistsData, ArtistTopTracksData, ArtistRelatedArtistsData, MultipleShowsData,
    MultipleEpisodesData, MultipleTracksData, SeveralAudioFeaturesData, FeaturedPlaylistsData,
    CategoryPlaylistsData, MultipleCategoriesData, RecommendationGenresData, MultipleDevicesData,
    AvailableMarketsData,
)
from .utilities import to_json, limit_value, json_or_text
from .values import VALID_SEED_KWARGS


__all__ = (
    "Route",
    "HTTPClient"
)


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
        return f"<spotipy.Route method='{self.method}', url='{self.url}'>"


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

        self._client_credentials: ClientCredentials | None = None

    def __repr__(self) -> str:
        return "<spotipy.HTTPClient>"

    # internal methods

    async def _get_session(self) -> aiohttp.ClientSession:

        if self._session is None:
            self._session = aiohttp.ClientSession()

        return self._session

    async def _get_credentials(
        self,
        _credentials: ClientCredentials | UserCredentials | None, /
    ) -> ClientCredentials | UserCredentials:

        session = await self._get_session()

        if not self._client_credentials:
            self._client_credentials = await ClientCredentials.from_client_secret(
                self._client_id,
                self._client_secret,
                session=session
            )

        credentials = _credentials or self._client_credentials
        if credentials.is_expired():
            await credentials.refresh(session=session)

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
        credentials: ClientCredentials | UserCredentials | None = None,
        query: Query | None = None,
        body: str | None = None,
        json: Body | None = None,
    ) -> Any:

        session = await self._get_session()
        credentials = await self._get_credentials(credentials)

        headers: Headers = {
            "Authorization": f"Bearer {credentials.access_token}"
        }

        if json is not None:
            headers["Content-Type"] = "application/json"
            body = to_json(json)

        response: aiohttp.ClientResponse | None = None
        data: Data | str | None = None

        for tries in range(3):

            try:

                async with session.request(
                        method=route.method,
                        url=route.url,
                        headers=headers,
                        params=query,
                        data=body
                ) as response:

                    data = await json_or_text(response)

                    match response.status:

                        case 200 | 201 | 202 | 204:
                            return data

                        case 400:
                            assert isinstance(data, dict)
                            raise BadRequest(response, data=data)
                        case 401:
                            assert isinstance(data, dict)
                            raise Unauthorized(response, data=data)
                        case 403:
                            assert isinstance(data, dict)
                            raise Forbidden(response, data=data)
                        case 404:
                            assert isinstance(data, dict)
                            raise NotFound(response, data=data)
                        case 413:
                            raise RequestEntityTooLarge(
                                response,
                                data={"error": {"status": 413, "message": "Image was too large."}}
                            )

                        case 429:
                            await asyncio.sleep(float(response.headers["Retry-After"]))
                            continue

                        case 500 | 502 | 503:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        case _:
                            raise SpotifyException()

            except OSError as error:
                if tries < 2 and error.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        if response:

            if response.status >= 500:
                assert isinstance(data, dict)
                raise SpotifyServerError(response, data=data)

            assert isinstance(data, dict)
            raise HTTPError(response, data=data)

        raise RuntimeError("This shouldn't happen.")

    # ALBUMS API

    async def get_album(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> AlbumData:

        query: Query = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/albums/{id}", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_albums(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> MultipleAlbumsData:

        if len(ids) > 20:
            raise ValueError("'ids' can not contain more than 20 ids.")

        query: Query = {"ids": ",".join(ids)}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/albums"),
            query=query,
            credentials=credentials
        )

    async def get_album_tracks(
        self,
        _id: str,
        /, *,
        market: str | None,
        limit: int | None,
        offset: int | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> PagingObjectData:

        query: Query = {}
        if market:
            query["market"] = market
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/albums/{id}/tracks", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_saved_albums(
        self,
        *,
        market: str | None,
        limit: int | None,
        offset: int | None,
        credentials: UserCredentials,
    ) -> PagingObjectData:

        query: Query = {}
        if market:
            query["market"] = market
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/me/albums"),
            query=query,
            credentials=credentials
        )

    async def save_albums(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials,
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/albums"),
            query=query,
            credentials=credentials
        )

    async def remove_albums(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials,
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/albums"),
            query=query,
            credentials=credentials
        )

    async def check_saved_albums(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials,
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/albums/contains"),
            query=query,
            credentials=credentials
        )

    async def get_new_releases(
        self,
        *,
        country: str | None,
        limit: int | None,
        offset: int | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> NewReleasesData:

        query: Query = {}
        if country:
            query["country"] = country
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/browse/new-releases"),
            query=query,
            credentials=credentials
        )

    # ARTISTS API

    async def get_artist(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> ArtistData:

        query: Query = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/artists/{id}", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_artists(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> MultipleArtistsData:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/artists"),
            query=query,
            credentials=credentials
        )

    async def get_artist_albums(
        self,
        _id: str,
        /, *,
        market: str | None,
        limit: int | None,
        offset: int | None,
        include_groups: list[IncludeGroup] | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> PagingObjectData:

        query: Query = {}
        if market:
            query["market"] = market
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if include_groups:
            query["include_groups"] = ",".join(include_group.value for include_group in include_groups)

        return await self.request(
            Route("GET", "/artists/{id}/albums", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_artist_top_tracks(
        self,
        _id: str,
        /, *,
        market: str,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> ArtistTopTracksData:

        query: Query = {
            "market": market
        }
        return await self.request(
            Route("GET", "/artists/{id}/top-tracks", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_related_artists(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> ArtistRelatedArtistsData:

        query: Query = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/artists/{id}/related-artists", id=_id),
            query=query,
            credentials=credentials
        )

    # SHOWS API

    async def get_show(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> ShowData:

        query: Query = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/shows/{id}", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_shows(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> MultipleShowsData:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/shows"),
            query=query,
            credentials=credentials
        )

    async def get_show_episodes(
        self,
        _id: str,
        /, *,
        market: str | None,
        limit: int | None,
        offset: int | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> PagingObjectData:

        query: Query = {}
        if market:
            query["market"] = market
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/shows/{id}/episodes", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_saved_shows(
        self,
        *,
        limit: int | None,
        offset: int | None,
        credentials: UserCredentials,
    ) -> PagingObjectData:

        query: Query = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/me/shows"),
            query=query,
            credentials=credentials
        )

    async def save_shows(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials,
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/shows"),
            query=query,
            credentials=credentials
        )

    async def remove_shows(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials,
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/shows"),
            query=query,
            credentials=credentials
        )

    async def check_saved_shows(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials,
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/shows/contains"),
            query=query,
            credentials=credentials
        )

    # EPISODE API

    async def get_episode(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> EpisodeData:

        query: Query = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/episodes/{id}", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_episodes(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> MultipleEpisodesData:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/episodes"),
            query=query,
            credentials=credentials
        )

    async def get_saved_episodes(
        self,
        *,
        market: str | None,
        limit: int | None,
        offset: int | None,
        credentials: UserCredentials,
    ) -> PagingObjectData:

        query: Query = {}
        if market:
            query["market"] = market
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/me/episodes"),
            query=query,
            credentials=credentials
        )

    async def save_episodes(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/episodes"),
            query=query,
            credentials=credentials
        )

    async def remove_episodes(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/episodes"),
            query=query,
            credentials=credentials
        )

    async def check_saved_episodes(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/episodes/contains"),
            query=query,
            credentials=credentials
        )

    # TRACKS API

    async def get_track(
        self,
        _id: str,
        /, *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> TrackData:

        query: Query = {}
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/tracks/{id}", id=_id),
            query=query,
            credentials=credentials
        )

    async def get_tracks(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> MultipleTracksData:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/tracks"),
            query=query,
            credentials=credentials
        )

    async def get_saved_tracks(
        self,
        *,
        market: str | None,
        limit: int | None,
        offset: int | None,
        credentials: UserCredentials
    ) -> PagingObjectData:

        query: Query = {}
        if market:
            query["market"] = market
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/me/tracks"),
            query=query,
            credentials=credentials
        )

    async def save_tracks(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/tracks"),
            query=query,
            credentials=credentials
        )

    async def remove_tracks(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/tracks"),
            query=query,
            credentials=credentials
        )

    async def check_saved_tracks(
        self,
        ids: list[str],
        /, *,
        credentials: UserCredentials
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/tracks/contains"),
            query=query,
            credentials=credentials
        )

    async def get_track_audio_features(
        self,
        _id: str,
        /, *,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> AudioFeaturesData:
        return await self.request(
            Route("GET", "/audio-features/{id}", id=_id),
            credentials=credentials
        )

    async def get_several_tracks_audio_features(
        self,
        ids: Sequence[str],
        *,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> SeveralAudioFeaturesData:

        if len(ids) > 100:
            raise ValueError("'ids' can not contain more than 100 ids.")

        query: Query = {
            "ids": ",".join(ids)
        }
        return await self.request(
            Route("GET", "/audio-features"),
            query=query,
            credentials=credentials
        )

    async def get_track_audio_analysis(
        self,
        _id: str,
        /, *,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> dict[str, Any]:
        # TODO: create TypedDict for this
        return await self.request(
            Route("GET", "/audio-analysis/{id}", id=_id),
            credentials=credentials
        )

    async def get_recommendations(
        self,
        *,
        seed_artist_ids: list[str] | None,
        seed_genres: list[str] | None,
        seed_track_ids: list[str] | None,
        limit: int | None,
        market: str | None,
        credentials: ClientCredentials | UserCredentials | None = None,
        **kwargs: int
    ) -> RecommendationData:

        seeds = len(
            [seed for seeds in [seed_artist_ids or [], seed_genres or [], seed_track_ids or []] for seed in seeds]
        )
        if seeds < 1 or seeds > 5:
            raise ValueError("too many or no seed values provided. min 1, max 5.")

        query: Query = {}
        if seed_artist_ids:
            query["seed_artists"] = ",".join(seed_artist_ids)
        if seed_genres:
            query["seed_genres"] = ",".join(seed_genres)
        if seed_track_ids:
            query["seed_tracks"] = ",".join(seed_track_ids)

        for key, value in kwargs.items():
            if key not in VALID_SEED_KWARGS:
                raise ValueError(f"'{key}' is not a valid kwarg.")
            query[key] = value

        if limit:
            limit_value("limit", limit, 1, 100)
            query["limit"] = limit
        if market:
            query["market"] = market

        return await self.request(
            Route("GET", "/recommendations"),
            query=query,
            credentials=credentials
        )

    # SEARCH API

    async def search(
        self,
        _query: str,
        /, *,
        search_types: list[SearchType],
        include_external: bool = False,
        market: str | None,
        limit: int | None,
        offset: int | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> SearchResultData:

        query: Query = {
            "q":    _query.replace(" ", "+"),
            "type": ",".join(search_type.value for search_type in search_types)
        }
        if include_external:
            query["include_external"] = "audio"
        if market:
            query["market"] = market
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset

        return await self.request(
            Route("GET", "/search"),
            query=query,
            credentials=credentials
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
    ) -> PagingObjectData:

        query: Query = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if time_range:
            query["time_range"] = time_range.value

        return await self.request(
            Route("GET", "/me/top/artists"),
            query=query,
            credentials=credentials
        )

    async def get_current_user_top_tracks(
        self,
        *,
        limit: int | None,
        offset: int | None,
        time_range: TimeRange | None,
        credentials: UserCredentials
    ) -> PagingObjectData:

        query: Query = {}
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if offset:
            query["offset"] = offset
        if time_range:
            query["time_range"] = time_range.value

        return await self.request(
            Route("GET", "/me/top/tracks"),
            query=query,
            credentials=credentials
        )

    async def get_user_profile(
        self,
        _id: str,
        /, *,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> UserData:
        return await self.request(
            Route("GET", "/users/{id}", id=_id),
            credentials=credentials
        )

    async def follow_playlist(
        self,
        _id: str,
        /, *,
        public: bool | None,
        credentials: UserCredentials
    ) -> None:

        body: Body = {}
        if public:
            body["public"] = public

        return await self.request(
            Route("PUT", "playlists/{id}/followers", id=_id),
            json=body,
            credentials=credentials
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

    async def check_if_users_follow_playlists(
        self,
        playlist_id: str,
        /, *,
        user_ids: list[str],
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> None:

        if len(user_ids) > 5:
            raise ValueError("'ids' can not contain more than 5 ids.")

        query: Query = {
            "ids": ",".join(user_ids)
        }
        return await self.request(
            Route("GET", "/playlists/{playlist_id}/followers/contains", playlist_id=playlist_id),
            query=query,
            credentials=credentials
        )

    async def get_followed_users(
        self,
    ) -> None:
        # TODO: Why is this here.
        raise SpotifyException("This operation is not yet implemented in the spotify api.")

    async def get_followed_artists(
        self,
        *,
        limit: int | None,
        after: str | None,
        credentials: UserCredentials
    ) -> AlternativePagingObjectData:

        query: Query = {
            "type": "artist"
        }
        if limit:
            limit_value("limit", limit, 1, 50)
            query["limit"] = limit
        if after:
            query["after"] = after

        return await self.request(
            Route("GET", "/me/following"),
            query=query,
            credentials=credentials
        )

    async def follow_users(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "type": "user",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/following"),
            query=query,
            credentials=credentials
        )

    async def follow_artists(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "type": "artist",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("PUT", "/me/following"),
            query=query,
            credentials=credentials
        )

    async def unfollow_users(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "type": "user",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/following"),
            query=query,
            credentials=credentials
        )

    async def unfollow_artists(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> None:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "type": "artist",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("DELETE", "/me/following"),
            query=query,
            credentials=credentials
        )

    async def check_followed_users(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "type": "user",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/following/contains"),
            query=query,
            credentials=credentials
        )

    async def check_followed_artists(
        self,
        ids: list[str],
        *,
        credentials: UserCredentials
    ) -> list[bool]:

        if len(ids) > 50:
            raise ValueError("'ids' can not contain more than 50 ids.")

        query: Query = {
            "type": "artist",
            "ids":  ",".join(ids)
        }
        return await self.request(
            Route("GET", "/me/following/contains"),
            query=query,
            credentials=credentials
        )

    # PLAYLISTS API

    async def get_playlist(
        self,
        _id: str,
        /, *,
        market: str | None,
        fields: str | None,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> PlaylistData:

        query: Query = {
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

        body: Body = {}
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
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> PagingObjectData:

        query: Query = {
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
    ) -> PlaylistSnapshotId:

        if len(uris) > 100:
            raise ValueError("'uris' can not contain more than 100 URI's.")

        body: Body = {
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
    ) -> PlaylistSnapshotId:

        body: Body = {
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

        body: Body = {
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
    ) -> PlaylistSnapshotId:

        if len(uris) > 100:
            raise ValueError("'uris' can not contain more than 100 URI's.")

        body: Body = {
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
    ) -> PagingObjectData:

        query: Query = {}
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
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> PagingObjectData:

        query: Query = {}
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

        body: Body = {
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
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> FeaturedPlaylistsData:

        query: Query = {}
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
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> CategoryPlaylistsData:

        query: Query = {}
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
        credentials: ClientCredentials | UserCredentials | None = None
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
                raise SpotifyException("There was a problem while uploading that image.")

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
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> MultipleCategoriesData:

        query: Query = {}
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
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> CategoryData:

        query: Query = {}
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
        credentials: ClientCredentials | UserCredentials | None = None
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

        query: Query = {
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

        body: Body = {
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

        query: Query = {
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

        query: Query = {}
        if device_id:
            query["device_id"] = device_id

        body: Body = {}

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

        query: Query = {}
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

        query: Query = {}
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

        query: Query = {}
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

        query: Query = {
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

        query: Query = {
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

        query: Query = {
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

        query: Query = {
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
    ) -> AlternativePagingObjectData:

        if before and after:
            raise ValueError("'before' and 'after' can not both be specified.")

        query: Query = {}
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

        query: Query = {
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
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> AvailableMarketsData:
        return await self.request(
            Route("GET", "/markets"),
            credentials=credentials
        )
