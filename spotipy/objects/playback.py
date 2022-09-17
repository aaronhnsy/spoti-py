from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired

from .common import ExternalURLs
from .device import Device, DeviceData
from .track import Track, TrackData


__all__ = (
    "ActionsData",
    "Actions",
    "ContextData",
    "Context",
    "PlaybackStateData",
    "PlaybackState",
    "CurrentlyPlayingData",
    "CurrentlyPlaying",
)


class ActionsData(TypedDict):
    interrupting_playback: NotRequired[bool]
    pausing: NotRequired[bool]
    resuming: NotRequired[bool]
    seeking: NotRequired[bool]
    skipping_next: NotRequired[bool]
    skipping_prev: NotRequired[bool]
    toggling_repeat_context: NotRequired[bool]
    toggling_repeat_track: NotRequired[bool]
    toggling_shuffle: NotRequired[bool]
    transferring_playback: NotRequired[bool]


class Actions:

    def __init__(self, data: ActionsData) -> None:
        self.interrupting_playback: bool = data.get("interrupting_playback", False)
        self.pausing: bool = data.get("pausing", False)
        self.resuming: bool = data.get("resuming", False)
        self.seeking: bool = data.get("seeking", False)
        self.skipping_next: bool = data.get("skipping_next", False)
        self.skipping_previous: bool = data.get("skipping_prev", False)
        self.toggling_repeat_context: bool = data.get("toggling_repeat_context", False)
        self.toggling_repeat_track: bool = data.get("toggling_repeat_track", False)
        self.toggling_shuffle: bool = data.get("toggling_shuffle", False)
        self.transferring_playback: bool = data.get("transferring_playback", False)

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}>"


class ContextData(TypedDict):
    external_urls: ExternalURLs
    href: str
    type: str
    uri: str


class Context:

    def __init__(self, data: ContextData) -> None:
        self.external_urls: ExternalURLs = data["external_urls"]
        self.href: str = data["href"]
        self.type: str = data["type"]
        self.uri: str = data["uri"]

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}>"


class PlaybackStateData(TypedDict):
    actions: ActionsData
    context: ContextData
    currently_playing_type: str
    device: DeviceData
    is_playing: bool
    item: TrackData | None
    progress_ms: int
    repeat_state: str
    shuffle_state: str
    timestamp: int


class PlaybackState:

    def __init__(self, data: PlaybackStateData) -> None:
        self.actions: Actions = Actions(data["actions"])
        self.context: Context = Context(data["context"])
        self.currently_playing_type: str = data["currently_playing_type"]
        self.device: Device = Device(data["device"])
        self.is_playing: bool = data["is_playing"]
        self.item: Track | None = Track(item) if (item := data["item"]) else None
        self.progress_ms: int = data["progress_ms"]
        self.repeat_state: str = data["repeat_state"]
        self.shuffle_state: str = data["shuffle_state"]
        self.timestamp: int = data["timestamp"]

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}>"


class CurrentlyPlayingData(TypedDict):
    context: ContextData
    currently_playing_type: str
    is_playing: bool
    item: TrackData | None
    progress_ms: int
    timestamp: int


class CurrentlyPlaying:

    def __init__(self, data: CurrentlyPlayingData) -> None:
        self.context: Context = Context(data["context"])
        self.currently_playing_type: str = data["currently_playing_type"]
        self.is_playing: bool = data["is_playing"]
        self.item: Track | None = Track(item) if (item := data["item"]) else None
        self.progress_ms: int = data["progress_ms"]
        self.timestamp: int = data["timestamp"]

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}>"
