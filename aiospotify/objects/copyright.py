# Future
from __future__ import annotations

# My stuff
from aiospotify import objects


__all__ = (
    "Copyright",
)


class Copyright:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.text: str | None = data.get('text')
        self.type: objects.CopyrightType = objects.CopyrightType(data.get('type', 'C'))

    def __repr__(self) -> str:
        return f'<spotify.Copyright type={self.type!r}>'
