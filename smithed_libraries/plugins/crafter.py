from beet import Context, ItemTag


def beet_default(ctx: Context):
    minecraft_version = ctx.meta["minecraft_version"]
    cache = ctx.cache["smithed_crafter"]

    all_items_url = f"https://raw.githubusercontent.com/misode/mcmeta/{minecraft_version}-registries/item/data.json"
    all_items = ItemTag(source_path=cache.download(all_items_url))
    all_items.data = {"values": all_items.data}

    ctx.generate("smithed.crafter:all", all_items)
