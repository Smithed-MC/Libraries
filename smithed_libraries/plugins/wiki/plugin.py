from typing import Any, Protocol, cast

from beet import Advancement, Context, Dialog, Font, Function, FunctionTag, LootTable
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
)
from .resources import WikiBook, WikiSection

PAGE_INDEX_OFFSET = 1000
SEPARATOR = "dark_gray"
DESCRIPTION = "gray"
PLACEHOLDER = "smithed.wiki:wiki/placeholder"


class SectionBuilder[T: SectionModel](Protocol):
    def __call__(
        self, key: str, builder: WikiBuilder, section: T
    ) -> list[tuple[str, JsonDict]]: ...


class WikiBuilder:
    current: BookModel
    current_path: str
    current_font: dict[tuple[str, int], int]

    builders: dict[str, SectionBuilder[Any]]

    def __init__(self, ctx: Context):
        self.builders = {
            "smithed.wiki:title": TitleSectionBuilder(),
            "smithed.wiki:category": CategorySectionBuilder(),
            "smithed.wiki:toc": TOCSectionBuilder(),
            "smithed.wiki:article": ArticleSectionBuilder(),
        }

        self.ctx = ctx
        ctx.require(self.build_all)

    def get_image(self, texture: str | None, height: int = 16) -> tuple[str, str]:
        if texture is None or len(texture.strip()) == 0:
            texture = PLACEHOLDER

        if (texture, height) in self.current_font:
            idx = self.current_font[(texture, height)]
            return chr(0xE000 + idx), self.current_path

        if texture in self.ctx.assets.textures:
            idx = len(self.current_font)
            self.current_font[(texture, height)] = idx
            return chr(0xE000 + idx), self.current_path
        else:
            raise ValueError(f"Texture {texture} not found")

    def build(self, key: str, section: SectionUnion) -> list[tuple[str, JsonDict]]:
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
        yield

        for location, book in ctx.data[WikiBook].items():
            book = BookModel.model_validate(book.data)
            namespace, path = location.split(":", 1)

            self.current = book
            self.current_path = f"{namespace}:{path}"
            self.current_font = {}

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
                                                    "summit": {"id": "sticker_book"},
                                                    "smithed": {
                                                        "ignore": {
                                                            "functionality": True,
                                                            "crafting": True,
                                                        }
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

            if book.grant_automatically:
                ctx.data[f"{namespace}:technical/tick/{path}"] = Advancement(
                    {
                        "criteria": {"tick": {"trigger": "minecraft:tick"}},
                        "rewards": {"loot": [path]},
                    }
                )

            trigger_name = f"{namespace}.{path.replace('/', '.')}.trigger"

            # Register the trigger commands for changing pages
            ctx.data[Function].setdefault(
                f"{namespace}:technical/load", Function()
            ).append(f"scoreboard objectives add {trigger_name} trigger")
            ctx.data[Function].setdefault(
                f"{namespace}:technical/tick", Function()
            ).append(
                f"""
                    scoreboard players enable @a {trigger_name}
                    execute as @a[scores={{{trigger_name}=1000..}}] run function {namespace}:wiki/{path}/change_page
                """
            )

            ctx.data[FunctionTag].setdefault(f"minecraft:load", FunctionTag()).add(
                f"{namespace}:technical/load"
            )

            ctx.data[FunctionTag].setdefault(f"minecraft:tick", FunctionTag()).add(
                f"{namespace}:technical/tick"
            )

            # Display the appropriate page when the player runs the trigger
            ctx.data[Function][f"{namespace}:wiki/{path}/change_page"] = Function(f"""
                    scoreboard players remove @s {trigger_name} 1000
                    execute store result storage smithed.wiki:temp page int 1 run scoreboard players get @s {trigger_name}
                    scoreboard players reset @s {trigger_name}
                    function {namespace}:wiki/{path}/change_page/macro with storage smithed.wiki:temp {{}} 
                """)

            ctx.data[Function][f"{namespace}:wiki/{path}/change_page/macro"] = Function(
                f"""
                    $dialog show @s {namespace}:{path}/page/$(page)
                """
            )

            # We use a unique key for each section, so that each section can generate multiple pages
            pages: list[tuple[str, JsonDict]] = []

            # The index of the first ToC
            toc_index = -1

            for idx, section in enumerate(book.sections):
                pages.extend(self.build(f"{namespace}:{path}/{idx}", section))

                if isinstance(section, TOCSectionModel):
                    if toc_index != -1:
                        raise ValueError(
                            f"Multiple ToC sections found for book {namespace}:{path}"
                        )
                    toc_index = idx

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
                        {"text": " " * 5},
                        (
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

                self.resolve_change_page(
                    page["body"]["contents"], trigger_name, key_to_index
                )

                ctx.data[f"{namespace}:{path}/page/{idx}"] = Dialog(page)


def resolve(section: ReferenceSectionModel, ctx: Context) -> NonReferenceSectionModel:
    root = section
    visited: set[str] = set()

    while root.type == "smithed.wiki:reference" and root.path not in visited:
        visited.add(root.path)
        section = ctx.data[WikiSection][root.path].data
        root = AnySectionModel.model_validate(section).root

    if root.type == "smithed.wiki:reference":
        raise ValueError("Resolve failed to resolve reference")

    return cast(NonReferenceSectionModel, root)


class TitleSectionBuilder(SectionBuilder[TitleSectionModel]):
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
        toc: list[JsonDict] = []

        if section.type == "smithed.wiki:reference":
            section = resolve(section, builder.ctx)

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

        if isinstance(section, CategorySectionModel):
            for idx, s in enumerate(section.sections):
                toc.extend(
                    self.build_category(f"{key}/{idx}", builder, s, indentation + 1)
                )

        return toc

    def __call__(
        self, key: str, builder: WikiBuilder, section: TOCSectionModel
    ) -> list[tuple[str, JsonDict]]:
        toc: list[JsonDict] = []

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
        for i, section in enumerate(sections):
            if section.type == "smithed.wiki:reference":
                section = resolve(section, builder.ctx)

            icon, font = builder.get_image(section.icon)

            body.append(
                {
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
