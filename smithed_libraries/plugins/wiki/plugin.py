import logging
from typing import Any, Protocol, cast

from beet import (
    Advancement,
    Context,
    Dialog,
    Font,
    Function,
    FunctionTag,
    LootTable,
    Predicate,
)
from beet.core.utils import JsonDict

from .models import (
    AnySectionModel,
    ArticleSectionModel,
    BookModel,
    CategorySectionModel,
    NonReferenceSectionModel,
    ReferenceSectionModel,
    SectionModel,
    SectionUnion,
    TOCSectionModel,
    TitleSectionModel,
    WikiOpts,
)
from .resources import WikiBook, WikiSection

logger = logging.getLogger(__name__)


PAGE_INDEX_OFFSET = 1000
SEPARATOR = "dark_gray"
DESCRIPTION = "gray"
PLACEHOLDER = "smithed.wiki:wiki/placeholder"


class SectionBuilder[T: SectionModel](Protocol):
    def __call__(
        self, key: str, builder: WikiBuilder, section: T
    ) -> list[tuple[str, JsonDict]]: ...


class WikiBuilder:
    """
    The context object used to build wiki books and sections.
    """

    current: BookModel
    """
    The book that is currently being built.
    """
    current_path: str
    """
    The path to the current book.
    """
    current_font: dict[tuple[str, int], int]
    """
    The set of font characters current in use.

    Where the key is a tuple of (`path to image`, `height`) and the value is the unicode character offset from \\uE000.
    """

    builders: dict[str, SectionBuilder[Any]]
    """
    The builders for each section type.
    """

    def __init__(self, ctx: Context):
        # Define the default builders for the sections
        self.builders = {
            "smithed.wiki:title": TitleSectionBuilder(),
            "smithed.wiki:category": CategorySectionBuilder(),
            "smithed.wiki:toc": TOCSectionBuilder(),
            "smithed.wiki:article": ArticleSectionBuilder(),
        }

        self.ctx = ctx

        # Get the override for the implementation folder if present
        self.opts = WikiOpts.model_validate(ctx.meta.get("smithed.wiki", {}))

        # Predicate used to detect if the player is holding a wiki book in either hand
        ctx.data["smithed.wiki:impl/technical/holding_book"] = Predicate(
            {
                "condition": "minecraft:any_of",
                "terms": [
                    {
                        "condition": "minecraft:entity_properties",
                        "entity": "this",
                        "predicate": {
                            "equipment": {
                                "offhand": {
                                    "predicates": {
                                        "minecraft:custom_data": {
                                            "smithed": {"wiki": {"book": True}}
                                        }
                                    }
                                }
                            }
                        },
                    },
                    {
                        "condition": "minecraft:entity_properties",
                        "entity": "this",
                        "predicate": {
                            "equipment": {
                                "mainhand": {
                                    "predicates": {
                                        "minecraft:custom_data": {
                                            "smithed": {"wiki": {"book": True}}
                                        }
                                    }
                                }
                            }
                        },
                    },
                ],
            }
        )

        # Define a scoreboard which is used to track when the player opens a book
        ctx.data[Function].setdefault(
            "smithed.wiki:impl/technical/load", Function()
        ).append(
            """ 
                schedule function smithed.wiki:impl/technical/tick 1t replace
                scoreboard objectives add smithed.wiki.use_book minecraft.used:minecraft.written_book
            """
        )

        # Function responsible for detecting the previously defined scoreboard
        ctx.data[Function].setdefault(
            "smithed.wiki:impl/technical/tick", Function()
        ).append(
            """
                schedule function smithed.wiki:impl/technical/tick 1t replace
                execute as @a[scores={smithed.wiki.use_book=1..}] run function smithed.wiki:impl/wiki/use_book
            """
        )

        ctx.data[FunctionTag].setdefault("minecraft:load", FunctionTag()).add(
            "smithed.wiki:impl/technical/load"
        )

        # The function ran on players that use a book
        ctx.data["smithed.wiki:impl/wiki/use_book"] = Function("""
                # Reset the player's score
                scoreboard players reset @s smithed.wiki.use_book

                # Exit early if they didn't use a wiki book
                execute unless predicate smithed.wiki:impl/technical/holding_book run return fail

                # Determine the ID of the book they used
                data remove storage smithed.wiki:temp trigger_name
                data modify storage smithed.wiki:temp trigger_name set from entity @s SelectedItem.components."minecraft:custom_data".smithed.wiki.trigger
                execute unless data storage smithed.wiki:temp trigger_name run data modify storage smithed.wiki:temp trigger_name set from entity @s equipment.offhand.components."minecraft:custom_data".smithed.wiki.trigger

                # Display the book
                function smithed.wiki:impl/wiki/use_book/macro with storage smithed.wiki:temp {} 
            """)

        # Function used to open the first page of the book via macri
        ctx.data["smithed.wiki:impl/wiki/use_book/macro"] = Function(f"""
                $trigger $(trigger_name) set {PAGE_INDEX_OFFSET}
            """)

        # Add the plugin to build all books at the end of the pipeline step
        ctx.require(self.build_all)

    def get_image(self, texture: str | None, height: int = 16) -> tuple[str, str]:
        """
        Parameters
        ---
        **texture**: The path in context to the texture. If `None`, the placeholder texture is used instead.

        **height**: The height of the texture in pixels. Defaults to 16px.

        Returns
        ---
        A tuple of a unicode character and font name to render the given texture.
        """
        if texture is None or len(texture.strip()) == 0:
            texture = PLACEHOLDER

        # If the texture & height has been registered, return it
        if (texture, height) in self.current_font:
            idx = self.current_font[(texture, height)]
            return chr(0xE000 + idx), self.current_path

        # If the texture is found in context, register it in the dictionary and return it
        if texture in self.ctx.assets.textures:
            idx = len(self.current_font)
            self.current_font[(texture, height)] = idx
            return chr(0xE000 + idx), self.current_path
        else:
            raise KeyError(f"Texture {texture} not found")

    def build(self, key: str, section: SectionUnion) -> list[tuple[str, JsonDict]]:
        """
        Builds the provided section.
        Parameters
        ---
        **key**: The key used to identify the section.

        **section**: The section to build.
        Returns
        ---
        A list of pages produced by the section.
        Each page is represented by a tuple where:
         - The first element is the key that generated the page (used for nesting)
         - And the second is the JSON body of the page.
        """
        if section.type == "smithed.wiki:reference":
            while section.type == "smithed.wiki:reference":
                section = AnySectionModel.model_validate(
                    self.ctx.data[WikiSection][section.path].data
                ).root

        dialog = self.builders[section.type](key, self, section)

        return dialog

    def resolve_change_page(
        self, contents: Any, trigger_name: str, key_to_index: dict[str, int]
    ):
        """
        Recursively update change_page actions to the appropriate trigger command

        Parameters
        ---
        **contents**: The object to update

        **trigger_name**: The name of the trigger to be used in the command

        **key_to_index**: A mapping from section key to page index
        """
        match contents:
            case list():
                for c in contents:
                    self.resolve_change_page(c, trigger_name, key_to_index)
            case dict():
                if (click_event := contents.get("click_event")) and isinstance(
                    click_event, dict
                ):
                    if click_event.get("action") == "change_page":
                        key = click_event.get("page")
                        if (
                            isinstance(key, str)
                            and key.startswith("%")
                            and key.endswith("%")
                        ):
                            key = key[1:-1]
                            contents["click_event"] = {
                                "action": "run_command",
                                "command": f"/trigger {trigger_name} set {key_to_index[key] + PAGE_INDEX_OFFSET}",
                            }

                for c in contents.values():
                    self.resolve_change_page(c, trigger_name, key_to_index)
            case _:
                pass

    def build_all(self, ctx: Context):
        """
        Builds all wiki books loaded into context
        """
        yield

        for location, book in ctx.data[WikiBook].items():
            logger.info(f"Building book {location}")
            # Validate the Pydantic model and configure the builder
            book = BookModel.model_validate(book.data)
            namespace, path = location.split(":", 1)

            base_path = f"{namespace}:{self.opts.implementation_folder}"

            self.current = book
            self.current_path = location
            self.current_font = {}

            location = f"{base_path}/{path}"

            # Generate a unique trigger name for each book
            trigger_name = f"{namespace}.{path.replace('/', '.')}.trigger"

            # The loot table to give a player the book
            ctx.data[location] = LootTable(
                {
                    "pools": [
                        {
                            "rolls": 1,
                            "entries": [
                                {
                                    "type": "minecraft:item",
                                    "name": "minecraft:written_book",
                                    "functions": [
                                        {
                                            "function": "minecraft:set_components",
                                            "components": {
                                                **book.components,
                                                "minecraft:custom_data": {
                                                    "smithed": {
                                                        "wiki": {
                                                            "book": True,
                                                            "trigger": trigger_name,
                                                        },
                                                        "ignore": {
                                                            "functionality": True,
                                                            "crafting": True,
                                                        },
                                                    },
                                                },
                                                "minecraft:enchantment_glint_override": False,
                                                "!written_book_content": {},
                                                "minecraft:tooltip_display": {
                                                    "hidden_components": [
                                                        "minecraft:written_book_content"
                                                    ]
                                                },
                                                "minecraft:max_stack_size": 1,
                                            },
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                }
            )

            # If the book is automatically granted, generate an advancement that rewards the above loot table
            if book.grant_automatically:
                ctx.data[f"{base_path}/technical/tick/{path}"] = Advancement(
                    {
                        "criteria": {"tick": {"trigger": "minecraft:tick"}},
                        "rewards": {"loot": [location]},
                    }
                )

            # Register the trigger commands for changing pages
            ctx.data[Function].setdefault(
                f"{namespace}:{self.opts.load_function}", Function()
            ).append(f"scoreboard objectives add {trigger_name} trigger")
            ctx.data[Function].setdefault(
                f"{namespace}:{self.opts.tick_function}", Function()
            ).append(
                f"""
                    scoreboard players enable @a {trigger_name}
                    execute as @a[scores={{{trigger_name}=1000..}}] run function {base_path}/{path}/change_page
                """
            )

            # Display the appropriate page when the player runs the trigger
            ctx.data[Function][f"{base_path}/{path}/change_page"] = Function(f"""
                    scoreboard players remove @s {trigger_name} 1000
                    execute store result storage smithed.wiki:temp page int 1 run scoreboard players get @s {trigger_name}
                    scoreboard players reset @s {trigger_name}
                    function {base_path}/{path}/change_page/macro with storage smithed.wiki:temp {{}} 
                """)

            ctx.data[Function][f"{base_path}/{path}/change_page/macro"] = Function(f"""
                    $dialog show @s {base_path}/{path}/page/$(page)
                """)

            # We use a unique key for each section, so that each section can generate multiple pages
            pages: list[tuple[str, JsonDict]] = []

            # The index of the first ToC
            toc_index = -1

            for idx, section in enumerate(book.sections):
                pages.extend(self.build(f"{self.current_path}/{idx}", section))

                # Store the index to the TOC, if theres multiple, raise an error.
                if isinstance(section, TOCSectionModel):
                    if toc_index != -1:
                        raise ValueError(
                            f"Multiple ToC sections found for book {namespace}:{path}"
                        )
                    toc_index = idx

            # Build the required font to render all images
            ctx.assets[Font][self.current_path] = Font(
                {
                    "providers": [
                        {
                            "type": "bitmap",
                            "ascent": 0,
                            "chars": [chr(0xE000 + idx)],
                            "file": texture + ".png",
                            "height": height,
                        }
                        for (texture, height), idx in self.current_font.items()
                    ]
                }
            )

            # Saves the index to the first occurence of a given key
            key_to_index: dict[str, int] = {}
            for idx, (key, _) in enumerate(pages):
                if key not in key_to_index:
                    key_to_index[key] = idx

            for idx, (_, page) in enumerate(pages):
                page["title"] = {
                    "translate": f"item.{namespace}.{path.replace('/', '.')}"
                }
                page["pause"] = False

                page["body"]["contents"].append(
                    [
                        (
                            "",
                            (
                                # If the page isn't first, add a back button
                                {
                                    "text": "\n<--",
                                    "color": "gold",
                                    "bold": True,
                                    "hover_event": {
                                        "action": "show_text",
                                        "value": {"text": "Previous Page"},
                                    },
                                    "click_event": {
                                        "action": "run_command",
                                        "command": f"/trigger {trigger_name} set {idx + PAGE_INDEX_OFFSET - 1}",
                                    },
                                }
                                if idx > 0
                                else {"text": "\n    "}
                            ),
                        ),
                        {"text": " " * 5},
                        (
                            # Add a button to go to the TOC if it is present in the book
                            {
                                "text": "■",
                                "color": "gold",
                                "hover_event": {
                                    "action": "show_text",
                                    "value": {"text": "Table of Contents"},
                                },
                                "click_event": {
                                    "action": "run_command",
                                    "command": f"/trigger {trigger_name} set {toc_index + PAGE_INDEX_OFFSET}",
                                },
                            }
                            if toc_index != -1
                            else {"text": " "}
                        ),
                        {"text": " " * 5},
                        (
                            # If it isn't the last page, add a button to go forward
                            {
                                "text": "-->",
                                "color": "gold",
                                "bold": True,
                                "hover_event": {
                                    "action": "show_text",
                                    "value": {"text": "Next Page"},
                                },
                                "click_event": {
                                    "action": "run_command",
                                    "command": f"/trigger {trigger_name} set {idx + PAGE_INDEX_OFFSET + 1}",
                                },
                            }
                            if idx < len(pages) - 1
                            else {"text": "    "}
                        ),
                    ]
                )

                # Resolve any change_page actions
                self.resolve_change_page(
                    page["body"]["contents"], trigger_name, key_to_index
                )

                # Save the page into context
                ctx.data[f"{base_path}/{path}/page/{idx}"] = Dialog(page)

        yield

        ctx.data[WikiBook].clear()
        ctx.data[WikiSection].clear()


def resolve(section: ReferenceSectionModel, ctx: Context) -> NonReferenceSectionModel:
    """
    Resolves a reference section to the section it points to.
    """
    root = section

    # Use a set to prevent cycles
    visited: set[str] = set()

    while root.type == "smithed.wiki:reference" and root.path not in visited:
        visited.add(root.path)
        section = ctx.data[WikiSection][root.path].data
        root = AnySectionModel.model_validate(section).root

    if root.type == "smithed.wiki:reference":
        raise ValueError("Resolve failed to resolve reference")

    return cast(NonReferenceSectionModel, root)


class TitleSectionBuilder(SectionBuilder[TitleSectionModel]):
    """
    The builder for title pages.
    """

    def __call__(
        self, key: str, builder: WikiBuilder, section: TitleSectionModel
    ) -> list[tuple[str, JsonDict]]:
        icon, font = builder.get_image(section.icon, 64)

        return [
            (
                key,
                {
                    "type": "minecraft:multi_action",
                    "body": {
                        "type": "minecraft:plain_message",
                        "contents": [
                            "",
                            {"text": section.title, "bold": True},
                            "\n",
                            {"text": icon, "font": font},
                            # Spacing for a 64px image.
                            "\n" * 9,
                            {"text": section.description, "color": DESCRIPTION},
                            "\n",
                        ],
                    },
                    "actions": [{"label": "Close"}],
                },
            )
        ]


class TOCSectionBuilder(SectionBuilder[TOCSectionModel]):

    def build_category(
        self, key: str, builder: WikiBuilder, section: SectionUnion, indentation: int
    ) -> list[JsonDict]:
        """
        Builds the links to the section of the TOC.
        """
        toc: list[JsonDict] = []

        # Resolve the reference
        if section.type == "smithed.wiki:reference":
            section = resolve(section, builder.ctx)

        # Appease the type checker
        assert section.type != "smithed.wiki:reference"

        toc.append({"text": f"{'  ' * indentation}- ", "color": SEPARATOR})

        toc.append(
            {
                "text": f"{section.title}\n",
                "color": "white",
                "click_event": {"action": "change_page", "page": f"%{key}%"},
                "hover_event": {
                    "action": "show_text",
                    "value": {"text": f"Jump to '{section.title}'"},
                },
            }
        )

        # Recursively build the subsections
        if isinstance(section, CategorySectionModel):
            for idx, s in enumerate(section.sections):
                toc.extend(
                    self.build_category(f"{key}/{idx}", builder, s, indentation + 1)
                )

        return toc

    def __call__(
        self, key: str, builder: WikiBuilder, section: TOCSectionModel
    ) -> list[tuple[str, JsonDict]]:
        """
        Builds the table of contents.
        """

        toc: list[JsonDict] = []

        # Build the sub-sections
        for idx in section.sections:
            category = builder.current.sections[idx]
            toc.extend(
                self.build_category(
                    f"{builder.current_path}/{idx}", builder, category, 0
                )
            )

        return [
            (
                key,
                {
                    "type": "minecraft:multi_action",
                    "body": {
                        "type": "minecraft:plain_message",
                        "contents": [
                            "",
                            {"text": "Table of Contents", "bold": True},
                            {"text": "\n---\n", "color": SEPARATOR},
                            *toc,
                        ],
                    },
                    "actions": [{"label": "Close"}],
                },
            )
        ]


class ArticleSectionBuilder(SectionBuilder[ArticleSectionModel]):
    def __call__(
        self, key: str, builder: WikiBuilder, section: ArticleSectionModel
    ) -> list[tuple[str, JsonDict]]:
        """
        Builds the article section.
        """

        return [
            (
                key,
                {
                    "type": "minecraft:multi_action",
                    "body": {
                        "type": "minecraft:plain_message",
                        "contents": [
                            "\n",
                            {"text": section.title, "bold": True},
                            {"text": "\n---\n", "color": SEPARATOR},
                            {"text": section.content},
                            "\n",
                        ],
                    },
                    "actions": [{"label": "Close"}],
                },
            )
        ]


class CategorySectionBuilder(SectionBuilder[CategorySectionModel]):
    def build_category(
        self,
        key: str,
        builder: WikiBuilder,
        sections: list[SectionUnion],
        body: list[JsonDict],
    ) -> list[tuple[str, JsonDict]]:
        """
        Builds the category section.
        """

        for i, section in enumerate(sections):
            if section.type == "smithed.wiki:reference":
                section = resolve(section, builder.ctx)

            icon, font = builder.get_image(section.icon)

            body.append(
                {
                    # Adds an additional space between the current icon and the next
                    "text": f'{icon}{"   " if i % 4 < 3 and i + 1 < len(sections) else "\n\n\n"}',
                    "font": font,
                    "hover_event": {
                        "action": "show_text",
                        "value": {"text": f"Jump to '{section.title}'"},
                    },
                    "click_event": {
                        "action": "change_page",
                        "page": f"%{key}/{i}%",
                    },
                }
            )

        # Build the sub-sections
        dialogs: list[tuple[str, JsonDict]] = []
        for i, d in enumerate(sections):
            dialogs.extend(builder.build(f"{key}/{i}", d))

        return dialogs

    def __call__(
        self, key: str, builder: WikiBuilder, section: CategorySectionModel
    ) -> list[tuple[str, JsonDict]]:
        body: list[JsonDict] = []
        dialogs = self.build_category(key, builder, section.sections, body)

        icon, font = builder.get_image(section.icon, 32)

        return [
            (
                key,
                {
                    "type": "minecraft:multi_action",
                    "body": {
                        "type": "minecraft:plain_message",
                        "contents": [
                            "",
                            {
                                "text": icon,
                                "font": font,
                                "bold": True,
                            },
                            # Adds space for a 32px image
                            "\n" * 5,
                            {
                                "text": f"{section.title}\n",
                                "bold": True,
                            },
                            {"text": section.description, "color": DESCRIPTION},
                            {"text": "\n---\n", "color": SEPARATOR},
                            *body,
                        ],
                    },
                    "actions": [{"label": "Close"}],
                },
            ),
            *dialogs,
        ]
