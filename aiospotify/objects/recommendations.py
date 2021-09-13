
# Future
from __future__ import annotations

# My stuff
from aiospotify import objects


VALID_KWARGS = [
    'min_acousticness',
    'max_acousticness',
    'target_acousticness',
    'min_danceability',
    'max_danceability',
    'target_danceability',
    'min_duration_ms',
    'max_duration_ms',
    'target_duration_ms',
    'min_energy',
    'max_energy',
    'target_energy',
    'min_instrumentalness',
    'max_instrumentalness',
    'target_instrumentalness',
    'min_key',
    'max_key',
    'target_key',
    'min_liveness',
    'max_liveness',
    'target_liveness',
    'min_loudness',
    'max_loudness',
    'target_loudness',
    'min_mode',
    'max_mode',
    'target_mode',
    'min_popularity',
    'max_popularity',
    'target_popularity',
    'min_speechiness',
    'max_speechiness',
    'target_speechiness',
    'min_tempo',
    'max_tempo',
    'target_tempo',
    'min_time_signature',
    'max_time_signature',
    'target_time_signature',
    'min_valence',
    'max_valence',
    'target_valence'
]


class Seed:

    def __init__(self, *, artist_ids: list[str] = None, genres: list[str] = None, track_ids: list[str] = None, **kwargs) -> None:

        self.parameters = {}

        seeds = [seed for seeds in [artist_ids or [], genres or [], track_ids or []] for seed in seeds]

        if len(seeds) > 5:
            raise ValueError('Too many seed values provided.')

        if artist_ids:
            self.parameters['seed_artists'] = ','.join(artist_ids)
        if genres:
            self.parameters['seed_genres'] = ','.join(genres)
        if track_ids:
            self.parameters['seed_tracks'] = ','.join(track_ids)

        for kwarg, value in kwargs.items():
            if kwarg not in VALID_KWARGS:
                raise ValueError(f'\'{kwarg}\' was not a valid kwarg.')
            self.parameters[kwarg] = value

    def __repr__(self) -> str:
        return f'<spotify.RecommendationSeed parameters={self.parameters}>'


class RecommendationSeed:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.tracks_after_filters = data.get('afterFilteringSize', 0)
        self.tracks_after_relinking = data.get('afterRelinkingSize', 0)
        self.href = data.get('href')
        self.id = data.get('id')
        self.initial_pool_size = data.get('initialPoolSize', 0)
        self.type = data.get('type')

    def __repr__(self) -> str:
        return f'<spotify.RecommendationSeed id=\'{self.id}\'>'


class Recommendation:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.seeds = [objects.RecommendationSeed(data) for data in data.get('seeds', [])]
        self.tracks = [objects.Track(data) for data in data.get('tracks', [])]

    def __repr__(self) -> str:
        return f'<spotify.Recommendation tracks={len(self.tracks)} seeds={len(self.seeds)}>'
