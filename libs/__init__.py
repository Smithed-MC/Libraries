from beet import Plugin, subproject
from importlib import resources

__all__ = [
    lib.name
    for lib in (resources.files("smithed") / "libs").iterdir()
]

WRAPPER_PLUGIN = lambda name: {"directory": f"@smithed/libs/{name}", "extend": "beet.yml"}


def __getattr__(name: str) -> Plugin:
    """Dynamically generates a plugin that creates a subproject for a library"""

    if name in __all__:
        return lambda ctx: ctx.require(subproject(WRAPPER_PLUGIN(name)))

    raise AttributeError(f"module 'smithed' has no plugin '{name}'")


def __dir__() -> list[str]:
    """Implements https://peps.python.org/pep-0562/"""

    return sorted(__all__)
