from typing import Any, Iterable

from pydantic import BaseModel, HttpUrl, validator

TextComponent = str | list[str] | dict[str, Any]

DOWNLOAD_LINK = (
    "https://github.com"
    "/Smithed-MC/Libraries/releases"
    "/download/v{version}/{id}-{version}_{type}.zip"
)


def flatten_component(component: TextComponent):
    def _flatten(component: TextComponent) -> Iterable[str]:
        match component:
            case str() as text:
                yield text

            case list() as texts:
                yield from _flatten(texts)

            case dict() as text_component:
                yield text_component.get("text", "")

    return "".join(_flatten(component))


class LibraryManifest(BaseModel):
    id: str
    name: str
    description: str
    version: str
    data_pack_url: HttpUrl | None = None
    resource_pack_url: HttpUrl | None = None

    @validator("data_pack_url", pre=True)
    def init_data_pack_url(cls, value: str, values: dict[str, Any]):
        return DOWNLOAD_LINK.format(
            version=values["version"],
            id=values["id"],
            type="data_pack",
        )

    @validator("resource_pack_url", pre=True)
    def init_resource_pack_url(cls, value: str, values: dict[str, Any]):
        return DOWNLOAD_LINK.format(
            version=values["version"],
            id=values["id"],
            type="resource_pack",
        )
