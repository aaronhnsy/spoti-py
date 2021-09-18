# Future
from __future__ import annotations

# My stuff
from aiospotify.typings.exceptions import AuthenticationErrorData, RegularErrorData


__all__ = (
    "SpotifyException",
    "AuthenticationError",
    "SpotifyResponseError",
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "TooManyRequests",
    "InternalServerError",
    "BadGatewayError",
    "ServiceUnavailable"
)


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


class SpotifyResponseError(SpotifyException):

    def __init__(self, data: RegularErrorData) -> None:
        self._status = data["status"]
        self._message = data["message"]

    @property
    def status(self) -> int:
        return self._status

    @property
    def message(self) -> str:
        return self._message


class BadRequest(SpotifyResponseError):
    pass


class Unauthorized(SpotifyResponseError):
    pass


class Forbidden(SpotifyResponseError):
    pass


class NotFound(SpotifyResponseError):
    pass


class TooManyRequests(SpotifyResponseError):
    pass


class InternalServerError(SpotifyResponseError):
    pass


class BadGatewayError(SpotifyResponseError):
    pass


class ServiceUnavailable(SpotifyResponseError):
    pass
