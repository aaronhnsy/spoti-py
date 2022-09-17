from __future__ import annotations

import enum
from typing import Any


__all__ = (
    "ExternalURLs",
    "ExternalIDs",
    "ReleaseDatePrecision"
)

ExternalURLs = dict[str, Any]
ExternalIDs = dict[str, Any]


class ReleaseDatePrecision(enum.Enum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
