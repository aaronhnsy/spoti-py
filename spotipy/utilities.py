from __future__ import annotations

import contextlib
import json
from typing import Any

import aiohttp


__all__ = (
    "to_json",
    "from_json",
    "json_or_text",
    "limit_value",
)

to_json = json.dumps
from_json = json.loads


async def json_or_text(response: aiohttp.ClientResponse) -> dict[str, Any] | str:

    text = await response.text(encoding="utf-8")

    with contextlib.suppress(KeyError):
        if response.headers["content-type"] in ["application/json", "application/json; charset=utf-8"]:
            return from_json(text)

    return text


def limit_value(name: str, value: int, minimum: int, maximum: int) -> None:

    if value < minimum or value > maximum:
        raise ValueError(f"'{name}' must be more than {minimum} and less than {maximum}")
