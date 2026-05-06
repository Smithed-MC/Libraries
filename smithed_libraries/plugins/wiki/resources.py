from typing import ClassVar

from beet import JsonFileBase, NamespaceFileScope

from .models import BookModel, AnySectionModel


class WikiBook(JsonFileBase[BookModel]):
    """
    Registers a wiki book resource.
    """

    scope: ClassVar[NamespaceFileScope] = ("wiki", "book")
    """
    The scope of the resource.
    Loaded from `namespace:wiki/book/<name>.json`
    """
    extension: ClassVar[str] = ".json"
    """
    The extension of the resource.
    """
    model = BookModel
    """
    The model used to validate the resource.
    """


class WikiSection(JsonFileBase[AnySectionModel]):
    """
    Registers a wiki section resource.
    """

    scope: ClassVar[NamespaceFileScope] = ("wiki", "section")
    """
    The scope of the resource.
    Loaded from `namespace:wiki/section/<name>.json`
    """
    extension: ClassVar[str] = ".json"
    """
    The extension of the resource.
    """
    model = AnySectionModel
    """
    The model used to validate the resource.
    """
