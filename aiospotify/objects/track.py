# Future
from __future__ import annotations

# My stuff
from aiospotify.objects import album, artist, base, enums, user
from typings.objects import AudioFeaturesData, PlaylistTrackData, SimpleTrackData, TrackData, TrackRestrictionData


__all__ = (
    "AudioFeatures",
    "TrackRestriction",
    "SimpleTrack",
    "Track",
    "PlaylistTrack",
)


class AudioFeatures:

    def __init__(self, data: AudioFeaturesData) -> None:

        self.acousticness = data["acousticness"]
        self.analysis_url = data["analysis_url"]
        self.danceability = data["danceability"]
        self.duration_ms = data["duration_ms"]
        self.energy = data["energy"]
        self.id = data["id"]
        self.instrumentalness = data["instrumentalness"]
        self.key = enums.Key(data["key"])
        self.liveness = data["liveness"]
        self.loudness = data["loudness"]
        self.mode = enums.Mode(data["mode"])
        self.speechiness = data["speechiness"]
        self.tempo = data["tempo"]
        self.time_signature = data["time_signature"]
        self.track_href = data["track_href"]
        self.type = data["type"]
        self.uri = data["uri"]
        self.valence = data["valence"]

    def __repr__(self) -> str:
        return f"<aiospotify.AudioFeatures id='{self.id}'>"


class TrackRestriction:

    def __init__(self, data: TrackRestrictionData) -> None:

        self.reason = data["reason"]

    def __repr__(self) -> str:
        return f"<aiospotify.TrackRestriction reason='{self.reason}'>"


class SimpleTrack(base.BaseObject):

    def __init__(self, data: SimpleTrackData) -> None:
        super().__init__(data)

        self.artists = [artist.SimpleArtist(artist_data) for artist_data in data["artists"]]
        self.available_markets = data["available_markets"]
        self.disc_number = data["disc_number"]
        self.duration_ms = data["duration_ms"]
        self.explicit = data["explicit"]
        self.external_urls = data["external_urls"]
        self.is_local = data["is_local"]
        self.preview_url = data["preview_url"]
        self.restriction = TrackRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.track_number = data["track_number"]

    def __repr__(self) -> str:
        return f"<aiospotify.SimpleTrack id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class Track(base.BaseObject):

    def __init__(self, data: TrackData) -> None:
        super().__init__(data)

        self.album = album.SimpleAlbum(data["album"])
        self.artists = [artist.SimpleArtist(artist_data) for artist_data in data["artists"]]
        self.available_markets = data.get("available_markets")
        self.disc_number = data["disc_number"]
        self.duration_ms = data["duration_ms"]
        self.explicit = data["explicit"]
        self.external_ids = data["external_ids"]
        self.external_urls = data["external_urls"]
        self.is_local = data["is_local"]
        self.popularity = data["popularity"]
        self.preview_url = data["preview_url"]
        self.restriction = TrackRestriction(restriction) if (restriction := data.get("restrictions")) else None
        self.track_number = data["track_number"]

    def __repr__(self) -> str:
        return f"<aiospotify.Track id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")


class PlaylistTrack(base.BaseObject):

    def __init__(self, data: PlaylistTrackData) -> None:
        super().__init__(data)

        self.added_at = data["added_at"]
        self.added_by = user.User(data["added_by"])
        self.is_local = data["is_local"]
        self.primary_colour = data["primary_color"]
        self.video_thumbnail = data["video_thumbnail"]["url"]

        track = data["track"]
        self.album = album.SimpleAlbum(track["album"])
        self.artists = [artist.SimpleArtist(artist_data) for artist_data in track["artists"]]
        self.available_markets = track["available_markets"]
        self.disc_number = track["disc_number"]
        self.duration_ms = track["duration_ms"]
        self.explicit = track["explicit"]
        self.external_ids = track["external_ids"]
        self.external_urls = track["external_urls"]
        self.is_local = track["is_local"]
        self.popularity = track["popularity"]
        self.preview_url = track["preview_url"]
        self.restriction = TrackRestriction(restriction) if (restriction := track.get("restrictions")) else None
        self.track_number = track["track_number"]

    def __repr__(self) -> str:
        return f"<aiospotify.PlaylistTrack id='{self.id}', name='{self.name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
