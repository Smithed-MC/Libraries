import json

from beet import Context

from .models import AnySectionModel, SectionModel, BookModel
from .plugin import WikiBuilder
from .resources import WikiBook, WikiContent, WikiSection


def beet_default(ctx: Context):
    ctx.data.extend_namespace.append(WikiBook)
    ctx.data.extend_namespace.append(WikiSection)
    ctx.data.extend_namespace.append(WikiContent)

    ctx.inject(WikiBuilder)

    yield

    for model in SectionModel._section_registry:
        model.model_rebuild()

    (ctx.cache["smithed.wiki"].directory / "book.json").write_text(
        json.dumps(BookModel.model_json_schema())
    )

    (ctx.cache["smithed.wiki"].directory / "section.json").write_text(
        json.dumps(AnySectionModel.model_json_schema())
    )
