from __future__ import annotations

import json
from typing import Any, Literal

import aiohttp


__all__ = (
    "to_json",
    "from_json",
    "limit_value",
    "json_or_text",
    "to_json",
    "MISSING",
)

to_json = json.dumps
from_json = json.loads


async def json_or_text(response: aiohttp.ClientResponse) -> dict[str, Any] | str:

    text = await response.text(encoding="utf-8")

    try:
        if response.headers["content-type"] in ["application/json", "application/json; charset=utf-8"]:
            return from_json(text)
    except KeyError:
        pass

    return text


def limit_value(name: str, value: int, minimum: int, maximum: int) -> None:

    if value < minimum or value > maximum:
        raise ValueError(f"'{name}' must be more than {minimum} and less than {maximum}")


class _MissingSentinel:

    def __eq__(self, other: Any) -> Literal[False]:
        return False

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "..."


MISSING: Any = _MissingSentinel()
