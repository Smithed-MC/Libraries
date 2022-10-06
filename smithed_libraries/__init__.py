from importlib import resources

from beet import Plugin, subproject

from . import plugins

__all__ = [
    *(
        lib.name
        for lib in (resources.files(__package__) / "packs").iterdir()
        if lib.is_dir()
    ),
    "plugins",
]

WRAPPER_PLUGIN = lambda name: {
    "directory": f"@smithed/libs/{name}",
    "extend": "beet.yml",
}


def __getattr__(name: str) -> Plugin:
    """Dynamically generates a plugin that creates a subproject for a library"""

    if name in __all__:
        return lambda ctx: ctx.require(subproject(WRAPPER_PLUGIN(name)))

    raise AttributeError(f"module {__package__!r} has no plugin {name!r}")


def __dir__() -> list[str]:
    """Implements https://peps.python.org/pep-0562/"""

    return sorted(__all__)
