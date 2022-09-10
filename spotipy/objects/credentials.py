from __future__ import annotations

import time
from typing import TypedDict, ClassVar

import aiohttp

from ..errors import AuthenticationError


__all__ = (
    "ClientCredentialsData",
    "ClientCredentials",
    "UserCredentialsData",
    "UserCredentials"
)


class ClientCredentialsData(TypedDict):
    access_token: str
    token_type: str
    expires_in: int


class ClientCredentials:

    TOKEN_URL: ClassVar[str] = "https://accounts.spotify.com/api/token"

    def __init__(self, data: ClientCredentialsData, client_id: str, client_secret: str) -> None:

        self._access_token: str = data["access_token"]
        self._token_type: str = data["token_type"]
        self._expires_in: int = data["expires_in"]

        self._client_id: str = client_id
        self._client_secret: str = client_secret

        self._last_authorized_time: float = time.time()

    def __repr__(self) -> str:
        return "<spotipy.ClientCredentials>"

    # properties

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def token_type(self) -> str:
        return self._token_type

    @property
    def expires_in(self) -> int:
        return self._expires_in

    # methods

    def is_expired(self) -> bool:
        return (time.time() - self._last_authorized_time) >= self.expires_in

    @classmethod
    async def from_client_details(
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

        async with session.post(cls.TOKEN_URL, data=data) as response:

            data = await response.json()
            if "error" in data:
                raise AuthenticationError(response, data)

            return cls(data, client_id, client_secret)

    async def refresh(self, session: aiohttp.ClientSession) -> None:

        data = {
            "grant_type":    "client_credentials",
            "client_id":     self._client_id,
            "client_secret": self._client_secret
        }

        async with session.post(self.TOKEN_URL, data=data) as response:

            data = await response.json()
            if "error" in data:
                raise AuthenticationError(response, data)

            self._access_token = data["access_token"]
            self._token_type = data["token_type"]
            self._expires_in = data["expires_in"]

            self._last_authorized_time = time.time()


class UserCredentialsData(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: str


class UserCredentials:

    TOKEN_URL: ClassVar[str] = "https://accounts.spotify.com/api/token"

    def __init__(self, data: UserCredentialsData, client_id: str, client_secret: str) -> None:

        self._access_token: str = data["access_token"]
        self._token_type: str = data["token_type"]
        self._expires_in: int = data["expires_in"]
        self._scope: str = data["scope"]
        self._refresh_token: str = data["refresh_token"]

        self._client_id: str = client_id
        self._client_secret: str = client_secret

        self._last_authorized_time: float = time.time()

    def __repr__(self) -> str:
        return "<spotipy.UserCredentials>"

    # properties

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

    # methods

    def is_expired(self) -> bool:
        return (time.time() - self._last_authorized_time) >= self.expires_in

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

        async with session.post(cls.TOKEN_URL, data=data) as response:

            data = await response.json()
            if "error" in data:
                raise AuthenticationError(response, data=data)
            if "refresh_token" not in data:
                data["refresh_token"] = refresh_token

            return cls(data, client_id, client_secret)

    async def refresh(self, session: aiohttp.ClientSession) -> None:

        data = {
            "client_id":     self._client_id,
            "client_secret": self._client_secret,
            "grant_type":    "refresh_token",
            "refresh_token": self._refresh_token,
        }

        async with session.post(self.TOKEN_URL, data=data) as response:

            data = await response.json()
            if "error" in data:
                raise AuthenticationError(response, data=data)

            self._access_token = data["access_token"]
            self._token_type = data["token_type"]
            self._scope = data["scope"]
            self._expires_in = data["expires_in"]

            self._last_authorized_time = time.time()
