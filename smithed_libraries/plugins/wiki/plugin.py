from typing import Any, Protocol

from beet import Advancement, Context, Dialog, LootTable
from beet.core.utils import JsonDict

from .models import (
    AnySectionModel,
    ArticleSectionModel,
    BookModel,
    CategorySectionModel,
    SectionModel,
    SectionReference,
    TOCSectionModel,
    TitleSectionModel,
)
from .resources import WikiBook, WikiSection


class SectionBuilder[T: SectionModel](Protocol):
    def __call__(self, ctx: Context, section: T) -> JsonDict | list[JsonDict]: ...


class WikiBuilder:
    builders: dict[str, SectionBuilder[Any]]

    def __init__(self, ctx: Context):
        self.builders = {
            "smithed.wiki:title": TitleSectionBuilder(),
            "smithed.wiki:category": CategorySectionBuilder(),
            "smithed.wiki:toc": TOCSectionBuilder(),
            "smithed.wiki:article": ArticleSectionBuilder(),
        }

        ctx.require(self.build)

    def build(self, ctx: Context):
        yield

        for location, book in ctx.data[WikiBook].items():
            book = BookModel.model_validate(book.data)
            namespace, path = location.split(":", 1)

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

            page_idx = 0
            for section in book.sections:
                if isinstance(section, str):
                    section = AnySectionModel.model_validate(
                        ctx.data[WikiSection][section].data
                    ).root

                dialog = self.builders[section.type](ctx, section)

                if isinstance(dialog, list):
                    for d in dialog:
                        ctx.data[f"{location}/page/{page_idx}"] = Dialog(d)
                        page_idx += 1
                else:
                    ctx.data[f"{location}/page/{page_idx}"] = Dialog(dialog)
                    page_idx += 1


class TitleSectionBuilder(SectionBuilder[TitleSectionModel]):
    def __call__(self, ctx: Context, section: TitleSectionModel) -> JsonDict:
        return {
            "type": "minecraft:multi_action",
            "body": [
                {
                    "text": section.title,
                },
                {"text": section.icon},
                {"text": section.description},
            ],
            "actions": [{"label": "Close"}],
        }


class TOCSectionBuilder(SectionBuilder[TOCSectionModel]):

    def build_category(
        self, ctx: Context, sections: list[SectionReference], indentation: int
    ) -> list[JsonDict]:
        toc: list[JsonDict] = []

        for section in sections:
            if isinstance(section, str):
                file = ctx.data[WikiSection][section]
                section = AnySectionModel.model_validate(file.data).root

            toc.append(
                {
                    "text": f"{'  ' * indentation}- {section.title}\n",
                }
            )

            if isinstance(section, CategorySectionModel):
                toc.extend(self.build_category(ctx, section.sections, indentation + 1))

        return toc

    def __call__(self, ctx: Context, section: TOCSectionModel) -> JsonDict:
        return {
            "type": "minecraft:multi_action",
            "body": {
                "type": "minecraft:plain_message",
                "contents": self.build_category(ctx, section.sections, 0),
            },
            "actions": [{"label": "Close"}],
        }


class ArticleSectionBuilder(SectionBuilder[ArticleSectionModel]):
    def __call__(self, ctx: Context, section: ArticleSectionModel) -> JsonDict:
        return {
            "type": "minecraft:multi_action",
            "body": {
                "type": "minecraft:plain_message",
                "contents": [
                    {
                        "text": section.title,
                    },
                    {"text": "---"},
                    {"text": section.content},
                ],
            },
            "actions": [{"label": "Close"}],
        }


class CategorySectionBuilder(SectionBuilder[CategorySectionModel]):
    def build_category(
        self, ctx: Context, sections: list[SectionReference]
    ) -> list[JsonDict]:
        category: list[Any] = []

        for section in sections:
            if isinstance(section, str):
                section = AnySectionModel.model_validate(
                    ctx.data[WikiSection][section].data
                ).root

            category.append(
                {
                    "text": section.icon,
                    "hover_event": {
                        "action": "show_text",
                        "value": {"text": section.title},
                    },
                }
            )

        return category

    def __call__(self, ctx: Context, section: CategorySectionModel) -> JsonDict:
        return {
            "type": "minecraft:multi_action",
            "body": {
                "type": "minecraft:plain_message",
                "contents": [
                    {
                        "text": section.icon,
                    },
                    {
                        "text": section.description,
                    },
                    {"text": "---"},
                    *self.build_category(ctx, section.sections),
                ],
            },
            "actions": [{"label": "Close"}],
        }
