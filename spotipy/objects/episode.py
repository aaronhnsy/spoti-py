from __future__ import annotations

from typing import TypedDict

from .base import BaseObject, BaseObjectData
from .common import ExternalUrlsData
from .image import Image, ImageData
from .show import ShowData, Show


__all__ = (
    "EpisodeRestrictionData",
    "EpisodeRestriction",
    "EpisodeResumePointData",
    "EpisodeResumePoint",
    "SimpleEpisodeData",
    "SimpleEpisode",
    "EpisodeData",
    "Episode",
)


class EpisodeRestrictionData(TypedDict):
    reason: str


class EpisodeRestriction:

    def __init__(self, data: EpisodeRestrictionData) -> None:
        self.reason = data["reason"]

    def __repr__(self) -> str:
        return f"<spotipy.EpisodeRestriction reason='{self.reason}'>"


class EpisodeResumePointData(TypedDict):
    fully_played: bool
    resume_position_ms: int


class EpisodeResumePoint:

    def __init__(self, data: EpisodeResumePointData) -> None:
        self.fully_played = data["fully_played"]
        self.resume_position_ms = data["resume_position_ms"]

    def __repr__(self) -> str:
        return f"<spotipy.EpisodeResumePoint fully_played={self.fully_played} resume_position_ms=" \
               f"{self.resume_position_ms}>"


class SimpleEpisodeData(BaseObjectData):
    audio_preview_url: str | None
    description: str
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrlsData
    html_description: str
    images: list[ImageData]
    is_externally_hosted: bool
    is_playable: bool
    languages: list[str]
    release_date: str
    release_date_precision: str
    restrictions: EpisodeRestrictionData
    resume_point: EpisodeResumePointData


class SimpleEpisode(BaseObject):

    def __init__(self, data: SimpleEpisodeData) -> None:
        super().__init__(data)

        self.audio_preview_url = data["audio_preview_url"]
        self.description = data["description"]
        self.duration_ms = data["duration_ms"]
        self.explicit = data["explicit"]
        self.external_urls = data["external_urls"]
        self.html_description = data["html_description"]
        self.images = [Image(image) for image in data["images"]]
        self.is_externally_hosted = data["is_externally_hosted"]
        self.is_playable = data["is_playable"]
        self.languages = data["languages"]
        self.release_date = data["release_date"]
        self.release_date_precision = data["release_date_precision"]
        self.restriction = EpisodeRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.resume_point = EpisodeResumePoint(resume_point) if (resume_point := data.get("resume_point")) else None

    def __repr__(self) -> str:
        return f"<spotipy.SimpleEpisode id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class EpisodeData(BaseObjectData):
    audio_preview_url: str | None
    description: str
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrlsData
    html_description: str
    images: list[ImageData]
    is_externally_hosted: bool
    is_playable: bool
    languages: list[str]
    release_date: str
    release_date_precision: str
    restrictions: EpisodeRestrictionData
    resume_point: EpisodeResumePointData
    show: ShowData


class Episode(BaseObject):

    def __init__(self, data: EpisodeData) -> None:
        super().__init__(data)

        self.audio_preview_url = data["audio_preview_url"]
        self.description = data["description"]
        self.duration_ms = data["duration_ms"]
        self.explicit = data["explicit"]
        self.external_urls = data["external_urls"]
        self.html_description = data["html_description"]
        self.images = [Image(image) for image in data["images"]]
        self.is_externally_hosted = data["is_externally_hosted"]
        self.is_playable = data["is_playable"]
        self.languages = data["languages"]
        self.release_date = data["release_date"]
        self.release_date_precision = data["release_date_precision"]
        self.show = Show(data["show"])
        self.restriction = EpisodeRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.resume_point = EpisodeResumePoint(resume_point) if (resume_point := data.get("resume_point")) else None

    def __repr__(self) -> str:
        return f"<spotipy.Episode id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
