from __future__ import annotations

import aiohttp

from .types.errors import HTTPErrorData, AuthenticationErrorData


__all__ = (
    "SpotipyError",
    "AuthenticationError",
    "HTTPError",
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "RequestEntityTooLarge",
    "SpotifyServerError",
    "HTTPErrorMapping"
)


class SpotipyError(Exception):
    pass


class AuthenticationError(SpotipyError):

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        data: AuthenticationErrorData
    ) -> None:
        self._response: aiohttp.ClientResponse = response
        self._error: str = data["error"]
        self._description: str = data["error_description"]

        super().__init__(self._description)

    @property
    def response(self) -> aiohttp.ClientResponse:
        return self._response

    @property
    def error(self) -> str:
        return self._error

    @property
    def description(self) -> str:
        return self._description


class HTTPError(SpotipyError):

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        data: HTTPErrorData | str
    ) -> None:
        self._response: aiohttp.ClientResponse = response
        self._status: int = response.status
        self._message: str = data["error"]["message"] if isinstance(data, dict) else (data or "")

        super().__init__(f"{self._status} - {response.reason}: {self._message}")

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


class SpotifyServerError(HTTPError):
    pass


HTTPErrorMapping: dict[int, type[HTTPError]] = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
}
