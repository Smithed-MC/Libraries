import json
import subprocess
from pathlib import Path

from beet import Context


def collect_version(ctx: Context):
    ctx.cache["version_manifest"].json[ctx.project_id] = ctx.project_version


def output_version_manifest(ctx: Context):
    manifest: Path = ctx.directory / "dist" / "manifest.json"
    manifest.parent.mkdir(exist_ok=True, parents=True)

    versions = json.loads(manifest.read_text()) if manifest.exists() else {}
    versions |= ctx.cache["version_manifest"].json

    if not manifest.exists():
        manifest.touch()

    hash = subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"]).decode()
    versions["last_commit"] = hash.strip()

    manifest.write_text(json.dumps(versions, indent=2))
