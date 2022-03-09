from beet import Context, subproject
from pathlib import Path

import logging

logger = logging.getLogger("build")
logger.setLevel("INFO")


def beet_default(ctx: Context):
    for file in Path("libs").iterdir():
        if file.is_dir():
            try:
                logger.info("Building Project %s", file)

                ctx.require(
                    subproject(
                        {
                            "directory": str(file),
                            "extend": ["beet.yaml"],
                            "output": "../../dist",
                            "pipeline": [
                                "beet.contrib.lantern_load.base_data_pack",
                                "default.versioning",
                                "beet.contrib.dundervar",
                            ],
                            "data_pack": {"zipped": True},
                            "resource_pack": {"zipped": True},
                        }
                    )
                )

            except Exception as err:
                logger.exception(err)
