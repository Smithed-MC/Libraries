from beet import Context, subproject
from pathlib import Path

import logging

logger = logging.getLogger("build")
logger.setLevel("INFO")


def beet_default(ctx: Context):
    libraries = ctx.meta.get('libraries', [])
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
                                "default.dbg",
                                "beet.contrib.dundervar"
                            ],
                            "extend": ["beet.yaml"],
                            "pipeline": [
                                "beet.contrib.lantern_load.base_data_pack"
                            ],
                            "data_pack": {"zipped": False},
                            "resource_pack": {"zipped": False},
                        }
                    )
                )

            except Exception as err:
                logger.exception(err)
