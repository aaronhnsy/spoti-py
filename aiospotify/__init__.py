# Future
from __future__ import annotations

# Standard Library
import logging
from typing import Final, Literal, NamedTuple

# My stuff
from .client import *
from .exceptions import *
from .objects import *
from .utils import *
from .values import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: Final[VersionInfo] = VersionInfo(major=2021, minor=9, micro=18, releaselevel="final", serial=0)

__title__: Final[str] = "aiospotify"
__author__: Final[str] = "Axelancerr"
__copyright__: Final[str] = "Copyright 2021-present Axelancerr"
__license__: Final[str] = "MIT"
__version__: Final[str] = "2021.09.18"
__maintainer__: Final[str] = "Aaron Hennessey"
__source__: Final[str] = "https://github.com/Axelancerr/aiospotify"

logging.getLogger("aiospotify")
