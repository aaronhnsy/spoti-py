from __future__ import annotations

from typing import TypedDict


__all__ = (
    "ActionsData",
    "Actions",
)


class ActionsData(TypedDict):
    interrupting_playback: bool
    pausing: bool
    resuming: bool
    seeking: bool
    skipping_next: bool
    skipping_prev: bool
    toggling_repeat_context: bool
    toggling_repeat_track: bool
    toggling_shuffle: bool
    transferring_playback: bool


class Actions:

    def __init__(self, data: ActionsData) -> None:
        self.interrupting_playback = data.get("interrupting_playback", False)
        self.pausing = data.get("pausing", False)
        self.resuming = data.get("resuming", False)
        self.seeking = data.get("seeking", False)
        self.skipping_next = data.get("skipping_next", False)
        self.skipping_previous = data.get("skipping_prev", False)
        self.toggling_repeat_context = data.get("toggling_repeat_context", False)
        self.toggling_repeat_track = data.get("toggling_repeat_track", False)
        self.toggling_shuffle = data.get("toggling_shuffle", False)
        self.transferring_playback = data.get("transferring_playback", False)

    def __repr__(self) -> str:
        return "<spotipy.Actions>"
