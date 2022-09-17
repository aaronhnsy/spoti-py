from __future__ import annotations

import enum


__all__ = (
    "IncludeGroup",
    "SearchType",
    "RepeatMode",
    "TimeRange",
)


class IncludeGroup(enum.Enum):
    ALBUM = "album"
    SINGLE = "single"
    APPEARS_ON = "appears_on"
    COMPILATION = "compilation"
    ALL = f"{ALBUM},{SINGLE},{APPEARS_ON},{COMPILATION}"


class SearchType(enum.Enum):
    ALBUM = "album"
    ARTIST = "artist"
    PLAYLIST = "playlist"
    TRACK = "track"
    SHOW = "show"
    EPISODE = "episode"
    All = f"{ALBUM},{ARTIST},{PLAYLIST},{TRACK},{SHOW},{EPISODE}"


class RepeatMode(enum.Enum):
    TRACK = "track"
    CONTEXT = "context"
    OFF = "off"


class TimeRange(enum.Enum):
    LONG_TERM = "long_term"
    MEDIUM_TERM = "medium_term"
    SHORT_TERM = "short_term"
