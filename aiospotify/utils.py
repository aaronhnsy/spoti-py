# Future
from __future__ import annotations

# Standard Library
import json
from typing import Any, Literal

# Packages
import aiohttp


__all__ = (
    "json_or_text",
    "MISSING"
)


async def json_or_text(response: aiohttp.ClientResponse) -> dict[str, Any] | str:

    text = await response.text(encoding="utf-8")

    try:
        if response.headers["content-type"] == "application/json; charset=utf-8":
            return json.loads(text)
    except KeyError:
        pass

    return text


class _MissingSentinel:

    def __eq__(self, other: Any) -> Literal[False]:
        return False

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "..."


MISSING: Any = _MissingSentinel()
