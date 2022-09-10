from __future__ import annotations

from ..objects.credentials import ClientCredentials, UserCredentials


__all__ = (
    "AnyCredentials",
)


AnyCredentials = ClientCredentials | UserCredentials
