from typing import Optional


class BaseObject:

    __slots__ = 'data', 'href', 'id', 'name', 'type', 'uri'

    def __init__(self, data: dict) -> None:
        self.data = data

        self.href: str = data.get('href')
        self.id: str = data.get('id')
        self.name: str = data.get('name')
        self.type: str = data.get('type')
        self.uri: str = data.get('uri')

    def __repr__(self) -> str:
        return f'<spotify.BaseObject id=\'{self.id}\' name=\'{self.name}\'>'

    def __str__(self) -> str:
        return self.name


class PagingObject:

    __slots__ = 'data', 'href', 'items', 'limit', 'next', 'offset', 'previous', 'total'

    def __init__(self, data: dict) -> None:
        self.data = data

        self.href: str = data.get('href')
        self.items: list[dict] = data.get('items')
        self.limit: int = data.get('limit')
        self.next: Optional[str] = data.get('next')
        self.offset: int = data.get('offset')
        self.previous: Optional[str] = data.get('previous')
        self.total: int = data.get('total')

    def __repr__(self) -> str:
        return f'<spotify.PagingObject total={self.total} offset={self.offset} limit={self.limit}>'
