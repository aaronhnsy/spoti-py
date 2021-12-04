# Future
from __future__ import annotations

# My stuff
from spotipy import objects
from spotipy.typings.objects import EpisodeData, EpisodeRestrictionData, EpisodeResumePointData, SimpleEpisodeData


__all__ = (
    "EpisodeRestriction",
    "EpisodeResumePoint",
    "SimpleEpisode",
    "Episode",
)


class EpisodeRestriction:

    def __init__(self, data: EpisodeRestrictionData) -> None:
        self.reason = data["reason"]

    def __repr__(self) -> str:
        return f"<spotipy.EpisodeRestriction reason='{self.reason}'>"


class EpisodeResumePoint:

    def __init__(self, data: EpisodeResumePointData) -> None:
        self.fully_played = data["fully_played"]
        self.resume_position_ms = data["resume_position_ms"]

    def __repr__(self) -> str:
        return f"<spotipy.EpisodeResumePoint fully_played={self.fully_played} resume_position_ms={self.resume_position_ms}>"


class SimpleEpisode(objects.BaseObject):

    def __init__(self, data: SimpleEpisodeData) -> None:
        super().__init__(data)

        self.audio_preview_url = data["audio_preview_url"]
        self.description = data["description"]
        self.duration_ms = data["duration_ms"]
        self.explicit = data["explicit"]
        self.external_urls = data["external_urls"]
        self.html_description = data["html_description"]
        self.images = [objects.Image(image) for image in data["images"]]
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


class Episode(objects.BaseObject):

    def __init__(self, data: EpisodeData) -> None:
        super().__init__(data)

        self.audio_preview_url = data["audio_preview_url"]
        self.description = data["description"]
        self.duration_ms = data["duration_ms"]
        self.explicit = data["explicit"]
        self.external_urls = data["external_urls"]
        self.html_description = data["html_description"]
        self.images = [objects.Image(image) for image in data["images"]]
        self.is_externally_hosted = data["is_externally_hosted"]
        self.is_playable = data["is_playable"]
        self.languages = data["languages"]
        self.release_date = data["release_date"]
        self.release_date_precision = data["release_date_precision"]
        self.show = objects.Show(data["show"])
        self.restriction = EpisodeRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.resume_point = EpisodeResumePoint(resume_point) if (resume_point := data.get("resume_point")) else None

    def __repr__(self) -> str:
        return f"<spotipy.Episode id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
