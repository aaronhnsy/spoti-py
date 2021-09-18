
# Future
from __future__ import annotations

# My stuff
from typings.objects import DisallowsData


__all__ = (
    "Disallows",
)


class Disallows:

    def __init__(self, data: DisallowsData) -> None:

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
        return "<aiospotify.Disallows>"
