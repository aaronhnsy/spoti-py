# Future
from __future__ import annotations

# Standard Library
from typing import Any, Literal

# My stuff
from spotipy.typings.objects import *


HTTPMethod = Literal["GET", "POST", "DELETE", "PATCH", "PUT"]
Parameters = dict[str, Any]
Data = dict[str, Any]
