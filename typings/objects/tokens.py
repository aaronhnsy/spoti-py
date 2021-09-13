# Future
from __future__ import annotations

# Standard Library
from typing import Literal, TypedDict


class ClientCredentialsData(TypedDict):
    access_token: str
    token_type: Literal["bearer"]
    expires_in: int
