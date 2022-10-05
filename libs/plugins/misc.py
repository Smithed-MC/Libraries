from beet import Context
from pathlib import Path

import yaml

__all__ = ["update_files"]

library_versions = Path("latest.yaml")


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
