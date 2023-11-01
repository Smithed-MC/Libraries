import requests
from beet import Context, ItemTag


def cache_item_list(ctx: Context, cache_identifier: str):
    url = f"https://raw.githubusercontent.com/misode/mcmeta/{ctx.minecraft_version}-registries/item/data.json"
    r = requests.get(url)
    if not r.ok:
        raise Exception(f"Failed to get {url}")
    data = r.json()
    ctx.cache.json[cache_identifier] = data


def beet_default(ctx: Context):
    cache_identifier = f"item_list@{ctx.minecraft_version}"
    if cache_identifier not in ctx.cache.json:
        cache_item_list(ctx, cache_identifier)

    ctx.data.item_tags["smithed.crafter:all"] = ItemTag(
        {"values": ctx.cache.json[cache_identifier]}
    )
