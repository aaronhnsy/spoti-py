# Future
from __future__ import annotations


__all__ = (
    "Image",
)


class Image:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.url: str = data.get('url')
        self.width: int | None = data.get('width')
        self.height: int | None = data.get('height')

    def __repr__(self) -> str:
        return f'<spotify.Image url=\'<{self.url}>\' width=\'{self.width}\' height=\'{self.height}\'>'

    def __str__(self) -> str:
        return self.url
