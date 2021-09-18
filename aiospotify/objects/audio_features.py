# Future
from __future__ import annotations

# My stuff
from aiospotify import objects
from typings.objects import AudioFeaturesData


__all__ = (
    "AudioFeatures",
)


class AudioFeatures:

    def __init__(self, data: AudioFeaturesData) -> None:

        self.acousticness: float = data["acousticness"]
        self.analysis_url: str = data["analysis_url"]
        self.danceability: float = data["danceability"]
        self.duration_ms: int = data["duration_ms"]
        self.energy: float = data["energy"]
        self.id: str | None = data["id"]
        self.instrumentalness: float = data["instrumentalness"]
        self.key: objects.Key = objects.Key(data.get("key", 0))
        self.liveness: float = data["liveness"]
        self.loudness: float = data["loudness"]
        self.mode: objects.Mode = objects.Mode(data.get("mode", 0))
        self.speechiness: float = data["speechiness"]
        self.tempo: float = data["tempo"]
        self.time_signature: int = data["time_signature"]
        self.track_href: str = data["track_href"]
        self.type: str = data["type"]
        self.uri: str = data["uri"]
        self.valence: float = data["valence"]

    def __repr__(self) -> str:
        return f"<aiospotify.AudioFeatures id='{self.id}'>"
