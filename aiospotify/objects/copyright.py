# Future
from __future__ import annotations

# Standard Library
from typing import Optional

# My stuff
from aiospotify import objects


# noinspection PyArgumentList
class Copyright:

    __slots__ = 'data', 'text', 'type'

    def __init__(self, data: dict) -> None:
        self.data = data

        self.text: Optional[str] = data.get('text')
        self.type: objects.CopyrightType = objects.CopyrightType(data.get('type', 'C'))

    def __repr__(self) -> str:
        return f'<spotify.Copyright type={self.type!r}>'
