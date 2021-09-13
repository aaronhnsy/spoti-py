# Future
from __future__ import annotations

# My stuff
from aiospotify import exceptions


API_BASE = "https://api.spotify.com"
ACCOUNTS_BASE = "https://accounts.spotify.com"


EXCEPTION_MAPPING = {
    400: exceptions.BadRequest,
    401: exceptions.Unauthorized,
    403: exceptions.Forbidden,
    404: exceptions.NotFound,
    429: exceptions.TooManyRequests,
    500: exceptions.InternalServerError,
    502: exceptions.BadGatewayError,
    503: exceptions.ServiceUnavailable
}


SCOPES = [
    "ugc-image-upload",

    "playlist-modify-private",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-read-collaborative",

    "user-read-private",
    "user-read-email",

    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",

    "user-library-modify",
    "user-library-read",

    "user-read-playback-position",
    "user-read-recently-played",
    "user-top-read",

    "app-remote-control",
    "streaming",

    "user-follow-modify",
    "user-follow-read",
]
