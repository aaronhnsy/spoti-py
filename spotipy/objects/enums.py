# Future
from __future__ import annotations

# Standard Library
import enum


__all__ = (
    "IncludeGroup",
    "Key",
    "Mode",
    "SearchType",
    "CopyrightType",
    "RepeatMode",
    "TimeRange"
)


class IncludeGroup(enum.Enum):
    ALBUM = "album"
    SINGLE = "single"
    APPEARS_ON = "appears_on"
    COMPILATION = "compilation"
    ALL = "album,single,appears_on,compilation"


class Key(enum.Enum):
    C = 0
    C_SHARP = 1
    D = 2
    D_SHARP = 3
    E = 4
    F = 5
    F_SHARP = 6
    G = 7
    G_SHARP = 8
    A = 9
    A_SHARP = 10
    B = 11


class Mode(enum.Enum):
    MAJOR = 1
    MINOR = 0


class SearchType(enum.Enum):
    ALBUM = "album"
    ARTIST = "artist"
    PLAYLIST = "playlist"
    TRACK = "track"
    SHOW = "show"
    EPISODE = "episode"
    ALL = "album,artist,playlist,track,show,episode"


class CopyrightType(enum.Enum):
    NORMAL = "C"
    PERFORMANCE = "P"


class RepeatMode(enum.Enum):
    TRACK = "track"
    CONTEXT = "context"
    OFF = "off"


class TimeRange(enum.Enum):
    LONG_TERM = "long_term"
    MEDIUM_TERM = "medium_term"
    SHORT_TERM = "short_term"
