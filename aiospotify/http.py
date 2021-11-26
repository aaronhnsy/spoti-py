# Future
from __future__ import annotations

# Standard Library
import asyncio
import logging
import urllib.parse
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, ClassVar, Literal

# Packages
import aiohttp

# My stuff
from aiospotify import exceptions, objects, utils, values
from aiospotify.typings.http import (
    RelatedArtistsData,
    ArtistTopTracksData,
    AvailableMarketsData,
    CategoryPlaylistsData,
    FeaturedPlaylistsData,
    MultipleAlbumsData,
    MultipleArtistsData,
    MultipleCategoriesData,
    MultipleEpisodesData,
    MultipleShowsData,
    MultipleTracksData,
    NewReleasesData,
    RecommendationGenresData,
    SearchResultData,
    SeveralTracksAudioFeaturesData,
)
from aiospotify.typings.objects import (
    AlbumData,
    ArtistData,
    AudioFeaturesData,
    CategoryData,
    EpisodeData,
    ImageData,
    PagingObjectData,
    PlaylistData,
    RecommendationData,
    ShowData,
    TrackData,
    UserData,
)


if TYPE_CHECKING:

    # My stuff
    from aiospotify.typings import Credentials, OptionalCredentials


__all__ = (
    "Route",
    "HTTPClient"
)

__log__: logging.Logger = logging.getLogger("aiospotify.http")

HTTPMethod = Literal["GET", "POST", "DELETE", "PATCH", "PUT"]


