# Future
from __future__ import annotations

# Standard Library
from typing import Any

# Packages
import aiohttp


__all__ = (
    "SpotifyException",
    "AuthenticationError",
    "HTTPError",
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "RequestEntityTooLarge",
    "TooManyRequests",
)


class SpotifyException(Exception):
    pass


class AuthenticationError(SpotifyException):

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        /,
        *,
        data: dict[str, Any]
    ) -> None:

        self._response: aiohttp.ClientResponse = response
        self._error: str = data["error"]
        self._error_description: str = data["error_description"]

    @property
    def response(self) -> aiohttp.ClientResponse:
        return self._response

    @property
    def error(self) -> str:
        return self._error

    @property
    def error_description(self) -> str:
        return self._error_description


class HTTPError(SpotifyException):

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        /,
        *,
        data: dict[str, dict[str, Any]] | None
    ) -> None:

        self._response: aiohttp.ClientResponse = response
        self._status: int = response.status

        if isinstance(data, dict):
            self._message: str = data["error"]["message"]
        else:
            self._message: str = data or ""

        message = f"{self.response.status} {self.response.reason}"
        if len(self.message):
            message += f": {self.message}"

        super().__init__(message)

    @property
    def response(self) -> aiohttp.ClientResponse:
        return self._response

    @property
    def status(self) -> int:
        return self._status

    @property
    def message(self) -> str:
        return self._message


class BadRequest(HTTPError):
    pass


class Unauthorized(HTTPError):
    pass


class Forbidden(HTTPError):
    pass


class NotFound(HTTPError):
    pass


class RequestEntityTooLarge(HTTPError):
    pass


class TooManyRequests(HTTPError):
    pass


class SpotifyServerError(HTTPError):
    pass
