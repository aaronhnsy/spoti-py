# Future
from __future__ import annotations

# My stuff
from aiospotify import objects
from aiospotify.typings.objects import RecommendationData, RecommendationSeedData


__all__ = (
    "RecommendationSeed",
    "Recommendation"
)


class RecommendationSeed:

    def __init__(self, data: RecommendationSeedData) -> None:

        self.initial_pool_size = data["initialPoolSize"]
        self.after_filtering_size = data["afterFilteringSize"]
        self.after_relinking_size = data["afterRelinkingSize"]
        self.href = data["href"]
        self.id = data["id"]
        self.type = data["type"]

    def __repr__(self) -> str:
        return f"<aiospotify.RecommendationSeed id='{self.id}', type='{self.type}'>"


class Recommendation:

    def __init__(self, data: RecommendationData) -> None:

        self.tracks = [objects.Track(data) for data in data["tracks"]]
        self.seeds = [objects.RecommendationSeed(data) for data in data["seeds"]]

    def __repr__(self) -> str:
        return f"<aiospotify.Recommendation tracks={len(self.tracks)}, seeds={len(self.seeds)}>"
