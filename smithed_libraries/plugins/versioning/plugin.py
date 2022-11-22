from beet import Context
from beet.contrib.find_replace import find_replace
from beet.contrib.rename_files import rename_files

from .api import generate_api
from .load import generate_load
from .models import ContextualModel, Versioning



def inject_version(ctx: Context):
    opts = ctx.inject(Versioning).opts

    substitution = opts.refactor.dict()
    del substitution["match"]

    # dynamic renames
    ctx.require(
        find_replace(data_pack={"match": opts.refactor.match}, substitute=substitution)
    )
    ctx.require(rename_files(data_pack={"match": opts.refactor.match} | substitution))


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

    # refactors file names and paths to inject version
    ctx.require(inject_version)

    # we generate api bindings **after** refactoring
    ctx.require(generate_api)

    # we load this afterwards so that dynamic renames don't "touch" it
    ctx.require("beet.contrib.lantern_load.base_data_pack")
