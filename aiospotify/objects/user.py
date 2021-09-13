# Future
from __future__ import annotations

# My stuff
from aiospotify import objects


__all__ = (
    "ExplicitContentSettings",
    "User"
)


class ExplicitContentSettings:

    def __init__(self, data: dict) -> None:
        self.data = data

        self.filter_enabled = data.get("filter_enabled")
        self.filter_locked = data.get("filter_locked")

    def __repr__(self) -> str:
        return f"<spotify.ExplicitContentSettings filter_enabled={self.filter_enabled} filter_locked={self.filter_locked}"


class User(objects.BaseObject):

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.country: str | None = data.get("country")
        self.name: str | None = data.get("display_name")
        self.email: str | None = data.get("email")
        self.explicit_content_settings: ExplicitContentSettings | None = ExplicitContentSettings(data.get("explicit_content")) if data.get("explicit_content") else None
        self.external_urls: dict[str | None, str | None] = data.get("external_urls", {})
        self.followers: objects.Followers = objects.Followers(data.get("followers")) if data.get("followers") else None
        self.images: list[objects.Image | None] | None = [objects.Image(image_data) for image_data in data.get("images")] if data.get("images") else None
        self.has_premium: bool | None = data.get("product") == "premium" if data.get("product") else None

    def __repr__(self) -> str:
        return f"<spotify.User display_name=\"{self.name}\" id=\"{self.id}\" url=\"<{self.url}>\">"

    @property
    def url(self):
        return self.external_urls.get("spotify")
