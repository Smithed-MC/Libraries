from beet import Context, ContextIntProvider, ContextIntProviderTag, Predicate, PredicateTag
from beet.contrib.find_replace import find_replace
from beet.contrib.rename_files import rename_files

from .api import generate_api
from .load import generate_load
from .models import ContextualModel, Versioning


def inject_version(ctx: Context):
    opts = ctx.inject(Versioning).opts

    # forward nested beet options directly instead of serializing their defaults.
    substitution = dict(opts.refactor)
    del substitution["match"]

    # dynamic renames
    ctx.require(
        find_replace(data_pack={"match": opts.refactor.match}, substitute=substitution)
    )
    ctx.require(rename_files(data_pack={"match": opts.refactor.match} | substitution))


def pack_enabled_tags(ctx: Context):
    opts = ctx.inject(Versioning).opts
    for name, part in opts.version.named_parts():
        ctx.data[f"{opts.namespace}:impl/internal/{name}"] = ContextIntProvider(str(part))
    ctx.data[f"{opts.namespace}:impl/major"] = ContextIntProvider({
        "type": "minecraft:max",
        "inputs": f"{opts.namespace}:impl/internal/major"
    })
    ctx.data[f"{opts.namespace}:impl/minor"] = ContextIntProvider({
        "type": "minecraft:conditional",
        "condition": {
            "type": "minecraft:int_value_check",
            "value": {
                "type": "minecraft:max",
                "inputs": f"#{opts.namespace}:major"
            },
            "test": f"{opts.namespace}:impl/internal/major"
        },
        "on_true": f"{opts.namespace}:impl/internal/minor",
        "on_false": -1
    })
    ctx.data[f"{opts.namespace}:impl/patch"] = ContextIntProvider({
        "type": "minecraft:conditional",
        "condition": {
            "type": "minecraft:int_value_check",
            "value": {
                "type": "minecraft:max",
                "inputs": f"#{opts.namespace}:major"
            },
            "test": f"{opts.namespace}:impl/internal/major"
        },
        "on_true": {
            "type": "minecraft:conditional",
            "condition": {
                "type": "minecraft:int_value_check",
                "value": {
                    "type": "minecraft:max",
                    "inputs": f"#{opts.namespace}:minor"
                },
                "test": f"{opts.namespace}:impl/internal/minor"
            },
            "on_true": f"{opts.namespace}:impl/internal/patch",
            "on_false": -1
        },
        "on_false": -1
    })

    for name, part in opts.version.named_parts():
        ctx.data[f"{opts.namespace}:{name}"] = ContextIntProviderTag({
            "values": [
                f"{opts.namespace}:impl/{name}"
            ]
        })

    ctx.data[f"{opts.namespace}:installed"] = Predicate({
        "type": "minecraft:random_chance",
        "chance": 1,
    })
    ctx.data[f"{opts.namespace}:installed"] = PredicateTag({
        "values": [
            f"{opts.namespace}:installed"
        ]
    })



def beet_default(ctx: Context):
    """This plugins generates all the versioning requirements that LL needs

    When writing your data pack, you can ignore any versioning you need.
    This plugin will allow you to automatically version any implementation
      alongside with defining APIs via an `@public` at the top of the file.

    It will generate call function for any api route as defined in the config.
    """

    ContextualModel.ctx = ctx  # TODO: use `configurable` in pydantic v2

    # all things for lantern load impl
    ctx.require(generate_load)

    # generate Pack Enabled Tags convention
    ctx.require(pack_enabled_tags)

    # refactors file names and paths to inject version
    ctx.require(inject_version)

    # we generate api bindings **after** refactoring
    ctx.require(generate_api)

    # we load this afterwards so that dynamic renames don't "touch" it
    ctx.require("beet.contrib.lantern_load.base_data_pack")
