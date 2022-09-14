from __future__ import annotations

import enum
from typing import TypedDict, Literal

from .track import Track, TrackData


__all__ = (
    "RecommendationSeedType",
    "RecommendationsSeedData",
    "RecommendationsSeed",
    "RecommendationsData",
    "Recommendations"
)


class RecommendationSeedType(enum.Enum):
    ARTIST = "ARTIST"
    TRACK = "TRACK"
    GENRE = "GENRE"


class RecommendationsSeedData(TypedDict):
    initialPoolSize: int
    afterFilteringSize: int
    afterRelinkingSize: int
    href: str | None
    id: str
    type: Literal["ARTIST", "TRACK", "GENRE"]


class RecommendationsSeed:

    def __init__(self, data: RecommendationsSeedData) -> None:
        self.initial_pool_size: int = data["initialPoolSize"]
        self.after_filtering_size: int = data["afterFilteringSize"]
        self.after_relinking_size: int = data["afterRelinkingSize"]
        self.href: str | None = data["href"]
        self.id: str = data["id"]
        self.type: RecommendationSeedType = RecommendationSeedType(data["type"])

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: id='{self.id}', type={self.type}>"


class RecommendationsData(TypedDict):
    tracks: list[TrackData]
    seeds: list[RecommendationsSeedData]


class Recommendations:

    def __init__(self, data: RecommendationsData) -> None:
        self.tracks: list[Track] = [Track(data) for data in data["tracks"]]
        self.seeds: list[RecommendationsSeed] = [RecommendationsSeed(data) for data in data["seeds"]]

    def __repr__(self) -> str:
        return f"<spotipy.{self.__class__.__name__}: tracks={len(self.tracks)}, seeds={len(self.seeds)}>"
