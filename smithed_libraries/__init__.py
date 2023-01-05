# pyright: reportUnsupportedDunderAll=false

from beet import subproject

from . import plugins

__version__ = "0.2.1"

__all__ = [
    "actionbar",
    "crafter",
    "crafter-addon",
    "custom-block",
    "damage",
    "enchanter",
    "item",
    "prevent-aggression",
]

# We dynamically generate plugins for all of our inner packs
# Each pack requires a subproject that extends the inner config
for pack in __all__:
    globals()[pack] = subproject({"extend": f"@{__package__}/packs/{pack}/beet.yaml"})

__all__.append("plugins")  # internal / normal beet plugins
