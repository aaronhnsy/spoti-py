# Future
from __future__ import annotations


__all__ = (
    "Followers",
)


class Followers:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.href: str = data.get('href')
        self.total: int = data.get('total')

    def __repr__(self) -> str:
        return f'<spotify.Followers total={self.total}>'
