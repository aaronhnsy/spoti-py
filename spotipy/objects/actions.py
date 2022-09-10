from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired


__all__ = (
    "ActionsData",
    "Actions",
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
        return "<spotipy.Actions>"
