from beet import Context


def beet_default(ctx: Context):
    """Relays `meta.zip` -> `*_pack.zipped`"""

    print("Building", ctx.project_name, ctx.project_version)

    if dir := ctx.output_directory:
        folder = ctx.project_id.partition(".")[-1]
        (dir / folder).mkdir(parents=True, exist_ok=True)
