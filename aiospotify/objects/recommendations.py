# Future
from __future__ import annotations

# My stuff
from aiospotify import objects


__all__ = (
    "RecommendationSeed",
    "Recommendation"
)


class RecommendationSeed:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.tracks_after_filters = data.get("afterFilteringSize", 0)
        self.tracks_after_relinking = data.get("afterRelinkingSize", 0)
        self.href = data.get("href")
        self.id = data.get("id")
        self.initial_pool_size = data.get("initialPoolSize", 0)
        self.type = data.get("type")

    def __repr__(self) -> str:
        return f"<spotify.RecommendationSeed id=\"{self.id}\">"


class Recommendation:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.seeds = [objects.RecommendationSeed(data) for data in data.get("seeds", [])]
        self.tracks = [objects.Track(data) for data in data.get("tracks", [])]

    def __repr__(self) -> str:
        return f"<spotify.Recommendation tracks={len(self.tracks)} seeds={len(self.seeds)}>"
