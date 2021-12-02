# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING


if TYPE_CHECKING:

    # My stuff
    from aiospotify.objects.token import ClientCredentials, UserCredentials

    Credentials = ClientCredentials | UserCredentials
    OptionalCredentials = ClientCredentials | UserCredentials | None
