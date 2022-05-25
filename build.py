from beet import Context, subproject
from pathlib import Path

import logging

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def beet_default(ctx: Context):
    libraries = ctx.meta.get("libraries", [])
    zip = ctx.meta.get("zip", True)
    items = Path("libs").iterdir()

    filtered = filter(
        lambda item: ((item.name in libraries)) if libraries else (item.name != 'template'), items
    )

    for file in filtered:
        if file.is_dir():
            try:
                logger.info("Building Project %s", file)

                ctx.require(
                    subproject(
                        {
                            "directory": str(file),
                            "output": "../../dist",
                            "extend": ["beet.yaml"],
                            "require": [
                                "default.versioning",
                                "beet.contrib.dbg",
                                "beet.contrib.dundervar",
                            ],
                            "pipeline": [
                                "mecha",
                                "beet.contrib.render",
                                "beet.contrib.lantern_load.base_data_pack"
                            ],
                            "data_pack": {"zipped": zip},
                            "resource_pack": {"zipped": zip},
                            "meta": {
                                "render": {
                                    "data_pack": {"functions": ["smithed.*"]}
                                }
                            }
                        }
                    )
                )

            except Exception as err:
                logger.exception(err)
