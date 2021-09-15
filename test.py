# Future
from __future__ import annotations

# Standard Library
import asyncio
import json
from typing import Any, Callable

# My stuff
import aiospotify


def clean_dict(obj: dict[str, Any], func: Callable[[dict[str, Any] | str], ...]) -> None:

    if isinstance(obj, dict):
        for key in list(obj.keys()):
            if func(key):
                del obj[key]
            else:
                clean_dict(obj[key], func)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if func(obj[i]):
                del obj[i]
            else:
                clean_dict(obj[i], func)


client = aiospotify.Client(client_id="...", client_secret="...")

TRACK = "3uwYgNxFDfx1GoLB6tLoUn"
ALBUM = "46K4raQPIGem3N031upNj9"
ARTIST = "5Rl15oVamLq7FbSb0NNBNy"
PLAYLIST = "6RVlf8pkTeqBKKUstQjIi8"
SHOW = "1K7ATPkW0vgE9y9UQH6DaF"


async def main() -> None:

    data = await client.http.get_track_audio_analysis(TRACK)

    print(json.dumps(clean_dict(data, (lambda key: key == "available_markets")), indent=4))

    await client.http.close()
    await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.new_event_loop().run_until_complete(main())
