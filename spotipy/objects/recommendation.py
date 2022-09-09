from __future__ import annotations

from typing import TypedDict

from .track import Track, TrackData


__all__ = (
    "RecommendationSeedData",
    "RecommendationSeed",
    "RecommendationData",
    "Recommendation"
)


class RecommendationSeedData(TypedDict):
    initialPoolSize: int
    afterFilteringSize: int
    afterRelinkingSize: int
    id: str
    type: str
    href: str


class RecommendationSeed:

    def __init__(self, data: RecommendationSeedData) -> None:
        self.initial_pool_size = data["initialPoolSize"]
        self.after_filtering_size = data["afterFilteringSize"]
        self.after_relinking_size = data["afterRelinkingSize"]
        self.href = data["href"]
        self.id = data["id"]
        self.type = data["type"]

    def __repr__(self) -> str:
        return f"<spotipy.RecommendationSeed id='{self.id}', type='{self.type}'>"


class RecommendationData(TypedDict):
    tracks: list[TrackData]
    seeds: list[RecommendationSeedData]


class Recommendation:

    def __init__(self, data: RecommendationData) -> None:
        self.tracks = [Track(data) for data in data["tracks"]]
        self.seeds = [RecommendationSeed(data) for data in data["seeds"]]

    def __repr__(self) -> str:
        return f"<spotipy.Recommendation tracks={len(self.tracks)}, seeds={len(self.seeds)}>"
