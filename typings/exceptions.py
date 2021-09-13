# Future
from __future__ import annotations

# Standard Library
from typing import TypedDict


class AuthenticationErrorData(TypedDict):
    error: str
    error_description: str


class RegularErrorData(TypedDict):
    status: int
    message: str
