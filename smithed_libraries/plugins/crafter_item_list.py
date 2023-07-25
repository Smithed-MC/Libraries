import requests
from beet import Context, ErrorMessage, ItemTag


def beet_default(ctx: Context):
    "Get the tag #smithed.crafter:all with a list of all items from misode/mcmeta repo."

    if not "smithed.all_item_list" in ctx.cache.json:
        item_url = "https://raw.githubusercontent.com/misode/mcmeta/{version}-registries/item/data.json"
        response = requests.get(
            url=item_url.format(version=ctx.meta["crafter_mc_version"])
        )

        if response.status_code == 200:
            item_tag = {"values": response.json()}
            ctx.data.item_tags["smithed.crafter:all"] = ItemTag()
            ctx.data.item_tags["smithed.crafter:all"].data = item_tag
            ctx.cache.json["smithed.all_item_list"] = item_tag
        else:
            raise ErrorMessage(
                f"Failed to get item list from {item_url.format(version=ctx.meta['crafter_mc_version'])}"
            )
    else:
        ctx.data.item_tags["smithed.crafter:all"] = ItemTag()
        ctx.data.item_tags["smithed.crafter:all"].data = ctx.cache.json[
            "smithed.all_item_list"
        ]
