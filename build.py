from beet import Context, subproject
from pathlib import Path

import logging

logger = logging.getLogger("build")
logger.setLevel("INFO")


def beet_default(ctx: Context):
    libraries = ctx.meta.get('libraries', [])
    zip = ctx.meta.get('zip', True)
    items = Path("libs").iterdir()

    filtered = filter(lambda item: (item.name in libraries) if libraries else True, items)

    for file in filtered:
        if file.is_dir():
            try:
                logger.info("Building Project %s", file)

                ctx.require(
                    subproject(
                        {
                            "directory": str(file),
                            "output": "../../dist",
                            "require": [
                                "default.versioning",
                                "beet.contrib.dbg",
                                "beet.contrib.dundervar"
                            ],
                            "extend": ["beet.yaml"],
                            "pipeline": [
                                "beet.contrib.lantern_load.base_data_pack"
                            ],
                            "data_pack": {"zipped": zip},
                            "resource_pack": {"zipped": zip},
                        }
                    )
                )

            except Exception as err:
                logger.exception(err)
