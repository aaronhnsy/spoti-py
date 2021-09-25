# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING


if TYPE_CHECKING:

    # My stuff
    from aiospotify import objects

    Credentials = objects.ClientCredentials | objects.UserCredentials
    OptionalCredentials = objects.ClientCredentials | objects.UserCredentials | None
