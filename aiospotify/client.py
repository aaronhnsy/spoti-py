# Future
from __future__ import annotations

# Packages
import aiohttp

# My stuff
from aiospotify import http, objects, utils


__all__ = (
    "Client",
)


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

        self.http = http.HTTPClient(client_id=self._client_id, client_secret=self._client_secret, session=self._session)

    def __repr__(self) -> str:
        return "<aiospotify.Client>"
