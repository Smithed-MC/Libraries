from typing import ClassVar

from beet import JsonFileBase, NamespaceFileScope, TextFileBase

from .models import BookModel, AnySectionModel

class WikiBook(JsonFileBase[BookModel]):
    scope: ClassVar[NamespaceFileScope] = ("wiki", "book")
    extension: ClassVar[str] = ".json"
    model = BookModel


class WikiSection(JsonFileBase[AnySectionModel]):
    scope: ClassVar[NamespaceFileScope] = ("wiki", "section")
    extension: ClassVar[str] = ".json"
    model = AnySectionModel

class WikiContent(TextFileBase[str]):
    scope: ClassVar[NamespaceFileScope] = ("wiki", "page")
    extension: ClassVar[str] = ".md"
