from __future__ import annotations

import enum


__all__ = (
    "IncludeGroup",
    "Key",
    "Mode",
    "SearchType",
    "CopyrightType",
    "RepeatMode",
    "TimeRange",
    "ReleaseDatePrecision"
)


class IncludeGroup(enum.Enum):
    Album = "album"
    Single = "single"
    AppearsOn = "appears_on"
    Compilation = "compilation"
    All = f"{Album},{Single},{AppearsOn},{Compilation}"


class Key(enum.Enum):
    C = 0
    C_Sharp = 1
    D = 2
    D_Sharp = 3
    E = 4
    F = 5
    F_Sharp = 6
    G = 7
    G_Sharp = 8
    A = 9
    A_Sharp = 10
    B = 11


class Mode(enum.Enum):
    Major = 1
    Minor = 0


class SearchType(enum.Enum):
    Album = "album"
    Artist = "artist"
    Playlist = "playlist"
    Track = "track"
    Show = "show"
    Episode = "episode"
    All = f"{Album},{Artist},{Playlist},{Track},{Show},{Episode}"


class CopyrightType(enum.Enum):
    Normal = "C"
    Performance = "P"


class RepeatMode(enum.Enum):
    Track = "track"
    Context = "context"
    Off = "off"


class TimeRange(enum.Enum):
    LongTerm = "long_term"
    MediumTerm = "medium_term"
    ShortTerm = "short_term"


class ReleaseDatePrecision(enum.Enum):
    Year = "year"
    Month = "month"
    Day = "day"
