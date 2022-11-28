import json

from beet import Context


def collect_version(ctx: Context):
    ctx.cache["version_manifest"].json[ctx.project_id] = ctx.project_version


def output_version_manifest(ctx: Context):
    manifest = ctx.meta["broadcast_directory"] / "dist" / "manifest.json"
    manifest.write_text(
        json.dumps(ctx.cache["version_manifest"].json, indent=2)
    )
