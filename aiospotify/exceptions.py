# Future
from __future__ import annotations

# Standard Library
from typing import TypedDict

# Packages
import aiohttp


__all__ = (
    "SpotifyException",
    "AuthenticationError",
    "SpotifyHTTPError",
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "TooManyRequests",
    "InternalServerError",
    "BadGatewayError",
    "ServiceUnavailable"
)


class AuthenticationErrorData(TypedDict):
    error: str
    error_description: str


class RegularErrorData(TypedDict):
    status: int
    message: str


class SpotifyException(Exception):
    ...


class AuthenticationError(SpotifyException):

    def __init__(self, data: AuthenticationErrorData) -> None:
        self._error = data["error"]
        self._error_description = data["error_description"]

    @property
    def error(self) -> str:
        return self._error

    @property
    def error_description(self) -> str:
        return self._error_description


class SpotifyHTTPError(SpotifyException):

    def __init__(self, response: aiohttp.ClientResponse, data: RegularErrorData) -> None:

        self._response = response
        self._status = data["status"]
        self._message = data["message"]

    @property
    def response(self) -> aiohttp.ClientResponse:
        return self._response

    @property
    def status(self) -> int:
        return self._status

    @property
    def message(self) -> str:
        return self._message


class BadRequest(SpotifyHTTPError):
    pass


class Unauthorized(SpotifyHTTPError):
    pass


class Forbidden(SpotifyHTTPError):
    pass


class NotFound(SpotifyHTTPError):
    pass


class TooManyRequests(SpotifyHTTPError):
    pass


class SpotifyServerError(SpotifyHTTPError):
    pass


class InternalServerError(SpotifyServerError):
    pass


class BadGatewayError(SpotifyServerError):
    pass


class ServiceUnavailable(SpotifyServerError):
    pass
