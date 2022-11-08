from beet import Context


def beet_default(ctx: Context):
    """Relays `meta.zip` -> `*_pack.zipped`"""

    ctx.data.zipped = ctx.assets.zipped = ctx.meta.get("zip", True)
