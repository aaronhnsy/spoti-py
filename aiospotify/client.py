# Future
from __future__ import annotations

# Standard Library
import math
from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

# Packages
import aiohttp

# My stuff
from aiospotify import http, objects, utils


if TYPE_CHECKING:

    # My stuff
    from aiospotify.typings import Credentials, OptionalCredentials


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

        self.http: http.HTTPClient = http.HTTPClient(client_id=self._client_id, client_secret=self._client_secret, session=self._session)

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
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> dict[ID, objects.Album | None]:

        response = await self.http.get_albums(ids=ids, market=market, credentials=credentials)
        return dict(zip(ids, [objects.Album(data) if data else None for data in response["albums"]]))

    async def get_album(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> objects.Album:

        response = await self.http.get_album(_id, market=market, credentials=credentials)
        return objects.Album(response)

    async def get_album_tracks(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.SimpleTrack]:

        response = await self.http.get_album_tracks(_id, market=market, limit=limit, offset=offset, credentials=credentials)
        return [objects.SimpleTrack(data) for data in objects.PagingObject(response).items]

    async def get_all_album_tracks(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.SimpleTrack]:

        response = await self.http.get_album_tracks(_id, market=market, limit=50, offset=0, credentials=credentials)
        paging = objects.PagingObject(response)

        tracks = [objects.SimpleTrack(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or fewer tracks, and we already have them so just return them
            return tracks

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_album_tracks(_id, market=market, limit=50, offset=_ * 50, credentials=credentials)
            tracks.extend([objects.SimpleTrack(data) for data in objects.PagingObject(response).items])

        return tracks

    async def get_full_album(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> objects.Album:

        album = await self.get_album(_id, market=market, credentials=credentials)

        if album._tracks_paging.total <= 50:  # The album has 50 or fewer tracks already, so we can just return it now.
            return album

        for _ in range(2, math.ceil(album._tracks_paging.total / 50)):
            response = await self.http.get_album_tracks(_id, market=market, limit=50, offset=_ * 50, credentials=credentials)
            album.tracks.extend([objects.SimpleTrack(data) for data in objects.PagingObject(response).items])

        return album

    # ARTISTS API

    async def get_artists(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> dict[ID, objects.Artist | None]:

        response = await self.http.get_artists(ids=ids, market=market, credentials=credentials)
        return dict(zip(ids, [objects.Artist(data) if data else None for data in response["artists"]]))

    async def get_artist(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> objects.Artist:

        response = await self.http.get_artist(_id, market=market, credentials=credentials)
        return objects.Artist(response)

    async def get_artist_top_tracks(
        self,
        _id: str,
        /,
        *,
        market: str = "GB",
        credentials: OptionalCredentials = None,
    ) -> list[objects.Track]:

        response = await self.http.get_artist_top_tracks(_id, market=market, credentials=credentials)
        return [objects.Track(data) for data in response["tracks"]]

    async def get_related_artists(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.Artist]:

        response = await self.http.get_related_artists(_id, market=market, credentials=credentials)
        return [objects.Artist(data) for data in response["artists"]]

    async def get_artist_albums(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        include_groups: Sequence[objects.IncludeGroup] | None = utils.MISSING,
        limit: int | None = None,
        offset: int | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.SimpleAlbum]:

        if include_groups == utils.MISSING:
            include_groups = [objects.IncludeGroup.ALBUM]

        response = await self.http.get_artist_albums(_id, market=market, include_groups=include_groups, limit=limit, offset=offset, credentials=credentials)
        return [objects.SimpleAlbum(data) for data in objects.PagingObject(response).items]

    async def get_all_artist_albums(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        include_groups: Sequence[objects.IncludeGroup] | None = utils.MISSING,
        credentials: OptionalCredentials = None,
    ) -> list[objects.SimpleAlbum]:

        if include_groups == utils.MISSING:
            include_groups = [objects.IncludeGroup.ALBUM]

        response = await self.http.get_artist_albums(_id, market=market, include_groups=include_groups, limit=50, offset=0, credentials=credentials)
        paging = objects.PagingObject(response)

        albums = [objects.SimpleAlbum(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or fewer tracks, and we already have them so just return them
            return albums

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_artist_albums(_id, market=market, include_groups=include_groups, limit=50, offset=_ * 50, credentials=credentials)
            albums.extend([objects.SimpleAlbum(data) for data in objects.PagingObject(response).items])

        return albums

    # BROWSE API

    async def get_new_releases(
        self,
        *,
        country: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.SimpleAlbum]:

        response = await self.http.get_new_releases(country=country, limit=limit, offset=offset, credentials=credentials)
        return [objects.SimpleAlbum(data) for data in objects.PagingObject(response["albums"]).items]

    async def get_featured_playlists(
        self,
        *,
        country: str | None = None,
        locale: str | None = None,
        timestamp: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: OptionalCredentials = None,
    ) -> tuple[str, list[objects.SimplePlaylist]]:

        response = await self.http.get_featured_playlists(
            country=country,
            locale=locale,
            timestamp=timestamp,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return response["message"], [objects.SimplePlaylist(data) for data in objects.PagingObject(response["playlists"]).items]

    async def get_categories(
        self,
        *,
        country: str | None = None,
        locale: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.Category]:

        response = await self.http.get_categories(country=country, locale=locale, limit=limit, offset=offset, credentials=credentials)
        return [objects.Category(data) for data in objects.PagingObject(response["categories"]).items]

    async def get_category(
        self,
        _id: str,
        /,
        *,
        country: str | None = None,
        locale: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> objects.Category:

        response = await self.http.get_category(_id, country=country, locale=locale, credentials=credentials)
        return objects.Category(response)

    async def get_category_playlists(
        self,
        _id: str,
        /,
        *,
        country: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.SimplePlaylist]:

        response = await self.http.get_category_playlists(_id, country=country, limit=limit, offset=offset, credentials=credentials)
        return [objects.SimplePlaylist(data) for data in objects.PagingObject(response["playlists"]).items]

    async def get_recommendations(
        self,
        *,
        seed_artist_ids: Sequence[str] | None = None,
        seed_genres: Sequence[str] | None = None,
        seed_track_ids: Sequence[str] | None = None,
        limit: int | None = None,
        market: str | None = None,
        credentials: OptionalCredentials = None,
        **kwargs: int
    ) -> objects.Recommendation:

        response = await self.http.get_recommendations(
            seed_artist_ids=seed_artist_ids,
            seed_genres=seed_genres,
            seed_track_ids=seed_track_ids,
            limit=limit,
            market=market,
            credentials=credentials,
            **kwargs
        )
        return objects.Recommendation(response)

    async def get_recommendation_genres(
        self,
        *,
        credentials: OptionalCredentials = None,
    ) -> list[str]:

        response = await self.http.get_recommendation_genres(credentials=credentials)
        return response["genres"]

    # EPISODE API

    async def get_episodes(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = "GB",
        credentials: OptionalCredentials = None,
    ) -> dict[ID, objects.Episode | None]:

        response = await self.http.get_episodes(ids=ids, market=market, credentials=credentials)
        return dict(zip(ids, [objects.Episode(data) if data else None for data in response["episodes"]]))

    async def get_episode(
        self,
        _id: str,
        /,
        *,
        market: str | None = "GB",
        credentials: OptionalCredentials = None,
    ) -> objects.Episode:

        response = await self.http.get_episode(_id, market=market, credentials=credentials)
        return objects.Episode(response)

    # FOLLOW API

    ...

    # LIBRARY API

    ...

    # MARKETS API

    async def get_available_markets(
        self,
        *,
        credentials: OptionalCredentials = None,
    ) -> list[str]:

        response = await self.http.get_available_markets(credentials=credentials)
        return response["markets"]

    # PERSONALIZATION API

    async def get_current_users_top_artists(
        self,
        *,
        time_range: objects.TimeRange | None,
        limit: int | None,
        offset: int | None,
        credentials: Credentials,
    ) -> list[objects.Artist]:

        response = await self.http.get_current_users_top_artists(time_range=time_range, limit=limit, offset=offset, credentials=credentials)
        return [objects.Artist(data) for data in objects.PagingObject(response).items]

    async def get_current_users_top_tracks(
        self,
        *,
        time_range: objects.TimeRange | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: Credentials,
    ) -> list[objects.Track]:

        response = await self.http.get_current_users_top_tracks(time_range=time_range, limit=limit, offset=offset, credentials=credentials)
        return [objects.Track(data) for data in objects.PagingObject(response).items]

    # PLAYLISTS API

    async def get_playlist(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        fields: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> objects.Playlist:

        response = await self.http.get_playlist(_id, market=market, fields=fields, credentials=credentials)
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
        credentials: OptionalCredentials = None,
    ) -> list[objects.PlaylistTrack]:

        response = await self.http.get_playlist_items(_id, market=market, fields=fields, limit=limit, offset=offset, credentials=credentials)
        return [objects.PlaylistTrack(data) for data in objects.PagingObject(response).items]

    async def get_all_playlist_items(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        fields: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.PlaylistTrack]:

        response = await self.http.get_playlist_items(_id, market=market, fields=fields, limit=100, offset=0, credentials=credentials)
        paging = objects.PagingObject(response)

        items = [objects.PlaylistTrack(data) for data in paging.items]

        if paging.total <= 100:  # There are 50 or fewer tracks, and we already have them so just return them
            return items

        for _ in range(1, math.ceil(paging.total / 100)):
            response = await self.http.get_playlist_items(_id, market=market, fields=fields, limit=100, offset=_ * 100, credentials=credentials)
            items.extend([objects.PlaylistTrack(data) for data in objects.PagingObject(response).items])

        return items

    async def get_full_playlist(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        fields: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> objects.Playlist:

        playlist = await self.get_playlist(_id, market=market, fields=fields, credentials=credentials)

        if playlist._tracks_paging.total <= 100:  # The playlist has 100 or fewer tracks already, so we can just return it now.
            return playlist

        for _ in range(1, math.ceil(playlist._tracks_paging.total / 100)):
            response = await self.http.get_playlist_items(_id, market=market, fields=fields, limit=100, offset=_ * 100, credentials=credentials)
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
        include_external: bool = False,
        credentials: OptionalCredentials = None,
    ) -> objects.SearchResult:

        response = await self.http.search(
            query,
            search_types=search_types,
            market=market,
            limit=limit,
            offset=offset,
            include_external=include_external,
            credentials=credentials
        )
        return objects.SearchResult(response)

    # SHOWS API

    async def get_shows(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = "GB",
        credentials: OptionalCredentials = None,
    ) -> dict[ID, objects.Show | None]:

        response = await self.http.get_shows(ids, market=market, credentials=credentials)
        return dict(zip(ids, [objects.Show(data) if data else None for data in response["shows"]]))

    async def get_show(
        self,
        _id: str,
        /,
        *,
        market: str | None = "GB",
        credentials: OptionalCredentials = None,
    ) -> objects.Show:

        response = await self.http.get_show(_id, market=market, credentials=credentials)
        return objects.Show(response)

    async def get_show_episodes(
        self,
        _id: str,
        /,
        *,
        market: str | None = "GB",
        limit: int | None = None,
        offset: int | None = None,
        credentials: OptionalCredentials = None,
    ) -> list[objects.SimpleEpisode]:

        response = await self.http.get_show_episodes(_id, market=market, limit=limit, offset=offset, credentials=credentials)
        return [objects.SimpleEpisode(data) for data in objects.PagingObject(response).items]

    async def get_all_show_episodes(
        self,
        _id: str,
        /,
        *,
        market: str | None = "GB",
        credentials: OptionalCredentials = None,
    ) -> list[objects.SimpleEpisode]:

        response = await self.http.get_show_episodes(_id, market=market, limit=50, offset=0, credentials=credentials)
        paging = objects.PagingObject(response)

        episodes = [objects.SimpleEpisode(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or fewer episodes, and we already have them so just return them
            return episodes

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_show_episodes(_id, market=market, limit=50, offset=_ * 50, credentials=credentials)
            episodes.extend([objects.SimpleEpisode(data) for data in objects.PagingObject(response).items])

        return episodes

    # TRACKS API #

    async def get_tracks(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> dict[ID, objects.Track | None]:

        response = await self.http.get_tracks(ids=ids, market=market, credentials=credentials)
        return dict(zip(ids, [objects.Track(data) if data else None for data in response["tracks"]]))

    async def get_track(
        self,
        _id: str,
        /,
        *,
        market: str | None = None,
        credentials: OptionalCredentials = None,
    ) -> objects.Track:

        response = await self.http.get_track(_id, market=market, credentials=credentials)
        return objects.Track(response)

    async def get_several_tracks_audio_features(
        self,
        ids: Sequence[ID],
        *,
        credentials: OptionalCredentials = None,
    ) -> dict[ID, objects.AudioFeatures | None]:

        response = await self.http.get_several_tracks_audio_features(ids, credentials=credentials)
        return dict(zip(ids, [objects.AudioFeatures(data) if data else None for data in response["audio_features"]]))

    async def get_track_audio_features(
        self,
        _id: str,
        /,
        *,
        credentials: OptionalCredentials = None,
    ) -> objects.AudioFeatures:

        response = await self.http.get_track_audio_features(_id, credentials=credentials)
        return objects.AudioFeatures(response)

    ...

    # USERS API

    async def get_current_user_profile(
        self,
        *,
        credentials: Credentials,
    ) -> objects.User:

        response = await self.http.get_current_user_profile(credentials=credentials)
        return objects.User(response)

    async def get_user_profile(
        self,
        _id: str,
        /,
        *,
        credentials: Credentials,
    ) -> objects.User:

        response = await self.http.get_user_profile(_id, credentials=credentials)
        return objects.User(response)
