from typing import Annotated, Any, ClassVar, Literal

from pydantic import BaseModel, Field, RootModel


class SectionModel(BaseModel):
    title: str
    icon: str | None = None

    _section_registry: ClassVar[list[type[BaseModel]]] = []

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        cls._section_registry.append(cls)


class TitleSectionModel(SectionModel):
    type: Literal["smithed.wiki:title"] = "smithed.wiki:title"
    description: str


class CategorySectionModel(SectionModel):
    type: Literal["smithed.wiki:category"] = "smithed.wiki:category"
    description: str
    sections: list[SectionReference]


class TOCSectionModel(SectionModel):
    type: Literal["smithed.wiki:toc"] = "smithed.wiki:toc"
    sections: list[SectionReference]


class ArticleSectionModel(SectionModel):
    type: Literal["smithed.wiki:article"] = "smithed.wiki:article"
    content: str


SectionUnion = Annotated[
    ArticleSectionModel | CategorySectionModel | TitleSectionModel | TOCSectionModel,
    Field(discriminator="type"),
]

type SectionReference = str | SectionUnion

class BookModel(BaseModel):
    components: dict[str, Any]
    sections: list[SectionReference]
    grant_automatically: bool = False


class AnySectionModel(RootModel[SectionUnion]):
    root: SectionUnion

AnySectionModel.model_rebuild()
