import json

from beet import Context

from .models import AnySectionModel, SectionModel, BookModel
from .plugin import WikiBuilder
from .resources import WikiBook, WikiSection



def beet_default(ctx: Context):
    """
        Main entry point for the Smithed Wiki library.
        ---
        ctx - The Beet context object used to manipulate the project.
    """

    # Add our resources to the context so that they will be automatically loaded
    ctx.data.extend_namespace.append(WikiBook)
    ctx.data.extend_namespace.append(WikiSection)

    # Inject the WikiBuilder to configure it and add necessary hooks
    ctx.inject(WikiBuilder)

    yield

    # Rebuild all models to properly update the necessary unions
    for model in SectionModel._section_registry:
        model.model_rebuild()

    # Create a JSON schema for the important models so that the IDE can lint the files correctly.
    (ctx.cache["smithed.wiki"].directory / "book.json").write_text(
        json.dumps(BookModel.model_json_schema())
    )

    (ctx.cache["smithed.wiki"].directory / "section.json").write_text(
        json.dumps(AnySectionModel.model_json_schema())
    )
