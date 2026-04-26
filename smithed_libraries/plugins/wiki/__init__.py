from typing import ClassVar

from beet import Context, JsonFileBase, NamespaceFileScope, TextFileBase
from pydantic import BaseModel


class WikiConfigModel(BaseModel):
    title: str
    description: str
    icon: str
    category: str


class WikiConfig(JsonFileBase[WikiConfigModel]):
    scope: ClassVar[NamespaceFileScope] = ("wiki", "book")
    extension: ClassVar[str] = ".json"


class WikiPage(JsonFileBase[WikiConfigModel]):
    scope: ClassVar[NamespaceFileScope] = ("wiki", "page")
    extension: ClassVar[str] = ".json"


class WikiContent(TextFileBase[str]):
    scope: ClassVar[NamespaceFileScope] = ("wiki", "page")
    extension: ClassVar[str] = ".md"


def beet_default(ctx: Context):
    ctx.data.extend_namespace.append(WikiConfig)
    ctx.data.extend_namespace.append(WikiPage)
    ctx.data.extend_namespace.append(WikiContent)

    yield 

    for config in ctx.data[WikiConfig].items():
        print(config)

    for page in ctx.data[WikiPage].items():
        print(page)

    for content in ctx.data[WikiContent].items():
        print(content)
