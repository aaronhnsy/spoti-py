# Future
from __future__ import annotations

# Standard Library
from typing import TypedDict


__all__ = (
    "AuthenticationErrorData",
    "RegularErrorData",
)


class AuthenticationErrorData(TypedDict):
    error: str
    error_description: str


class RegularErrorData(TypedDict):
    status: int
    message: str
