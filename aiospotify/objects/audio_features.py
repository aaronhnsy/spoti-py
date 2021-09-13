# Future
from __future__ import annotations

# My stuff
from aiospotify import objects


__all__ = (
    "AudioFeatures",
)


class AudioFeatures:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.acousticness: float = data.get("acousticness", 0)
        self.analysis_url: str | None = data.get("analysis_url")
        self.danceability: float = data.get("danceability", 0)
        self.duration_ms: int = data.get("duration_ms", 0)
        self.energy: float = data.get("energy", 0)
        self.id: str | None = data.get("id")
        self.instrumentalness: float = data.get("instrumentalness", 0)
        self.key: objects.Key = objects.Key(data.get("key", 0))
        self.liveness: float = data.get("liveness", 0)
        self.loudness: float = data.get("loudness", 0)
        self.mode: objects.Mode = objects.Mode(data.get("mode", 0))
        self.speechiness: float = data.get("speechiness", 0)
        self.tempo: float = data.get("tempo", 0)
        self.time_signature: int = data.get("time_signature", 0)
        self.track_href: str | None = data.get("track_href")
        self.type: str = data.get("type", "audio_features")
        self.uri: str | None = data.get("uri")
        self.valence: float = data.get("valence", 0)

    def __repr__(self) -> str:
        return f"<spotify.AudioFeatures id=\"{self.id}\">"
