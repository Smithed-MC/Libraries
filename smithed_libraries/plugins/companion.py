from beet import Context, JsonFile


class ItemGroups(JsonFile):
    scope = ("item_groups",)
    extension = ".json"


def item_groups(ctx: Context):
    """Item Groups allow the companion mod to display items in the creative menu"""

    ctx.data.extend_namespace.append(ItemGroups)


def beet_default(ctx: Context):
    """This plugin enables behavior which benefits the companion mod

    Enables the following:
      - Item Groups
    """

    ctx.require(item_groups)
