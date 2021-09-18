# Future
from __future__ import annotations

# Standard Library
import time
from typing import ClassVar, Literal

# Packages
import aiohttp

# My stuff
from aiospotify import exceptions
from typings.objects import ClientCredentialsData


__all__ = (
    "ClientCredentials",
)


class ClientCredentials:

    TOKEN_ROUTE: ClassVar[str] = f"https://accounts.spotify.com/api/token"

    def __init__(self, data: ClientCredentialsData, client_id: str, client_secret: str) -> None:

        self._access_token = data["access_token"]
        self._token_type = data["token_type"]
        self._expires_in = data["expires_in"]

        self._client_id: str = client_id
        self._client_secret: str = client_secret

        self._last_authorized_time: float = time.time()

    def __repr__(self) -> str:
        return f"<aiospotify.ClientCredentials>"

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

        async with session.post(url=self.TOKEN_ROUTE, data=data) as post:

            data = await post.json()

            if data.get("error"):
                raise exceptions.AuthenticationError(data)

            self._access_token = data["access_token"]
            self._token_type = data["token_type"]
            self._expires_in = data["expires_in"]

            self._last_authorized_time = time.time()

    @classmethod
    async def create(
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

        async with session.post(url=cls.TOKEN_ROUTE, data=data) as response:

            data = await response.json()

            if data.get("error"):
                raise exceptions.AuthenticationError(data)

            return cls(data, client_id=client_id, client_secret=client_secret)
