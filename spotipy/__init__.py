from __future__ import annotations

import logging
from typing import Final, Literal, NamedTuple

from .client import *
from .errors import *
from .http import *
from .objects import *
from .utilities import *
from .values import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: Final[VersionInfo] = VersionInfo(major=0, minor=2, micro=0, releaselevel="final", serial=0)

__title__: Final[str] = "spotipy"
__author__: Final[str] = "Axelancerr"
__copyright__: Final[str] = "Copyright 2021-present Axelancerr"
__license__: Final[str] = "MIT"
__version__: Final[str] = "0.2.0"
__maintainer__: Final[str] = "Aaron Hennessey"
__source__: Final[str] = "https://github.com/Axelware/spoti-py"

logging.getLogger("spotipy")
