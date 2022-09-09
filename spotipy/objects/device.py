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
        self.id = data["id"]
        self.is_active = data["is_active"]
        self.is_private_session = data["is_private_session"]
        self.is_restricted = data["is_restricted"]
        self.name = data["name"]
        self.type = data["type"]
        self.volume_percent = data["volume_percent"]

    def __repr__(self) -> str:
        return f"<spotipy.Device id='{self.id}' name='{self.name}'>"
