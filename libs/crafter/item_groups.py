from beet import Context, JsonFile


class ItemGroups(JsonFile):
    scope = ("item_groups",)
    extension = ".json"


def beet_default(ctx: Context):
    ctx.data.extend_namespace.append(ItemGroups)