class Route:

    BASE_URL: ClassVar[str] = f"https://api.spotify.com/v1"

    def __init__(
        self,
        method: HTTPMethod,
        path: str,
        /,
        **parameters: Any
    ) -> None:

        self.method: HTTPMethod = method
        self.path: str = path

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
        credentials: OptionalCredentials,
        parameters: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:

        if not self._session:
            self._session = aiohttp.ClientSession()

        if not self._client_credentials:
            self._client_credentials = await objects.ClientCredentials.from_client_secret(self._client_id, self._client_secret, session=self._session)

        _credentials = credentials or self._client_credentials

        if _credentials.is_expired():
            await _credentials.refresh(session=self._session)

        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {_credentials.access_token}"
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
                        __log__.debug(f"{route.method} @ {route.url} received payload: {response_data}")
                        return response_data

                    if response.status == 429:
                        retry_after = float(response.headers["Retry-After"])
                        __log__.warning(f"{route.method} @ {route.url} is being ratelimited, retrying in {retry_after:.2f} seconds.")
                        await asyncio.sleep(retry_after)
                        __log__.debug(f"{route.method} @ {route.url} is done sleeping for ratelimit, retrying...")
                        continue

                    if response.status in {500, 502, 503}:
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    if error := response_data.get("error"):
                        raise values.EXCEPTION_MAPPING[response.status](response, error)

            except OSError as error:
                if tries < 4 and error.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        if response:
            raise exceptions.HTTPError(response, response_data["error"])

        raise RuntimeError("This shouldn't happen.")

    async def close(self) -> None:

        if not self._session:
            return

        await self._session.close()

    # ALBUMS API

    async def get_album(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> AlbumData:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/albums/{id}", id=_id), parameters=parameters, credentials=credentials)

    async def get_albums(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> MultipleAlbumsData:

        if len(ids) > 20:
            raise ValueError("'get_albums' can only take a maximum of 20 album ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/albums"), parameters=parameters, credentials=credentials)

    async def get_album_tracks(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        limit: int | None,
        offset: int | None,
        credentials: OptionalCredentials = None,
    ) -> PagingObjectData:

        parameters = {}
        if market:
            parameters["market"] = market
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/albums/{id}/tracks", id=_id), parameters=parameters, credentials=credentials)

    async def get_saved_albums(self) -> None:
        pass

    async def save_albums(self) -> None:
        pass

    async def remove_albums(self) -> None:
        pass

    async def check_saved_albums(self) -> None:
        pass

    async def get_new_releases(
        self,
        *,
        country: str | None,
        limit: int | None,
        offset: int | None,
        credentials: OptionalCredentials = None,
    ) -> NewReleasesData:

        parameters = {}
        if country:
            parameters["country"] = country
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/browse/new-releases"), parameters=parameters, credentials=credentials)

    # ARTISTS API

    async def get_artist(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> ArtistData:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/artists/{id}", id=_id), parameters=parameters, credentials=credentials)

    async def get_artists(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> MultipleArtistsData:

        if len(ids) > 50:
            raise ValueError("'get_artists' can only take a maximum of 50 artist ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/artists"), parameters=parameters, credentials=credentials)

    async def get_artist_albums(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        include_groups: Sequence[objects.IncludeGroup] | None = utils.MISSING,
        limit: int | None,
        offset: int | None,
        credentials: OptionalCredentials = None,
    ) -> PagingObjectData:

        if include_groups == utils.MISSING:
            include_groups = [objects.IncludeGroup.ALBUM]

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

        return await self.request(Route("GET", "/artists/{id}/albums", id=_id), parameters=parameters, credentials=credentials)

    async def get_artist_top_tracks(
        self,
        _id: str,
        /,
        *,
        market: str = "GB",
        credentials: OptionalCredentials = None,
    ) -> ArtistTopTracksData:

        parameters = {"market": market}
        return await self.request(Route("GET", "/artists/{id}/top-tracks", id=_id), parameters=parameters, credentials=credentials)

    async def get_related_artists(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> RelatedArtistsData:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/artists/{id}/related-artists", id=_id), parameters=parameters, credentials=credentials)

    # SHOWS API

    async def get_show(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> ShowData:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/shows/{id}", id=_id), parameters=parameters, credentials=credentials)

    async def get_shows(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> MultipleShowsData:

        if len(ids) > 50:
            raise ValueError("'get_shows' can only take a maximum of 50 show ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/shows"), parameters=parameters, credentials=credentials)

    async def get_show_episodes(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        limit: int | None,
        offset: int | None,
        credentials: OptionalCredentials = None,
    ) -> PagingObjectData:

        parameters = {}
        if market:
            parameters["market"] = market
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/shows/{id}/episodes", id=_id), parameters=parameters, credentials=credentials)

    async def get_saved_shows(self) -> None:
        pass

    async def save_shows(self) -> None:
        pass

    async def remove_shows(self) -> None:
        pass

    async def check_saved_shows(self) -> None:
        pass

    # EPISODE API

    async def get_episode(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> EpisodeData:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/episodes/{id}", id=_id), parameters=parameters, credentials=credentials)

    async def get_episodes(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> MultipleEpisodesData:

        if len(ids) > 50:
            raise ValueError("'get_episodes' can only take a maximum of 50 episodes ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/episodes"), parameters=parameters, credentials=credentials)

    async def get_saved_episodes(self) -> None:
        pass

    async def save_episodes(self) -> None:
        pass

    async def remove_episodes(self) -> None:
        pass

    async def check_saved_episodes(self) -> None:
        pass

    # TRACKS API

    async def get_track(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> TrackData:

        parameters = {"market": market} if market else None
        return await self.request(Route("GET", "/tracks/{id}", id=_id), parameters=parameters, credentials=credentials)

    async def get_tracks(
        self,
        ids: Sequence[str],
        *,
        market: str | None,
        credentials: OptionalCredentials = None,
    ) -> MultipleTracksData:

        if len(ids) > 50:
            raise ValueError("'get_tracks' can only take a maximum of 50 track ids.")

        parameters = {"ids": ",".join(ids)}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/tracks"), parameters=parameters, credentials=credentials)

    async def get_saved_tracks(self) -> None:
        pass

    async def save_tracks(self) -> None:
        pass

    async def remove_tracks(self) -> None:
        pass

    async def check_saved_tracks(self) -> None:
        pass

    async def get_several_tracks_audio_features(
        self,
        ids: Sequence[str],
        *,
        credentials: OptionalCredentials = None,
    ) -> SeveralTracksAudioFeaturesData:

        if len(ids) > 100:
            raise ValueError("'get_several_track_audio_features' can only take a maximum of 100 track ids.")

        return await self.request(Route("GET", "/audio-features"), parameters={"ids": ",".join(ids)}, credentials=credentials)

    async def get_track_audio_features(
        self,
        _id: str,
        /,
        *,
        credentials: OptionalCredentials = None,
    ) -> AudioFeaturesData:
        return await self.request(Route("GET", "/audio-features/{id}", id=_id), credentials=credentials)

    async def get_track_audio_analysis(
        self,
        _id: str,
        /,
        *,
        credentials: OptionalCredentials = None,
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/audio-analysis/{id}", id=_id), credentials=credentials)

    async def get_recommendations(
        self,
        *,
        seed_artist_ids: Sequence[str] | None,
        seed_genres: Sequence[str] | None,
        seed_track_ids: Sequence[str] | None,
        limit: int | None,
        market: str | None,
        credentials: OptionalCredentials = None,
        **kwargs: int
    ) -> RecommendationData:

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

        return await self.request(Route("GET", "/recommendations"), parameters=parameters, credentials=credentials)

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
        include_external: bool = False,
        credentials: OptionalCredentials = None,
    ) -> SearchResultData:

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

        return await self.request(Route("GET", "/search"), parameters=parameters, credentials=credentials)

    # USERS API

    async def get_current_user_profile(
        self,
        *,
        credentials: Credentials,
    ) -> UserData:
        return await self.request(Route("GET", "/me"), credentials=credentials)

    async def get_current_user_top_artists(
        self,
        *,
        time_range: objects.TimeRange | None,
        limit: int | None,
        offset: int | None,
        credentials: Credentials,
    ) -> PagingObjectData:

        parameters = {}
        if time_range:
            parameters["time_range"] = time_range.value
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/me/top/artists"), parameters=parameters, credentials=credentials)

    async def get_current_user_top_tracks(
        self,
        *,
        time_range: objects.TimeRange | None,
        limit: int | None,
        offset: int | None,
        credentials: Credentials,
    ) -> PagingObjectData:

        parameters = {}
        if time_range:
            parameters["time_range"] = time_range.value
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/me/top/tracks"), parameters=parameters, credentials=credentials)

    async def get_user_profile(
        self,
        _id: str,
        /,
        *,
        credentials: Credentials,
    ) -> UserData:
        return await self.request(Route("GET", "/users/{id}", id=_id), credentials=credentials)

    async def follow_playlist(self) -> None:
        pass

    async def unfollow_playlist(self) -> None:
        pass

    async def get_followed_artists(self) -> None:
        pass

    async def get_followed_users(self) -> None:
        pass

    async def follow_artists(self) -> None:
        pass

    async def follow_users(self) -> None:
        pass

    async def unfollow_artists(self) -> None:
        pass

    async def unfollow_users(self) -> None:
        pass

    async def check_followed_artists(self) -> None:
        pass

    async def check_followed_users(self) -> None:
        pass

    async def check_playlist_followers(self) -> None:
        pass

    # PLAYLISTS API

    async def get_playlist(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        fields: str | None,
        credentials: OptionalCredentials = None,
    ) -> PlaylistData:

        parameters = {"additional_types": "track"}
        if market:
            parameters["market"] = market
        if fields:
            parameters["fields"] = fields

        return await self.request(Route("GET", "/playlists/{id}", id=_id), parameters=parameters, credentials=credentials)

    async def change_playlist_details(
        self,
        _id: str,
        /,
        *,
        name: str | None,
        public: bool | None,
        collaborative: bool | None,
        description: str | None,
        credentials: Credentials,
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

        return await self.request(Route("PUT", "/playlists/{id}", id=_id), data=data, credentials=credentials)

    async def get_playlist_items(
        self,
        _id: str,
        /,
        *,
        market: str | None,
        fields: str | None,
        limit: int | None,
        offset: int | None,
        credentials: OptionalCredentials = None,
    ) -> PagingObjectData:

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

        return await self.request(Route("GET", "/playlists/{id}/tracks", id=_id), parameters=parameters, credentials=credentials)

    async def add_items_to_playlist(
        self,
        _id: str,
        /,
        *,
        position: int | None,
        uris: Sequence[str],
        credentials: Credentials,
    ) -> dict[str, Any]:

        data: dict[str, Any] = {"uris": uris}
        if position:
            data["position"] = position

        return await self.request(Route("POST", "/playlists/{id}/tracks", id=_id), data=data, credentials=credentials)

    async def reorder_playlist_items(
        self,
        _id: str,
        /,
        *,
        range_start: int,
        insert_before: int,
        range_length: int | None,
        snapshot_id: str | None,
        credentials: Credentials,
    ) -> dict[str, Any]:

        data: dict[str, Any] = {
            "range_start": range_start,
            "insert_before": insert_before
        }
        if range_length:
            data["range_length"] = range_length
        if snapshot_id:
            data["snapshot_id"] = snapshot_id

        return await self.request(Route("PUT", "/playlists/{id}/tracks", id=_id), data=data, credentials=credentials)

    async def replace_playlist_items(
        self,
        _id: str,
        /,
        *,
        uris: Sequence[str] | None,
        credentials: Credentials,
    ) -> None:

        data: dict[str, Any] = {"uris": None}
        if uris:
            if len(uris) > 100:
                raise ValueError("'uris' must be less than 100 uris.")
            data["uris"] = uris

        return await self.request(Route("PUT", "/playlists/{id}/tracks", id=_id), data=data, credentials=credentials)

    async def remove_items_from_playlist(
        self,
        _id: str,
        /,
        *,
        uris: Sequence[str],
        snapshot_id: str | None,
        credentials: Credentials,
    ) -> dict[str, Any]:

        data: dict[str, Any] = {"tracks": [{"uri": uri} for uri in uris]}
        if snapshot_id:
            data["snapshot_id"] = snapshot_id

        return await self.request(Route("DELETE", "/playlists/{id}/tracks", id=_id), data=data, credentials=credentials)

    async def get_current_user_playlists(
        self,
        *,
        limit: int | None,
        offset: int | None,
        credentials: Credentials,
    ) -> PagingObjectData:

        parameters = {}
        if limit:
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/me/playlists"), parameters=parameters, credentials=credentials)

    async def get_user_playlists(
        self,
        _id: str,
        /,
        *,
        limit: int | None,
        offset: int | None,
        credentials: Credentials,
    ) -> PagingObjectData:

        parameters = {}
        if limit:
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/users/{id}/playlists", id=_id), parameters=parameters, credentials=credentials)

    async def create_playlist(
        self,
        *,
        user_id: str,
        name: str,
        public: bool | None,
        collaborative: bool | None,
        description: str | None,
        credentials: Credentials,
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

        return await self.request(Route("POST", "/users/{user_id}/playlists", user_id=user_id), data=data, credentials=credentials)

    async def get_featured_playlists(
        self,
        *,
        country: str | None,
        locale: str | None,
        timestamp: str | None,
        limit: int | None,
        offset: int | None,
        credentials: OptionalCredentials = None,
    ) -> FeaturedPlaylistsData:

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

        return await self.request(Route("GET", "/browse/featured-playlists"), parameters=parameters, credentials=credentials)

    async def get_category_playlists(
        self,
        _id: str,
        /,
        *,
        country: str | None,
        limit: int | None,
        offset: int | None,
        credentials: OptionalCredentials = None,
    ) -> CategoryPlaylistsData:

        parameters = {}
        if country:
            parameters["country"] = country
        if limit:
            if limit < 1 or limit > 50:
                raise ValueError("'limit' must be between 1 and 50 inclusive.")
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        return await self.request(Route("GET", "/browse/categories/{id}/playlists", id=_id), parameters=parameters, credentials=credentials)

    async def get_playlist_cover_image(
        self,
        _id: str,
        /,
        *,
        credentials: OptionalCredentials = None,
    ) -> Sequence[ImageData]:
        return await self.request(Route("GET", "/playlists/{id}/images", id=_id), credentials=credentials)

    async def upload_playlist_cover_image(self) -> None:
        pass

    # CATEGORY API

    async def get_categories(
        self,
        *,
        country: str | None,
        locale: str | None,
        limit: int | None,
        offset: int | None,
        credentials: OptionalCredentials = None,
    ) -> MultipleCategoriesData:

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

        return await self.request(Route("GET", "/browse/categories"), parameters=parameters, credentials=credentials)

    async def get_category(
        self,
        _id: str,
        /,
        *,
        country: str | None,
        locale: str | None,
        credentials: OptionalCredentials = None,
    ) -> CategoryData:

        parameters = {}
        if country:
            parameters["country"] = country
        if locale:
            parameters["locale"] = locale

        return await self.request(Route("GET", "/browse/categories/{id}", id=_id), parameters=parameters, credentials=credentials)

    # GENRE API

    async def get_available_genre_seeds(
        self,
        *,
        credentials: OptionalCredentials = None,
    ) -> RecommendationGenresData:
        return await self.request(Route("GET", "/recommendations/available-genre-seeds"), credentials=credentials)

    # PLAYER API

    async def get_playback_state(
        self,
        *,
        market: str | None,
        credentials: Credentials,
    ) -> dict[str, Any]:

        parameters = {"additional_types": "track"}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/me/player"), parameters=parameters, credentials=credentials)

    async def transfer_playback(
        self,
        *,
        device_id: str,
        play: bool | None,
        credentials: Credentials,
    ) -> None:

        data: dict[str, Any] = {"device_ids": [device_id]}
        if play:
            data["play"] = play

        return await self.request(Route("PUT", "/me/player"), data=data, credentials=credentials)

    async def get_available_devices(
        self,
        *,
        credentials: Credentials,
    ) -> dict[str, Any]:
        return await self.request(Route("GET", "/me/player/devices"), credentials=credentials)

    async def get_currently_playing_track(
        self,
        *,
        market: str | None,
        credentials: Credentials,
    ) -> dict[str, Any]:

        parameters = {"additional_types": "track"}
        if market:
            parameters["market"] = market

        return await self.request(Route("GET", "/me/player/currently-playing"), parameters=parameters, credentials=credentials)

    async def start_playback(
        self,
        *,
        credentials: Credentials,
    ) -> None:
        pass

    async def resume_playback(
        self,
        *,
        credentials: Credentials,
    ) -> None:
        await self.start_playback(credentials=credentials)

    async def pause_playback(
        self,
        *,
        device_id: str | None,
        credentials: Credentials,
    ) -> None:

        parameters = {}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/pause"), parameters=parameters, credentials=credentials)

    async def skip_to_next(
        self,
        *,
        device_id: str | None,
        credentials: Credentials,
    ) -> None:

        parameters = {}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("POST", "/me/player/next"), parameters=parameters, credentials=credentials)

    async def skip_to_previous(
        self,
        *,
        device_id: str | None,
        credentials: Credentials,
    ) -> None:

        parameters = {}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("POST", "/me/player/previous"), parameters=parameters, credentials=credentials)

    async def seek_to_position(
        self,
        *,
        position_ms: int,
        device_id: str | None,
        credentials: Credentials,
    ) -> None:

        parameters: dict[str, Any] = {"position_ms": position_ms}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/seek"), parameters=parameters, credentials=credentials)

    async def set_repeat_mode(
        self,
        *,
        repeat_mode: objects.RepeatMode,
        device_id: str | None,
        credentials: Credentials,
    ) -> None:

        parameters = {"state": repeat_mode.value}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/repeat"), parameters=parameters, credentials=credentials)

    async def set_playback_volume(
        self,
        *,
        volume_percent: int,
        device_id: str | None,
        credentials: Credentials,
    ) -> None:

        if volume_percent < 0 or volume_percent > 100:
            raise ValueError("'volume_percent' must between 1 and 100 inclusive.")

        parameters: dict[str, Any] = {"volume_percent": volume_percent}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/volume"), parameters=parameters, credentials=credentials)

    async def toggle_playback_shuffle(
        self,
        *,
        state: bool,
        device_id: str | None,
        credentials: Credentials,
    ) -> None:

        parameters: dict[str, Any] = {"state": state}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("PUT", "/me/player/shuffle"), parameters=parameters, credentials=credentials)

    async def get_recently_played_tracks(
        self,
        *,
        limit: int | None,
        before: int | None,
        after: int | None,
        credentials: Credentials,
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

        return await self.request(Route("GET", "/me/player/recently-played"), parameters=parameters, credentials=credentials)

    async def add_item_to_playback_queue(
        self,
        *,
        uri: str,
        device_id: str | None,
        credentials: Credentials,
    ) -> None:

        parameters = {"uri": uri}
        if device_id:
            parameters["device_id"] = device_id

        return await self.request(Route("POST", "/me/player/queue"), parameters=parameters, credentials=credentials)

    # MARKETS API

    async def get_available_markets(
        self,
        *,
        credentials: OptionalCredentials = None,
    ) -> AvailableMarketsData:
        return await self.request(Route("GET", "/markets"), credentials=credentials)
