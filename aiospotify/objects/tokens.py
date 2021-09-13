# Future
from __future__ import annotations

# Standard Library
import time
from typing import Literal

# Packages
import aiohttp

# My stuff
from aiospotify import exceptions, values
from typings.objects.tokens import ClientCredentialsData


__all__ = (
    "ClientCredentials",
)


TOKEN_URL = f"{values.ACCOUNTS_BASE}/api/token"


class ClientCredentials:

    def __init__(self, data: ClientCredentialsData) -> None:

        self._access_token: str = data["access_token"]
        self._token_type: Literal["bearer"] = data["token_type"]
        self._expires_in: int = data["expires_in"]

        self._time_last_authorized: float = time.time()

    def __repr__(self) -> str:
        return f"<spotify.ClientCredentials>"

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def token_type(self) -> Literal["bearer"]:
        return self._token_type

    @property
    def expires_in(self) -> int:
        return self._expires_in

    @property
    def time_last_authorized(self) -> float:
        return self._time_last_authorized

    #

    def has_expired(self) -> bool:
        return (time.time() - self._time_last_authorized) >= self.expires_in

    async def refresh(self, session: aiohttp.ClientSession, client_id: str, client_secret: str) -> None:

        data = {
            "grant_type":    "client_credentials",
            "client_id":     client_id,
            "client_secret": client_secret
        }

        async with session.post(TOKEN_URL, data=data) as post:

            data = await post.json()

            if data.get("error"):
                raise exceptions.AuthenticationError(data)

            self._access_token = data["access_token"]
            self._token_type = data["token_type"]
            self._expires_in = data["expires_in"]

            self._time_last_authorized = time.time()

    #

    @classmethod
    async def create(cls, session: aiohttp.ClientSession, client_id: str, client_secret: str) -> ClientCredentials:

        data = {
            "grant_type":    "client_credentials",
            "client_id":     client_id,
            "client_secret": client_secret
        }

        async with session.post(TOKEN_URL, data=data) as response:

            data = await response.json()

            if data.get("error"):
                raise exceptions.AuthenticationError(data)

            return cls(data)
