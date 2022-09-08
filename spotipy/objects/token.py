from __future__ import annotations

import time

import aiohttp

from spotipy import exceptions, values
from spotipy.typings.objects import ClientCredentialsData, UserCredentialsData


__all__ = (
    "ClientCredentials",
    "UserCredentials"
)


class ClientCredentials:

    def __init__(self, data: ClientCredentialsData, client_id: str, client_secret: str) -> None:

        self._access_token = data["access_token"]
        self._token_type = data["token_type"]
        self._expires_in = data["expires_in"]

        self._client_id: str = client_id
        self._client_secret: str = client_secret

        self._last_authorized_time: float = time.time()

    def __repr__(self) -> str:
        return "<spotipy.ClientCredentials>"

    #

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def token_type(self) -> str:
        return self._token_type

    @property
    def expires_in(self) -> int:
        return self._expires_in

    #

    def is_expired(self) -> bool:
        return (time.time() - self._last_authorized_time) >= self.expires_in

    async def refresh(
        self,
        *,
        session: aiohttp.ClientSession
    ) -> None:

        data = {
            "grant_type":    "client_credentials",
            "client_id":     self._client_id,
            "client_secret": self._client_secret
        }

        async with session.post(url=values.TOKEN_URL, data=data) as response:

            data = await response.json()

            if data.get("error"):
                raise exceptions.AuthenticationError(response, data=data)

            self._access_token = data["access_token"]
            self._token_type = data["token_type"]
            self._expires_in = data["expires_in"]

            self._last_authorized_time = time.time()

    @classmethod
    async def from_client_secret(
        cls,
        client_id: str,
        client_secret: str,
        *,
        session: aiohttp.ClientSession
    ) -> ClientCredentials:

        data = {
            "grant_type":    "client_credentials",
            "client_id":     client_id,
            "client_secret": client_secret
        }

        async with session.post(url=values.TOKEN_URL, data=data) as response:

            data = await response.json()

            if data.get("error"):
                raise exceptions.AuthenticationError(response, data=data)

            return cls(data, client_id=client_id, client_secret=client_secret)


class UserCredentials:

    def __init__(self, data: UserCredentialsData, client_id: str, client_secret: str) -> None:

        self._access_token = data["access_token"]
        self._token_type = data["token_type"]
        self._scope = data["scope"]
        self._expires_in = data["expires_in"]
        self._refresh_token = data.get("refresh_token")

        self._client_id: str = client_id
        self._client_secret: str = client_secret

        self._last_authorized_time: float = time.time()

    def __repr__(self) -> str:
        return "<spotipy.UserCredentials>"

    #

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def token_type(self) -> str:
        return self._token_type

    @property
    def scope(self) -> str:
        return self._scope

    @property
    def expires_in(self) -> int:
        return self._expires_in

    #

    def is_expired(self) -> bool:
        return (time.time() - self._last_authorized_time) >= self.expires_in

    async def refresh(
        self,
        *,
        session: aiohttp.ClientSession
    ) -> None:

        data = {
            "grant_type":    "refresh_token",
            "refresh_token": self._refresh_token,
            "client_id":     self._client_id,
            "client_secret": self._client_secret
        }

        async with session.post(url=values.TOKEN_URL, data=data) as response:

            data = await response.json()

            if data.get("error"):
                raise exceptions.AuthenticationError(response, data=data)

            self._access_token = data["access_token"]
            self._token_type = data["token_type"]
            self._scope = data["scope"]
            self._expires_in = data["expires_in"]

            self._last_authorized_time = time.time()

    @classmethod
    async def from_refresh_token(
        cls,
        client_id: str,
        client_secret: str,
        *,
        session: aiohttp.ClientSession,
        refresh_token: str,
    ) -> UserCredentials:

        data = {
            "client_id":     client_id,
            "client_secret": client_secret,
            "grant_type":    "refresh_token",
            "refresh_token": refresh_token,
        }

        async with session.post(url=values.TOKEN_URL, data=data) as response:

            data = await response.json()

            if data.get("error"):
                raise exceptions.AuthenticationError(response, data=data)

            data["refresh_token"] = refresh_token

            return cls(data, client_id=client_id, client_secret=client_secret)
