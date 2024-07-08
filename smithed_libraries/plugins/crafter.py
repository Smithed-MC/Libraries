from beet import Context, Function, Predicate
from typing import Any
import json
from mecha import Mecha

mc = Mecha()

def beet_default(ctx: Context):
    generate_advanced_remove_tool(ctx)

    generate_tag_args(ctx)


def append_tag(
    ctx: Context,
    tag: str,
):

    return f"""
execute 
    if items entity @s weapon.mainhand #minecraft:{tag} 
    run data modify storage smithed.crafter:main root.temp.item_tag append value '#minecraft:{tag}'
"""


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
    ].append(mc.serialize(mc.parse("\n".join(commands), multiline=True)))


def delete_tool(ctx: Context, item: str, max_damage: int):
    return f"""
execute 
    if data entity @s {{HandItems:[{{id:"minecraft:{item}"}}]}}
    if score $temp1 smithed.data matches {max_damage}.. 
    run function smithed.crafter:v{ctx.project_version}/block/table/crafting/output/clear_input/delete_tool/sub
"""



def generate_advanced_remove_tool(ctx: Context):
    minecraft_version: str = ctx.meta["minecraft_version"]
    url = f"https://raw.githubusercontent.com/misode/mcmeta/{minecraft_version}-summary/item_components/data.json"
    item_components_file = ctx.cache["smithed.crafter"].download(url)
    with open(item_components_file) as f:
        item_components: dict[str, (list[Any] | dict[str,Any])] = json.load(f)

    commands: list[str] = []

    for item, components in item_components.items():
        if isinstance(components, list):
            components_dict = {x["type"]: x["value"] for x in components}
        else:
            components_dict = components

        max_damage = components_dict.get("minecraft:max_damage", None)
        if max_damage:
            command = delete_tool(ctx, item, max_damage)
            commands.append(command)

    ctx.data.functions[
        f"smithed.crafter:v{ctx.project_version}/block/table/crafting/output/clear_input/delete_tool/vanilla"
    ].append(mc.serialize(mc.parse("\n".join(commands), multiline=True)))