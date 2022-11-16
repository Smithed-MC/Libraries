# pyright: reportUnsupportedDunderAll=false

from beet import Plugin, subproject

from . import plugins

__version__ = "0.1.0"

__all__ = [
    "actionbar",
    "crafter",
    "crafter-addon",
    "custom-block",
    "damage",
    "enchanter",
    "item",
    "prevent-aggression",
    "plugins",
]


def __getattr__(name: str) -> Plugin:
    """Dynamically generates a plugin that creates a subproject for a library"""

    if name in __all__:
        return subproject({"extend": f"@{__package__}/packs/{name}/beet.yaml"})

    raise AttributeError(f"module {__package__!r} has no plugin {name!r}")


def __dir__() -> list[str]:
    """Implements https://peps.python.org/pep-0562/"""

    return sorted(__all__)
