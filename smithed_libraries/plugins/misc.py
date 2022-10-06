from pathlib import Path

import yaml
from beet import Context

__all__ = ["update_files"]

library_versions = Path("latest.yaml")


def relay_config_values(ctx: Context):
    """Relays `meta.zip` -> `*_pack.zipped`"""

    ctx.data.zipped = ctx.assets.zipped = ctx.meta.get("zip", True)


def update_files(ctx: Context):
    """Produce other files which need information from builds

    Currently:
      - updates `latest.yaml`
    """

    yield

    if ctx.meta.get("release") and library_versions.exists():
        latest_versions = yaml.safe_load(library_versions.read_text())
        latest_versions[ctx.project_name] = ctx.project_version
        library_versions.write_text(yaml.safe_dump(latest_versions))
