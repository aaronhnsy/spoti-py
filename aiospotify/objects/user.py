# Future
from __future__ import annotations

# My stuff
from aiospotify import objects
from aiospotify.typings.objects import ExplicitContentSettingsData, UserData


__all__ = (
    "ExplicitContentSettings",
    "User"
)


class ExplicitContentSettings:

    def __init__(self, data: ExplicitContentSettingsData) -> None:

        self.filter_enabled = data["filter_enabled"]
        self.filter_locked = data["filter_locked"]

    def __repr__(self) -> str:
        return f"<aiospotify.ExplicitContentSettings filter_enabled={self.filter_enabled}, filter_locked={self.filter_locked}"


class User(objects.BaseObject):

    def __init__(self, data: UserData) -> None:
        super().__init__(data)

        self.country = data.get("country")
        self.display_name = data["display_name"]
        self.email = data.get("email")
        self.explicit_content_settings = ExplicitContentSettings(explicit_content) if (explicit_content := data.get("explicit_content")) else None
        self.external_urls = data["external_urls"]
        self.followers = objects.Followers(data["followers"])
        self.images = [objects.Image(image) for image in data["images"]]
        self.product = data.get("product")

    def __repr__(self) -> str:
        return f"<aiospotify.User id='{self.id}', name='{self.display_name}'>"

    #

    @property
    def url(self) -> str | None:
        return self.external_urls.get("spotify")
