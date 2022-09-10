from __future__ import annotations

from typing import TypedDict


__all__ = (
    "AuthenticationErrorData",
    "HTTPErrorKeyData",
    "HTTPErrorData",
)


class AuthenticationErrorData(TypedDict):
    error: str
    error_description: str


class HTTPErrorKeyData(TypedDict):
    status: int
    message: str


class HTTPErrorData(TypedDict):
    error: HTTPErrorKeyData
