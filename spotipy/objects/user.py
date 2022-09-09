from __future__ import annotations

from typing import TypedDict

from .base import BaseObject, BaseObjectData
from .common import ExternalUrlsData
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
        self.filter_enabled = data["filter_enabled"]
        self.filter_locked = data["filter_locked"]

    def __repr__(self) -> str:
        return f"<spotipy.ExplicitContentSettings filter_enabled={self.filter_enabled}, filter_locked=" \
               f"{self.filter_locked}"


class UserData(BaseObjectData):
    country: str
    display_name: str
    email: str
    explicit_content: ExplicitContentSettingsData
    external_urls: ExternalUrlsData
    followers: FollowersData
    images: list[ImageData]
    product: str


class User(BaseObject):

    def __init__(self, data: UserData) -> None:
        super().__init__(data)

        self.country = data.get("country")
        self.display_name = data.get("display_name")
        self.email = data.get("email")
        self.explicit_content_settings = ExplicitContentSettings(explicit_content) if (
            explicit_content := data.get("explicit_content")) else None
        self.external_urls = data["external_urls"]
        self.followers = Followers(followers) if (followers := data.get("followers")) else None
        self.images = [Image(image) for image in images] if (images := data.get("images")) else None
        self.product = data.get("product")

    def __repr__(self) -> str:
        return f"<spotipy.User id='{self.id}', name='{self.display_name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
