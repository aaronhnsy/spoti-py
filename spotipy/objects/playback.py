from __future__ import annotations

from typing import TypedDict

from .actions import ActionsData, Actions
from .common import ExternalUrlsData
from .device import Device, DeviceData
from .track import Track, TrackData


__all__ = (
    "ContextData",
    "Context",
    "PlaybackStateData",
    "PlaybackState",
    "CurrentlyPlayingData",
    "CurrentlyPlaying",
)


class ContextData(TypedDict):
    external_urls: ExternalUrlsData
    href: str
    type: str
    uri: str


class Context:

    def __init__(self, data: ContextData) -> None:
        self.external_urls = data["external_urls"]
        self.href = data["href"]
        self.type = data["type"]
        self.uri = data["uri"]

    def __repr__(self) -> str:
        return "<spotipy.Context"


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
        self.actions = Actions(data["actions"])
        self.context = Context(data["context"])
        self.currently_playing_type = data["currently_playing_type"]
        self.device = Device(data["device"])
        self.is_playing = data["is_playing"]
        self.item = Track(item) if (item := data["item"]) else None
        self.progress_ms = data["progress_ms"]
        self.repeat_state = data["repeat_state"]
        self.shuffle_state = data["shuffle_state"]
        self.timestamp: int = data["timestamp"]

    def __repr__(self) -> str:
        return "<spotipy.CurrentlyPlayingContext>"


class CurrentlyPlayingData(TypedDict):
    context: ContextData
    currently_playing_type: str
    is_playing: bool
    item: TrackData | None
    progress_ms: int
    timestamp: int


class CurrentlyPlaying:

    def __init__(self, data: CurrentlyPlayingData) -> None:
        self.context = Context(data["context"])
        self.currently_playing_type = data["currently_playing_type"]
        self.is_playing = data["is_playing"]
        self.item = Track(item) if (item := data["item"]) else None
        self.progress_ms = data["progress_ms"]
        self.timestamp: int = data["timestamp"]

    def __repr__(self) -> str:
        return "<spotipy.CurrentlyPlaying>"
