import os
from beet import Context, subproject
from pathlib import Path

import logging

import yaml

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def beet_default(ctx: Context):
    libraries = ctx.meta.get("libraries", [])
    zip = ctx.meta.get("zip", True)
    release = ctx.meta.get("release", False)
    
    items = Path("libs").iterdir()

    filtered = filter(
        lambda item: ((item.name in libraries)) if libraries else (item.name != 'template'), items
    )
    
    if(release): 
        if os.path.isfile("latest.yaml"):
            latest = yaml.load(open("latest.yaml", "r+"), Loader=yaml.FullLoader)
        else:
            latest = {}

    for file in filtered:
        if file.is_dir():
            try:
                logger.info("Building Project %s", file)
                output = "../../dist"
                if release:
                    config = yaml.load(open(str(file) + "/beet.yaml", "r"), Loader=yaml.FullLoader)
                    output += "/v" + config["version"]
                    latest[config["name"]] = config["version"]


                ctx.require(
                    subproject(
                        {
                            "directory": str(file),
                            "output": output,
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
                
    if(release):
        with open("latest.yaml", "w+") as f:
            yaml.dump(latest, f)
