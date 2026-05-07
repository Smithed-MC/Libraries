import pytest
from pydantic import ValidationError
from beet import Context, Texture, run_beet

# Relative imports from your package
from ..models import (
    AnySectionModel,
    ArticleSectionModel,
    BookModel,
    ReferenceSectionModel,
    TitleSectionModel,
    TOCSectionModel,
)
from ..plugin import resolve, WikiBuilder
from ..resources import WikiSection


@pytest.fixture(scope="session")
def ctx():
    """
    Session-scoped fixture to provide a fully loaded Beet context.
    """
    with run_beet() as ctx:
        yield ctx


# --- MODEL TESTS (../models.py) ---


def test_title_section_validates_correctly():
    """
    Tests that a well-formed dictionary correctly validates into a TitleSectionModel
    and checks that default values (like type) are applied.
    """
    data = {
        "type": "smithed.wiki:title",
        "title": "Welcome to the Wiki",
        "description": "This is a test description.",
    }
    model = TitleSectionModel(**data)  # type: ignore

    assert model.title == "Welcome to the Wiki"
    assert model.description == "This is a test description."
    assert model.icon is None  # Tests the default fallback


def test_article_section_missing_content_fails():
    """
    Tests that omitting a required field (like 'content' in ArticleSectionModel)
    properly raises a Pydantic ValidationError.
    """
    data = {
        "type": "smithed.wiki:article",
        "title": "Invalid Article",
        # Missing 'content'
    }

    with pytest.raises(ValidationError):
        ArticleSectionModel(**data)  # type: ignore


def test_any_section_model_discriminator():
    """
    Tests the discriminatory union. Ensures that providing a specific 'type'
    correctly routes the validation to the appropriate sub-model (TOCSectionModel).
    """
    data = {
        "type": "smithed.wiki:toc",
        "title": "Table of Contents",
        "sections": [0, 1, 2],
    }

    model = AnySectionModel.model_validate(data).root
    assert isinstance(model, TOCSectionModel)
    assert model.sections == [0, 1, 2]


def test_book_model_validation():
    """
    Tests that an entire BookModel parses its child sections correctly via the
    SectionUnion and respects default boolean flags.
    """
    data = {
        "components": {"minecraft:custom_data": {"foo": 1}},
        "sections": [
            {
                "type": "smithed.wiki:title",
                "title": "My Book",
                "description": "Book desc",
            },
            {
                "type": "smithed.wiki:article",
                "title": "Page 1",
                "content": "Hello World",
            },
        ],
    }

    book = BookModel(**data)  # type: ignore
    assert not book.grant_automatically  # Default is False
    assert len(book.sections) == 2
    assert isinstance(book.sections[0], TitleSectionModel)
    assert isinstance(book.sections[1], ArticleSectionModel)


# --- RESOURCE TESTS (../resources.py) ---


def test_wiki_section_resource():
    """
    Tests that the Beet WikiSection resource loads correct model data.
    """
    data = {"type": "smithed.wiki:article", "title": "A", "content": "B"}
    resource = WikiSection(data)  # type: ignore
    data = AnySectionModel.model_validate(resource.data).root

    assert isinstance(data, ArticleSectionModel)


# --- PLUGIN LOGIC TESTS (../plugin.py) ---


def test_resolve_standard_reference(ctx: Context):
    """
    Tests that the `resolve` function successfully follows a standard reference
    to grab the underlying article model from the Beet Context.
    """
    # Inject a target article into the Beet context
    ctx.data[WikiSection]["my_pack:articles/target"] = WikiSection(
        {
            "type": "smithed.wiki:article",
            "title": "Targeted Article",
            "content": "You found me!",
        }  # type: ignore
    )

    # Create the reference pointing to the injected article
    ref = ReferenceSectionModel(path="my_pack:articles/target")

    resolved = resolve(ref, ctx)
    assert isinstance(resolved, ArticleSectionModel)
    assert resolved.title == "Targeted Article"


def test_resolve_chained_reference(ctx: Context):
    """
    Tests that the `resolve` function can follow a chain of multiple references
    (e.g., Ref A -> Ref B -> Article) and eventually return the NonReferenceSectionModel.
    """
    ctx.data[WikiSection]["test:ref2"] = WikiSection(
        {
            "type": "smithed.wiki:article",
            "title": "Deep Article",
            "content": "Deep content",
        }  # type: ignore
    )

    ctx.data[WikiSection]["test:ref1"] = WikiSection(
        {"type": "smithed.wiki:reference", "path": "test:ref2"}  # type: ignore
    )

    ref = ReferenceSectionModel(path="test:ref1")
    resolved = resolve(ref, ctx)

    assert isinstance(resolved, ArticleSectionModel)
    assert resolved.title == "Deep Article"


def test_resolve_reference_cycle_handling(ctx: Context):
    """
    Tests that if two references point to each other in an infinite loop,
    the `resolve` function safely breaks the loop and raises a ValueError.
    """
    # Creating a cycle: ref_a -> ref_b -> ref_a
    ctx.data[WikiSection]["test:ref_a"] = WikiSection(
        {"type": "smithed.wiki:reference", "path": "test:ref_b"}  # type: ignore
    )
    ctx.data[WikiSection]["test:ref_b"] = WikiSection(
        {"type": "smithed.wiki:reference", "path": "test:ref_a"}  # type: ignore
    )

    ref = ReferenceSectionModel(path="test:ref_a")

    with pytest.raises(ValueError, match="Resolve failed to resolve reference"):
        resolve(ref, ctx)


def test_wiki_builder_get_image_placeholder(ctx: Context):
    """
    Tests that passing None to `get_image` defaults to the placeholder texture,
    registers it in the current_font dictionary, and returns the E000 unicode character.
    """
    builder = WikiBuilder(ctx)
    builder.current_font = {}
    builder.current_path = "test_path"

    # Inject PLACEHOLDER to bypass Key Error
    ctx.assets.textures["smithed.wiki:wiki/placeholder"] = Texture()

    char, path = builder.get_image(None, 16)

    assert char == chr(0xE000)
    assert path == "test_path"
    assert ("smithed.wiki:wiki/placeholder", 16) in builder.current_font


def test_wiki_builder_get_image_valid_texture(ctx: Context):
    """
    Tests that providing a valid texture path registers correctly and
    increments the unicode offset for subsequent images.
    """
    ctx.assets.textures["minecraft:item/diamond"] = Texture()
    ctx.assets.textures["minecraft:item/emerald"] = Texture()

    builder = WikiBuilder(ctx)
    builder.current_font = {}
    builder.current_path = "test_path"

    char1, _ = builder.get_image("minecraft:item/diamond", 16)
    char2, _ = builder.get_image("minecraft:item/emerald", 16)

    assert char1 == chr(0xE000)
    assert char2 == chr(0xE001)

    # Fetching the same image should return the cached unicode character
    char_duplicate, _ = builder.get_image("minecraft:item/diamond", 16)
    assert char_duplicate == chr(0xE000)
