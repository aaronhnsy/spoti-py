# Future
from __future__ import annotations

# My stuff
from aiospotify import exceptions


__all__ = (
    "EXCEPTION_MAPPING",
    "SCOPES",
    "VALID_SEED_KWARGS",
)


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

VALID_SEED_KWARGS = [
    "min_acousticness",
    "max_acousticness",
    "target_acousticness",
    "min_danceability",
    "max_danceability",
    "target_danceability",
    "min_duration_ms",
    "max_duration_ms",
    "target_duration_ms",
    "min_energy",
    "max_energy",
    "target_energy",
    "min_instrumentalness",
    "max_instrumentalness",
    "target_instrumentalness",
    "min_key",
    "max_key",
    "target_key",
    "min_liveness",
    "max_liveness",
    "target_liveness",
    "min_loudness",
    "max_loudness",
    "target_loudness",
    "min_mode",
    "max_mode",
    "target_mode",
    "min_popularity",
    "max_popularity",
    "target_popularity",
    "min_speechiness",
    "max_speechiness",
    "target_speechiness",
    "min_tempo",
    "max_tempo",
    "target_tempo",
    "min_time_signature",
    "max_time_signature",
    "target_time_signature",
    "min_valence",
    "max_valence",
    "target_valence"
]
