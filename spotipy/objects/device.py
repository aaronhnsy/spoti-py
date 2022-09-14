from __future__ import annotations

from typing import TypedDict


__all__ = (
    "DeviceData",
    "Device",
)


class DeviceData(TypedDict):
    id: str
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    type: str
    volume_percent: int


class Device:

    def __init__(self, data: DeviceData) -> None:
        self.id: str = data["id"]
        self.is_active: bool = data["is_active"]
        self.is_private_session: bool = data["is_private_session"]
        self.is_restricted: bool = data["is_restricted"]
        self.name: str = data["name"]
        self.type: str = data["type"]
        self.volume_percent: int = data["volume_percent"]

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: id='{self.id}', name='{self.name}'>"
