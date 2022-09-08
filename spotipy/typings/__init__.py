from __future__ import annotations

from typing import Any, Literal

from spotipy.typings.objects import *


HTTPMethod = Literal["GET", "POST", "DELETE", "PATCH", "PUT"]
Parameters = dict[str, Any]
Data = dict[str, Any]
