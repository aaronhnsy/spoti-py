# Future
from __future__ import annotations

# My stuff
from spotipy.typings.objects import DeviceData


__all__ = (
    "Device",
)


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
