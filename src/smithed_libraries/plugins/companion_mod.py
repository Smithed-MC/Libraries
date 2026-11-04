from typing import ClassVar

from beet import Context, JsonFile, NamespaceFileScope


class ItemGroup(JsonFile):
    scope: ClassVar[NamespaceFileScope] = ("item_groups",)
    extension: ClassVar[str] = ".json"


def item_groups(ctx: Context):
    """Item Groups allow the companion mod to display items in the creative menu"""

    ctx.data.extend_namespace.append(ItemGroup)


def beet_default(ctx: Context):
    """This plugin enables behaviors which are implemented in the companion mod

    Enables the following:
      - Item Groups
    """

    ctx.require(item_groups)
