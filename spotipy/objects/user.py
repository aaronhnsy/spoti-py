from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired

from .base import BaseObject, BaseObjectData
from .common import ExternalURLs
from .followers import Followers, FollowersData
from .image import Image, ImageData


__all__ = (
    "ExplicitContentSettingsData",
    "ExplicitContentSettings",
    "UserData",
    "User"
)


class ExplicitContentSettingsData(TypedDict):
    filter_enabled: bool
    filter_locked: bool


class ExplicitContentSettings:

    def __init__(self, data: ExplicitContentSettingsData) -> None:
        self.filter_enabled: bool = data["filter_enabled"]
        self.filter_locked: bool = data["filter_locked"]

    def __repr__(self) -> str:
        return f"<spotipy.ExplicitContentSettings filter_enabled={self.filter_enabled}, filter_locked=" \
               f"{self.filter_locked}"


class UserData(BaseObjectData):
    country: NotRequired[str]
    display_name: str
    email: NotRequired[str]
    explicit_content: NotRequired[ExplicitContentSettingsData]
    external_urls: ExternalURLs
    followers: NotRequired[FollowersData]
    images: NotRequired[list[ImageData]]
    product: NotRequired[str]


class User(BaseObject):

    def __init__(self, data: UserData) -> None:
        super().__init__(data)

        self.country: str | None = data.get("country")
        self.display_name: str | None = data["display_name"]
        self.email: str | None = data.get("email")
        self.explicit_content_settings: ExplicitContentSettings | None = ExplicitContentSettings(explicit_content) if (explicit_content := data.get("explicit_content")) else None
        self.external_urls: ExternalURLs = data["external_urls"]
        self.followers: Followers | None = Followers(followers) if (followers := data.get("followers")) else None
        self.images: list[Image] | None = [Image(image) for image in images] if (images := data.get("images")) else None
        self.product: str | None = data.get("product")

    def __repr__(self) -> str:
        return f"<spotipy.User id='{self.id}', name='{self.display_name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
