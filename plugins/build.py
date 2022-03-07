from beet import Context, subproject
from pathlib import Path

def beet_default(ctx: Context):
    for file in Path('libs').iterdir():
        if file.is_dir():
            ctx.require(
                subproject(
                    {
                        "directory": str(file),
                        "extend": ["beet.yaml"],
                        "output": "../dist",
                        "data_pack": {"zipped": True},
                        "resource_pack": {"zipped": True}
                    }
                )
            )
