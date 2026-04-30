from typing import Annotated, Any, ClassVar, Literal

from pydantic import BaseModel, Field, RootModel


class SectionModel(BaseModel):
    _section_registry: ClassVar[list[type[BaseModel]]] = []

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        cls._section_registry.append(cls)

class NonReferenceSectionModel(SectionModel):
    title: str
    icon: str | None = None

class ReferenceSectionModel(BaseModel):
    type: Literal["smithed.wiki:reference"] = "smithed.wiki:reference"
    path: str

class TitleSectionModel(NonReferenceSectionModel):
    type: Literal["smithed.wiki:title"] = "smithed.wiki:title"
    description: str

class CategorySectionModel(NonReferenceSectionModel):
    type: Literal["smithed.wiki:category"] = "smithed.wiki:category"
    description: str
    sections: list[SectionUnion]


class TOCSectionModel(NonReferenceSectionModel):
    type: Literal["smithed.wiki:toc"] = "smithed.wiki:toc"
    sections: list[int]


class ArticleSectionModel(NonReferenceSectionModel):
    type: Literal["smithed.wiki:article"] = "smithed.wiki:article"
    content: str


SectionUnion = Annotated[
    ReferenceSectionModel | ArticleSectionModel | CategorySectionModel | TitleSectionModel | TOCSectionModel,
    Field(discriminator="type"),
]

class BookModel(BaseModel):
    components: dict[str, Any]
    sections: list[SectionUnion]
    grant_automatically: bool = False


class AnySectionModel(RootModel[SectionUnion]):
    root: SectionUnion

AnySectionModel.model_rebuild()
