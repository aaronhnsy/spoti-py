from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TypeVar

import aiohttp

from .http import HTTPClient
from .objects import (
    ClientCredentials, UserCredentials, Album, SimpleTrack, SimpleAlbum, Artist, IncludeGroup,
    PagingObject, Track, Show, SimpleEpisode, AudioFeatures, Recommendation, SearchType,
    SearchResult, User, TimeRange, Playlist, PlaylistTrack, SimplePlaylist, Category, Image,
    Episode,
)


__all__ = (
    "Client",
)


ID = TypeVar("ID", bound=str)


class Client:

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: aiohttp.ClientSession | None = None
    ) -> None:

        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._session: aiohttp.ClientSession | None = session

        self.http: HTTPClient = HTTPClient(
            client_id=self._client_id,
            client_secret=self._client_secret,
            session=self._session
        )

    def __repr__(self) -> str:
        return "<spotipy.Client>"

    # ALBUMS API

    async def get_album(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Album:

        response = await self.http.get_album(_id, market=market, credentials=credentials)
        return Album(response)

    async def get_albums(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> dict[ID, Album | None]:

        response = await self.http.get_albums(ids=ids, market=market, credentials=credentials)
        return dict(zip(ids, [Album(data) if data else None for data in response["albums"]]))

    async def get_album_tracks(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimpleTrack]:

        response = await self.http.get_album_tracks(
            _id,
            market=market,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [SimpleTrack(data) for data in PagingObject(response).items]

    async def get_all_album_tracks(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimpleTrack]:

        response = await self.http.get_album_tracks(_id, market=market, limit=50, offset=0, credentials=credentials)
        paging = PagingObject(response)

        tracks = [SimpleTrack(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or fewer tracks, and we already have them so just return them
            return tracks

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_album_tracks(
                _id,
                market=market,
                limit=50,
                offset=_ * 50,
                credentials=credentials
            )
            tracks.extend([SimpleTrack(data) for data in PagingObject(response).items])

        return tracks

    async def get_full_album(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Album:

        album = await self.get_album(_id, market=market, credentials=credentials)

        if album._tracks_paging.total <= 50:
            return album

        for _ in range(2, math.ceil(album._tracks_paging.total / 50)):
            response = await self.http.get_album_tracks(
                _id,
                market=market,
                limit=50,
                offset=_ * 50,
                credentials=credentials
            )
            album.tracks.extend([SimpleTrack(data) for data in PagingObject(response).items])

        return album

    async def get_saved_albums(self) -> ...:
        raise NotImplementedError

    async def save_albums(self) -> ...:
        raise NotImplementedError

    async def remove_albums(self) -> ...:
        raise NotImplementedError

    async def check_saved_albums(self) -> ...:
        raise NotImplementedError

    async def get_new_releases(
        self,
        *,
        country: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimpleAlbum]:

        response = await self.http.get_new_releases(
            country=country,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [SimpleAlbum(data) for data in PagingObject(response["albums"]).items]

    # ARTISTS API

    async def get_artist(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Artist:

        response = await self.http.get_artist(_id, market=market, credentials=credentials)
        return Artist(response)

    async def get_artists(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> dict[ID, Artist | None]:

        response = await self.http.get_artists(ids=ids, market=market, credentials=credentials)
        return dict(zip(ids, [Artist(data) if data else None for data in response["artists"]]))

    async def get_artist_albums(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        include_groups: list[IncludeGroup] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimpleAlbum]:

        if include_groups is None:
            include_groups = [IncludeGroup.Album]

        response = await self.http.get_artist_albums(
            _id,
            market=market,
            include_groups=include_groups,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [SimpleAlbum(data) for data in PagingObject(response).items]

    async def get_all_artist_albums(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        include_groups: list[IncludeGroup] | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimpleAlbum]:

        if include_groups is None:
            include_groups = [IncludeGroup.Album]

        response = await self.http.get_artist_albums(
            _id,
            market=market,
            include_groups=include_groups,
            limit=50,
            offset=0,
            credentials=credentials
        )
        paging = PagingObject(response)

        albums = [SimpleAlbum(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or fewer tracks, and we already have them so just return them
            return albums

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_artist_albums(
                _id,
                market=market,
                include_groups=include_groups,
                limit=50,
                offset=_ * 50,
                credentials=credentials
            )
            albums.extend([SimpleAlbum(data) for data in PagingObject(response).items])

        return albums

    async def get_artist_top_tracks(
        self,
        _id: str,
        /, *,
        market: str = "GB",
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[Track]:

        response = await self.http.get_artist_top_tracks(_id, market=market, credentials=credentials)
        return [Track(data) for data in response["tracks"]]

    async def get_related_artists(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[Artist]:

        response = await self.http.get_related_artists(_id, market=market, credentials=credentials)
        return [Artist(data) for data in response["artists"]]

    # SHOWS API

    async def get_show(
        self,
        _id: str,
        /, *,
        market: str | None = "GB",
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Show:

        response = await self.http.get_show(_id, market=market, credentials=credentials)
        return Show(response)

    async def get_shows(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = "GB",
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> dict[ID, Show | None]:

        response = await self.http.get_shows(ids, market=market, credentials=credentials)
        return dict(zip(ids, [Show(data) if data else None for data in response["shows"]]))

    async def get_show_episodes(
        self,
        _id: str,
        /, *,
        market: str | None = "GB",
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimpleEpisode]:

        response = await self.http.get_show_episodes(
            _id,
            market=market,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [SimpleEpisode(data) for data in PagingObject(response).items]

    async def get_all_show_episodes(
        self,
        _id: str,
        /, *,
        market: str | None = "GB",
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimpleEpisode]:

        response = await self.http.get_show_episodes(_id, market=market, limit=50, offset=0, credentials=credentials)
        paging = PagingObject(response)

        episodes = [SimpleEpisode(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or fewer episodes, and we already have them so just return them
            return episodes

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_show_episodes(
                _id,
                market=market,
                limit=50,
                offset=_ * 50,
                credentials=credentials
            )
            episodes.extend([SimpleEpisode(data) for data in PagingObject(response).items])

        return episodes

    async def get_saved_shows(self) -> ...:
        raise NotImplementedError

    async def save_shows(self) -> ...:
        raise NotImplementedError

    async def remove_shows(self) -> ...:
        raise NotImplementedError

    async def check_saved_shows(self) -> ...:
        raise NotImplementedError

    # EPISODE API

    async def get_episode(
        self,
        _id: str,
        /, *,
        market: str | None = "GB",
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Episode:

        response = await self.http.get_episode(_id, market=market, credentials=credentials)
        return Episode(response)

    async def get_episodes(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = "GB",
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> dict[ID, Episode | None]:

        response = await self.http.get_episodes(ids=ids, market=market, credentials=credentials)
        return dict(zip(ids, [Episode(data) if data else None for data in response["episodes"]]))

    async def get_saved_episodes(self) -> ...:
        raise NotImplementedError

    async def save_episodes(self) -> ...:
        raise NotImplementedError

    async def remove_episodes(self) -> ...:
        raise NotImplementedError

    async def check_saved_episodes(self) -> ...:
        raise NotImplementedError

    # TRACKS API

    async def get_track(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Track:

        response = await self.http.get_track(_id, market=market, credentials=credentials)
        return Track(response)

    async def get_tracks(
        self,
        ids: Sequence[ID],
        *,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> dict[ID, Track | None]:

        response = await self.http.get_tracks(ids=ids, market=market, credentials=credentials)
        return dict(zip(ids, [Track(data) if data else None for data in response["tracks"]]))

    async def get_saved_tracks(self) -> ...:
        raise NotImplementedError

    async def save_tracks(self) -> ...:
        raise NotImplementedError

    async def remove_tracks(self) -> ...:
        raise NotImplementedError

    async def check_saved_tracks(self) -> ...:
        raise NotImplementedError

    async def get_several_tracks_audio_features(
        self,
        ids: Sequence[ID],
        *,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> dict[ID, AudioFeatures | None]:

        response = await self.http.get_several_tracks_audio_features(ids, credentials=credentials)
        return dict(zip(ids, [AudioFeatures(data) if data else None for data in response["audio_features"]]))

    async def get_track_audio_features(
        self,
        _id: str,
        /, *,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> AudioFeatures:

        response = await self.http.get_track_audio_features(_id, credentials=credentials)
        return AudioFeatures(response)

    async def get_track_audio_analysis(self) -> ...:
        raise NotImplementedError

    async def get_recommendations(
        self,
        *,
        seed_artist_ids: list[str] | None = None,
        seed_genres: list[str] | None = None,
        seed_track_ids: list[str] | None = None,
        limit: int | None = None,
        market: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
        **kwargs: int
    ) -> Recommendation:

        response = await self.http.get_recommendations(
            seed_artist_ids=seed_artist_ids,
            seed_genres=seed_genres,
            seed_track_ids=seed_track_ids,
            limit=limit,
            market=market,
            credentials=credentials,
            **kwargs
        )
        return Recommendation(response)

    # SEARCH API

    async def search(
        self,
        query: str,
        /, *,
        search_types: list[SearchType] | None = None,
        market: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        include_external: bool = False,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> SearchResult:

        if search_types is None:
            search_types = [SearchType.All]

        response = await self.http.search(
            query,
            search_types=search_types,
            market=market,
            limit=limit,
            offset=offset,
            include_external=include_external,
            credentials=credentials
        )
        return SearchResult(response)

    # USERS API

    async def get_current_user_profile(
        self,
        *,
        credentials: UserCredentials,
    ) -> User:

        response = await self.http.get_current_user_profile(credentials=credentials)
        return User(response)

    async def get_current_users_top_artists(
        self,
        *,
        time_range: TimeRange | None,
        limit: int | None,
        offset: int | None,
        credentials: UserCredentials,
    ) -> list[Artist]:

        response = await self.http.get_current_user_top_artists(
            time_range=time_range,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [Artist(data) for data in PagingObject(response).items]

    async def get_current_users_top_tracks(
        self,
        *,
        time_range: TimeRange | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: UserCredentials,
    ) -> list[Track]:

        response = await self.http.get_current_user_top_tracks(
            time_range=time_range,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [Track(data) for data in PagingObject(response).items]

    async def get_user_profile(
        self,
        _id: str,
        /, *,
        credentials: UserCredentials,
    ) -> User:

        response = await self.http.get_user_profile(_id, credentials=credentials)
        return User(response)

    async def follow_playlist(self) -> ...:
        raise NotImplementedError

    async def unfollow_playlist(self) -> ...:
        raise NotImplementedError

    async def get_followed_artists(self) -> ...:
        raise NotImplementedError

    async def get_followed_users(self) -> ...:
        raise NotImplementedError

    async def follow_artists(self) -> ...:
        raise NotImplementedError

    async def follow_users(self) -> ...:
        raise NotImplementedError

    async def unfollow_artists(self) -> ...:
        raise NotImplementedError

    async def unfollow_users(self) -> ...:
        raise NotImplementedError

    async def check_followed_artists(self) -> ...:
        raise NotImplementedError

    async def check_followed_users(self) -> ...:
        raise NotImplementedError

    async def check_playlist_followers(self) -> ...:
        raise NotImplementedError

    # PLAYLISTS API

    async def get_playlist(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        fields: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Playlist:

        response = await self.http.get_playlist(_id, market=market, fields=fields, credentials=credentials)
        return Playlist(response)

    async def change_playlist_details(self) -> ...:
        raise NotImplementedError

    async def get_playlist_items(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        fields: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[PlaylistTrack]:

        response = await self.http.get_playlist_items(
            _id,
            market=market,
            fields=fields,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [PlaylistTrack(data) for data in PagingObject(response).items]

    async def get_all_playlist_items(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        fields: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[PlaylistTrack]:

        response = await self.http.get_playlist_items(
            _id,
            market=market,
            fields=fields,
            limit=100,
            offset=0,
            credentials=credentials
        )
        paging = PagingObject(response)

        items = [PlaylistTrack(data) for data in paging.items]

        if paging.total <= 100:  # There are 50 or fewer tracks, and we already have them so just return them
            return items

        for _ in range(1, math.ceil(paging.total / 100)):
            response = await self.http.get_playlist_items(
                _id,
                market=market,
                fields=fields,
                limit=100,
                offset=_ * 100,
                credentials=credentials
            )
            items.extend([PlaylistTrack(data) for data in PagingObject(response).items])

        return items

    async def get_full_playlist(
        self,
        _id: str,
        /, *,
        market: str | None = None,
        fields: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Playlist:

        playlist = await self.get_playlist(_id, market=market, fields=fields, credentials=credentials)

        if playlist._tracks_paging.total <= 100:
            return playlist

        for _ in range(1, math.ceil(playlist._tracks_paging.total / 100)):
            response = await self.http.get_playlist_items(
                _id,
                market=market,
                fields=fields,
                limit=100,
                offset=_ * 100,
                credentials=credentials
            )
            playlist.tracks.extend([PlaylistTrack(data) for data in PagingObject(response).items])

        return playlist

    async def add_items_to_playlist(self) -> ...:
        raise NotImplementedError

    async def reorder_playlist_items(self) -> ...:
        raise NotImplementedError

    async def replace_playlist_items(self) -> ...:
        raise NotImplementedError

    async def remove_items_from_playlist(self) -> ...:
        raise NotImplementedError

    async def get_current_user_playlists(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        credentials: UserCredentials,
    ) -> list[SimplePlaylist]:

        response = await self.http.get_current_user_playlists(limit=limit, offset=offset, credentials=credentials)
        return [SimplePlaylist(data) for data in PagingObject(response).items]

    async def get_all_current_user_playlists(
        self,
        *,
        credentials: UserCredentials,
    ) -> list[SimplePlaylist]:

        response = await self.http.get_current_user_playlists(limit=50, offset=0, credentials=credentials)
        paging = PagingObject(response)

        playlists = [SimplePlaylist(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or fewer playlists, and we already have them so just return them
            return playlists

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_current_user_playlists(limit=50, offset=_ * 50, credentials=credentials)
            playlists.extend([SimplePlaylist(data) for data in PagingObject(response).items])

        return playlists

    async def get_user_playlists(
        self,
        _id: str,
        /, *,
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimplePlaylist]:

        response = await self.http.get_user_playlists(_id, limit=limit, offset=offset, credentials=credentials)
        return [SimplePlaylist(data) for data in PagingObject(response).items]

    async def get_all_user_playlists(
        self,
        _id: str,
        /, *,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimplePlaylist]:

        response = await self.http.get_user_playlists(_id, limit=50, offset=0, credentials=credentials)
        paging = PagingObject(response)

        playlists = [SimplePlaylist(data) for data in paging.items]

        if paging.total <= 50:  # There are 50 or fewer playlists, and we already have them so just return them
            return playlists

        for _ in range(1, math.ceil(paging.total / 50)):
            response = await self.http.get_user_playlists(_id, limit=50, offset=_ * 50, credentials=credentials)
            playlists.extend([SimplePlaylist(data) for data in PagingObject(response).items])

        return playlists

    async def create_playlist(self) -> ...:
        raise NotImplementedError

    async def get_featured_playlists(
        self,
        *,
        country: str | None = None,
        locale: str | None = None,
        timestamp: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> tuple[str, list[SimplePlaylist]]:

        response = await self.http.get_featured_playlists(
            country=country,
            locale=locale,
            timestamp=timestamp,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return response["message"], [SimplePlaylist(data) for data in PagingObject(response["playlists"]).items]

    async def get_category_playlists(
        self,
        _id: str,
        /, *,
        country: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[SimplePlaylist]:

        response = await self.http.get_category_playlists(
            _id,
            country=country,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [SimplePlaylist(data) for data in PagingObject(response["playlists"]).items]

    async def get_playlist_cover_image(
        self,
        _id: str,
        /, *,
        credentials: ClientCredentials | UserCredentials | None = None
    ) -> list[Image]:

        response = await self.http.get_playlist_cover_image(_id, credentials=credentials)
        return [Image(data) for data in response]

    async def upload_playlist_cover_image(self) -> ...:
        raise NotImplementedError

    # CATEGORY API

    async def get_categories(
        self,
        *,
        country: str | None = None,
        locale: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[Category]:

        response = await self.http.get_categories(
            country=country,
            locale=locale,
            limit=limit,
            offset=offset,
            credentials=credentials
        )
        return [Category(data) for data in PagingObject(response["categories"]).items]

    async def get_category(
        self,
        _id: str,
        /, *,
        country: str | None = None,
        locale: str | None = None,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> Category:

        response = await self.http.get_category(_id, country=country, locale=locale, credentials=credentials)
        return Category(response)

    # GENRE API

    async def get_available_genre_seeds(
        self,
        *,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[str]:

        response = await self.http.get_available_genre_seeds(credentials=credentials)
        return response["genres"]

    # PLAYER API

    async def get_playback_state(self) -> ...:
        raise NotImplementedError

    async def transfer_playback(self) -> ...:
        raise NotImplementedError

    async def get_available_devices(self) -> ...:
        raise NotImplementedError

    async def get_currently_playing_track(self) -> ...:
        raise NotImplementedError

    async def start_playback(self) -> ...:
        raise NotImplementedError

    async def resume_playback(self) -> ...:
        raise NotImplementedError

    async def pause_playback(self) -> ...:
        raise NotImplementedError

    async def skip_to_next(self) -> ...:
        raise NotImplementedError

    async def skip_to_previous(self) -> ...:
        raise NotImplementedError

    async def seek_to_position(self) -> ...:
        raise NotImplementedError

    async def set_repeat_mode(self) -> ...:
        raise NotImplementedError

    async def set_playback_volume(self) -> ...:
        raise NotImplementedError

    async def toggle_playback_shuffle(self) -> ...:
        raise NotImplementedError

    async def get_recently_played_tracks(self) -> ...:
        raise NotImplementedError

    async def add_item_to_playback_queue(self) -> ...:
        raise NotImplementedError

    # MARKETS API

    async def get_available_markets(
        self,
        *,
        credentials: ClientCredentials | UserCredentials | None = None,
    ) -> list[str]:

        response = await self.http.get_available_markets(credentials=credentials)
        return response["markets"]
