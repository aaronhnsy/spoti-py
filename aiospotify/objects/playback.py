# Future
from __future__ import annotations

# My stuff
from aiospotify import objects
from aiospotify.typings.objects import ContextData, CurrentlyPlayingData, PlaybackStateData


__all__ = (
    "Context",
    "PlaybackState",
    "CurrentlyPlaying",
)


class Context:

    def __init__(self, data: ContextData) -> None:

        self.external_urls = data["external_urls"]
        self.href = data["href"]
        self.type = data["type"]
        self.uri = data["uri"]

    def __repr__(self) -> str:
        return "<aiospotify.Context"


class PlaybackState:

    def __init__(self, data: PlaybackStateData) -> None:

        self.actions = objects.Actions(data["actions"])
        self.context = Context(data["context"])
        self.currently_playing_type = data["currently_playing_type"]
        self.device = objects.Device(data["device"])
        self.is_playing = data["is_playing"]
        self.item = objects.Track(item) if (item := data["item"]) else None
        self.progress_ms = data["progress_ms"]
        self.repeat_state = data["repeat_state"]
        self.shuffle_state = data["shuffle_state"]
        self.timestamp: int = data["timestamp"]

    def __repr__(self) -> str:
        return "<aiospotify.CurrentlyPlayingContext>"


class CurrentlyPlaying:

    def __init__(self, data: CurrentlyPlayingData) -> None:

        self.context = Context(data["context"])
        self.currently_playing_type = data["currently_playing_type"]
        self.is_playing = data["is_playing"]
        self.item = objects.Track(item) if (item := data["item"]) else None
        self.progress_ms = data["progress_ms"]
        self.timestamp: int = data["timestamp"]

    def __repr__(self) -> str:
        return "<aiospotify.CurrentlyPlaying>"
