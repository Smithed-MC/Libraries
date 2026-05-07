from typing import Annotated, Any, ClassVar, Literal

from pydantic import BaseModel, Field, RootModel


class WikiOpts(BaseModel):
    implementation_folder: str = "wiki"
    """
    The base folder the generated files go into.
    """

    tick_function: str = "impl/technical/tick"
    load_function: str = "impl/technical/load"

class SectionModel(BaseModel):
    """
    Represents a section of pages for a Wiki.
    """
    _section_registry: ClassVar[list[type[BaseModel]]] = []

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        cls._section_registry.append(cls)


class NonReferenceSectionModel(SectionModel):
    """
    Represents any section that is not a reference to another section
    """

    title: str
    """The title of the section"""
    icon: str | None = None
    """The icon used to display the section"""


class ReferenceSectionModel(BaseModel):
    """
    Represents a reference to another section
    """

    type: Literal["smithed.wiki:reference"] = "smithed.wiki:reference"
    """The type of the section"""
    path: str
    """The path to the referenced section in the Beet context"""


class TitleSectionModel(NonReferenceSectionModel):
    """
    Represents a title page
    """

    type: Literal["smithed.wiki:title"] = "smithed.wiki:title"
    """The type of the section"""

    description: str
    """The description of the book"""


class CategorySectionModel(NonReferenceSectionModel):
    """
    Represents a category of sections
    """

    type: Literal["smithed.wiki:category"] = "smithed.wiki:category"
    """The type of the section"""

    description: str
    """The description of the category"""

    sections: list[SectionUnion]
    """The sections in the category"""


class TOCSectionModel(NonReferenceSectionModel):
    """
    Represents the table of contents of the book
    """
    type: Literal["smithed.wiki:toc"] = "smithed.wiki:toc"
    """The type of the section"""

    sections: list[int]
    """The index to each section in the book"""


class ArticleSectionModel(NonReferenceSectionModel):
    """
    Represents an article section
    """
    type: Literal["smithed.wiki:article"] = "smithed.wiki:article"
    """The type of the section"""

    content: str
    """The content of the article"""


SectionUnion = Annotated[
    ReferenceSectionModel
    | ArticleSectionModel
    | CategorySectionModel
    | TitleSectionModel
    | TOCSectionModel,
    Field(discriminator="type"),
]
"""Represents the possible types for a section"""


class BookModel(BaseModel):
    components: dict[str, Any]
    sections: list[SectionUnion]
    grant_automatically: bool = False


class AnySectionModel(RootModel[SectionUnion]):
    root: SectionUnion


AnySectionModel.model_rebuild()
