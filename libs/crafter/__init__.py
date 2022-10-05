from beet import Context, subproject


def beet_default(ctx: Context):
    ctx.require(subproject({"directory": "@smithed/crafter", "extend": "beet.yml"}))
