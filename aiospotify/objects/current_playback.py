# Future
from __future__ import annotations

# Standard Library
from typing import Literal

# My stuff
from aiospotify.objects import Track


class Context:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.external_urls: dict[str | None, str | None] = data.get('external_urls', {})
        self.href: str = data.get('href')
        self.type: str = data.get('type')
        self.uri: str = data.get('uri')

    def __repr__(self) -> str:
        return f'<spotify.Context uri=\'{self.uri}\''

    @property
    def url(self) -> str | None:
        return self.external_urls.get('spotify', None)


class Disallows:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.interrupting_playback: bool = data.get('interrupting_playback', False)
        self.pausing: bool = data.get('pausing', False)
        self.resuming: bool = data.get('resuming', False)
        self.seeking: bool = data.get('seeking', False)
        self.skipping_next: bool = data.get('skipping_next', False)
        self.skipping_previous: bool = data.get('skipping_prev', False)
        self.toggling_repeat_context: bool = data.get('toggling_repeat_context', False)
        self.toggling_repeat_track: bool = data.get('toggling_repeat_track', False)
        self.toggling_shuffle: bool = data.get('toggling_shuffle', False)
        self.transferring_playback: bool = data.get('transferring_playback', False)

    def __repr__(self) -> str:
        return '<spotify.Disallows>'


class Device:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.id: int = data.get('id', 0)
        self.is_active: bool = data.get('is_active', False)
        self.is_private_session: bool = data.get('is_private_session', False)
        self.is_restricted: bool = data.get('is_restricted', False)
        self.name: str = data.get('name', 'unknown')
        self.type: str = data.get('type', 'unknown')
        self.volume_percent: int = data.get('volume_percent', 100)

    def __repr__(self) -> str:
        return f'<spotify.Device id=\'{self.id}\' name=\'{self.name}\'>'


class CurrentlyPlaying:

    def __init__(self, data: dict) -> None:
        self.data = data

        context = data.get('context')
        self.context: Context | None = Context(context) if context else None

        item = data.get('item')
        self.item: Track | None = Track(item) if item else None

        self.currently_playing_type: Literal['track', 'episode', 'ad', 'unknown'] = data.get('currently_playing_type', 'unknown')
        self.is_playing: bool = data.get('is_playing', True)

        self.progress: int = data.get('progress', 0)
        self.timestamp: int = data.get('timestamp', 0)

    def __repr__(self) -> str:
        return f'<spotify.CurrentlyPlaying item={self.item!r} is_playing={self.is_playing}>'


class CurrentlyPlayingContext(CurrentlyPlaying):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        actions = data.get('actions', {}).get('disallows')
        self.actions: Disallows | None = Disallows(actions) if actions else None

        device = data.get('device')
        self.device: Device | None = Device(device) if device else None

        self.repeat_state: Literal['off', 'track', 'context', 'unknown'] = data.get('repeat_state', 'unknown')
        self.shuffle_state: bool = data.get('shuffle_state', False)

    def __repr__(self) -> str:
        return f'<spotify.CurrentlyPlayingContext item={self.item!r} device={self.device} is_playing={self.is_playing}>'
