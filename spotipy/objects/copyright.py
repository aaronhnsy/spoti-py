from __future__ import annotations

from spotipy import objects
from spotipy.typings.objects import CopyrightData


__all__ = (
    "Copyright",
)


class Copyright:

    def __init__(self, data: CopyrightData) -> None:
        self.text = data["text"]
        self.type = objects.CopyrightType(data["type"])

    def __repr__(self) -> str:
        return f"<spotipy.Copyright type={self.type!r}>"
