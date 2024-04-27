from beet import Context, Function, Predicate
from typing import Any
import json


def beet_default(ctx: Context):
    generate_advanced_remove_tool(ctx)

    generate_tag_args(ctx)


def append_tag(
    ctx: Context,
    tag: str,
):
    # execute if predicate smithed.crafter:block/table/tags/wool run data modify storage smithed.crafter:main root.temp.item_tag append value "#minecraft:wool"

    predicate = {
        "condition": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {"equipment": {"mainhand": {"items": f"#minecraft:{tag}"}}},
    }
    predicate = Predicate(predicate)
    ctx.data.predicates[f"smithed.crafter:block/table/tags/{tag}"] = predicate

    return f"execute if predicate smithed.crafter:block/table/tags/{tag} run data modify storage smithed.crafter:main root.temp.item_tag append value '#minecraft:{tag}'"


def generate_tag_args(ctx: Context):
    minecraft_version: str = ctx.meta["minecraft_version"]
    url = f"https://raw.githubusercontent.com/misode/mcmeta/{minecraft_version}-registries/tag/item/data.json"
    item_tags_file = ctx.cache["smithed.crafter"].download(url)
    with open(item_tags_file) as f:
        item_tags: dict[str, list[str]] = json.load(f)

    commands: list[str] = []
    commands.append(
        "data modify storage smithed.crafter:main root.temp.item_tag set value []"
    )
    for item_tag in item_tags:
        command = append_tag(ctx, item_tag)
        commands.append(command)

    commands.append("function #smithed.crafter:event/query_tags")

    ctx.data.functions[
        f"smithed.crafter:v{ctx.project_version}/block/table/crafting/input/query_tags"
    ] = Function("\n".join(commands))


def delete_tool(item: str, max_damage: int):
    # execute if data entity @s {HandItems:[{id:"minecraft:wooden_sword"}]} if score $temp1 smithed.data matches 59.. run function smithed.crafter:impl/block/table/crafting/output/clear_input/delete_tool/sub
    return f"execute if data entity @s {{HandItems:[{{id:'{item}'}}]}} if score $temp1 smithed.data matches {max_damage}.. run function smithed.crafter:impl/block/table/crafting/output/clear_input/delete_tool/sub"


def generate_advanced_remove_tool(ctx: Context):
    minecraft_version: str = ctx.meta["minecraft_version"]
    url = f"https://raw.githubusercontent.com/misode/mcmeta/{minecraft_version}-summary/item_components/data.json"
    item_components_file = ctx.cache["smithed.crafter"].download(url)
    with open(item_components_file) as f:
        item_components: dict[str, list[Any]] = json.load(f)

    commands: list[str] = []

    for item, components in item_components.items():
        max_damage = [c for c in components if c["type"] == "minecraft:max_damage"]
        if max_damage:
            max_damage = max_damage[0]["value"]

            command = delete_tool(item, max_damage)
            commands.append(command)

    ctx.data.functions[
        f"smithed.crafter:v{ctx.project_version}/block/table/crafting/output/clear_input/delete_tool/vanilla"
    ] = Function("\n".join(commands))