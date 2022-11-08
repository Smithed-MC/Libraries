import logging
import re
from contextlib import suppress
from functools import cache
from itertools import zip_longest
from typing import Any, ClassVar, cast

from beet import (
    Advancement,
    Context,
    Function,
    FunctionTag,
    ListOption,
    PackSelector,
    TextFileBase,
)
from beet.contrib.find_replace import find_replace
from beet.contrib.rename_files import RenderRenameOption, TextRenameOption, rename_files
from pydantic import BaseModel, Field, root_validator, validator

logger = logging.getLogger(__name__)

JsonType = str | int | float | bool | list["JsonType"] | dict[str, "JsonType"]
JsonDict = dict[str, "JsonType"]

PUBLIC_PAT = re.compile("^#>? @public")


VERSION_PART_NAMES = ["major", "minor", "patch"]
# print(version_part_names, next_step_names, list(step_pairs))


class Version(BaseModel):
    """Provides methods and fields for the version for ease of use"""

    version: str = Field(regex=r"\d+\.\d+\.\d+")

    major: int = -1
    minor: int = -1
    patch: int = -1

    @validator("version")
    def set_attributes(cls, value: str, values: dict[str, Any]):
        values |= dict(zip(VERSION_PART_NAMES, (int(part) for part in value.split())))
        return value

    @root_validator
    def ensure_version_parts(cls, values: dict[str, Any]):
        for key, val in values.items():
            if val < 0:
                raise ValueError(f"{key} had an invalid version value: {val}")

        return values

    def parts(self):
        yield self.major
        yield self.minor
        yield self.patch

    def named_parts(self):
        return zip(VERSION_PART_NAMES, self.parts())

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"


class VersioningModel(BaseModel, extra="forbid"):
    """The `versioning` config of `beet.yaml`"""

    class ApiOptions(BaseModel):
        implementation: str
        check: str

    ctx: ClassVar[Context]

    namespace: str = ""
    scoreholder: str = ""
    scheduled: ListOption[str] = ListOption()
    version: Version = ""  # type: ignore
    refactor: TextRenameOption | RenderRenameOption
    api: ApiOptions

    @validator("namespace", always=True)
    def init_namespace(cls, value: str):
        return cls.ctx.project_id

    @validator("scoreholder", always=True)
    def init_scoreholder(cls, value: str):
        return value or "#" + cls.ctx.project_id

    @validator("schedule", always=True)
    def init_schedule(cls, value: ListOption[str]):
        return value.entries or ListOption(__root__=["tick"])

    @validator("version", pre=True, always=True)
    def init_version(cls, value: str):
        return value or cls.ctx.project_version


def load_tags(ctx: Context, model: VersioningModel):
    """Sets the Lantern Load tags for deps, enumeration, and resolution"""

    ctx.data["load:load"] = FunctionTag({"values": [f"#{model.namespace}:load"]})

    ctx.data[f"{model.namespace}:load"] = FunctionTag(
        {
            "values": [
                {"id": f"#{model.namespace}:load/dependencies", "required": False},
                f"#{model.namespace}:load/enumerate",
                f"#{model.namespace}:load/resolve",
            ]
        }
    )


def clear_schedule_loops(namespace: str, version: str, scheduled: list[str]):
    """Ensures every schedule loop is disabled"""

    return "\n".join(
        f"schedule clear {namespace}:impl/{version}/technical/{function}"
        for function in scheduled
    )


def call_if_version_match(scoreholder: str, version: Version, path: str):
    """Generates a version check for `{namespace}:calls` functions

    Checks each versioning score exactly before running `impl` function.
    """

    inner_execute = " ".join(
        f"if score {scoreholder}.{name} load.status matches {part}"
        for name, part in version.named_parts()
    )

    return f"execute {inner_execute} run function {path}"


def resolve_func(ctx: Context, opts: VersioningModel):
    """Resolves the best version"""

    name = f"{opts.namespace}:calls/{opts.version}/technical/resolve"

    ctx.data[name] = Function(
        clear_schedule_loops(
            opts.namespace, str(opts.version), opts.scheduled.entries()
        )
        + call_if_version_match(
            opts.scoreholder,
            opts.version,
            f"{opts.namespace}:impl/{opts.version}/technical/load",
        )
    )

    ctx.data[f"{opts.namespace}:load/resolve"] = FunctionTag({"values": [name]})


def enumerate_step_name(namespace: str, version: Version, step: str):
    return f"{namespace}:calls/{version}/technical/enumerate/{step}"


def enumerate_func(ctx: Context, opts: VersioningModel):
    """The enumeration function which sets the best version"""

    name = f"{opts.namespace}:calls/{opts.version}/technical/enumerate"
    major = VERSION_PART_NAMES[0]

    ctx.data[name] = Function(
        f"scoreboard players reset {opts.scoreholder}.set load.status\n"
        + "".join(
            f"scoreboard players add {opts.scoreholder}.{name} load.status 0\n"
            for name in VERSION_PART_NAMES
        )
        + f"function {enumerate_step_name(opts.namespace, opts.version, major)}"
    )

    ctx.data[f"{opts.namespace}:load/enumerate"] = FunctionTag({"values": [name]})


def enumerate_step(
    ctx: Context,
    scoreholder: str,
    namespace: str,
    version: Version,
    step: str,
    next_step: str | None,
    value: int,
):
    """A single step in the enumerate function"""

    step_body = (
        "execute "
        f"if score {scoreholder}.{step} load.status matches ..{value} "
        f"unless score {scoreholder}.{step} load.status matches {value} "
        f"run function {set_version()}"
    )

    if next_step is not None:
        step_body += (
            "\n"
            "execute "
            f"unless score {scoreholder}.set load.status matches 1 "
            f"if score {scoreholder}.{step} load.status matches ..{value} "
            f"if score {scoreholder}.{step} load.status matches {value} "
            f"run function {enumerate_step_name(namespace, version, next_step)}"
        )

    ctx.data[enumerate_step_name(namespace, version, step)] = Function(step_body)


@cache
def set_version(ctx: Context, opts: VersioningModel):
    name = f"{opts.namespace}:calls/{opts.version}/technical/enumerate/set_version"

    ctx.data[name] = Function(
        "".join(
            f"scoreboard players set {opts.scoreholder}.{name} load.status {part}\n"
            for name, part in opts.version.named_parts()
        )
        + f"scoreboard players set {opts.scoreholder}.set load.status 1"
    )

    return name


def generate_call(ctx: Context, opts: VersioningModel, path: str):
    """Generates the actual call function that checks the version"""

    *_, versioned_path = path.split(f"/{opts.version}/")

    api_path = f"{opts.namespace}:{versioned_path}"
    call_path = path.replace(opts.api.implementation, opts.api.check)

    logger.debug("api: %s", api_path)

    ctx.data[api_path] = FunctionTag({"values": [call_path]})
    ctx.data[call_path] = Function(
        call_if_version_match(opts.scoreholder, opts.version, path)
    )


def generate_api_calls(ctx: Context, opts: VersioningModel):
    """Generates API calls based on `@public` listed inside of function files

    TODO: Support @public on any line of the function doc comment
            https://github.com/SpyglassMC/Spyglass/wiki/IMP-Doc
    """

    for path in ctx.data.functions.match(opts.namespace):
        function = ctx.data.functions[path]

        if PUBLIC_PAT.match(function.lines[0]):
            generate_call(ctx, opts, path)


def resolve_advancements(ctx: Context, advancement: Advancement, opts: VersioningModel):
    """Adds version checking to advancement conditions"""

    criteria = advancement.data["criteria"]
    for requirement in criteria.values():
        conditions = requirement.setdefault("conditions", {})
        player_conditions = conditions.setdefault("player", [])

        for number, name in zip(opts.version.parts(), VERSION_PART_NAMES):
            scoreholder_part = f"{opts.scoreholder}.{name}"
            version_check = {
                "condition": "minecraft:value_check",
                "value": {
                    "type": "minecraft:score",
                    "target": {
                        "type": "minecraft:fixed",
                        "name": scoreholder_part,
                    },
                    "score": "load.status",
                },
                "range": number,
            }

            for cond in player_conditions:
                with suppress(KeyError):
                    if (
                        cond["condition"] == "minecraft:value_check"
                        and cond["value"]["target"]["name"] == scoreholder_part
                    ):
                        cond["range"] = number
                        break

            else:  # only when there's no break
                player_conditions.append(version_check)


def run(ctx: Context, opts: VersioningModel):
    """This is the main versioning plugin"""

    load_tags(ctx, opts)
    generate_api_calls(ctx, opts)  # TODO: use mecha

    # for files that match the selector, refactor and handle files
    pack_selector = PackSelector.from_options(match=opts.refactor.match)
    files = pack_selector.select_files(ctx.data, extend=TextFileBase[Any])

    for file, (_, path) in files.items():
        path = cast(str, path)  #

        if type(file) is Advancement:
            resolve_advancements(ctx, file, opts)

    # TODO: other load tags
    resolve_func(ctx, opts)
    enumerate_func(ctx, opts)

    enumerate_steps(ctx, opts)


def enumerate_steps(ctx: Context, opts: VersioningModel):
    """Generates the enumerate steps that the enumerate function calls"""

    for (step, part), next_step in zip_longest(
        opts.version.named_parts(), VERSION_PART_NAMES[1:]
    ):
        enumerate_step(
            ctx,
            opts.namespace,
            opts.scoreholder,
            opts.version,
            step,
            next_step,
            part,
        )


def smithed_cache(ctx: Context, opts: VersioningModel):
    """This only runs if the project is a Smithed library"""

    import json
    from pathlib import Path

    from smithed_libraries import commands

    pack = commands.LibraryManifest(
        id=opts.namespace,
        name=ctx.project_name,
        description=commands.flatten_component(ctx.project_description),
        version=str(opts.version),
    ).json()

    if (path := Path("manifest.json")).exists():
        manifest = json.loads(path.read_text())
    else:
        manifest = []

    manifest.append(pack)  # type: ignore

    path.write_text(json.dumps(manifest))


def beet_default(ctx: Context):
    """This plugins generates all the versioning requirements that LL needs

    When writing your data pack, you can ignore any versioning you need.
    This plugin will allow you to automatically version any implementation
      alongside with defining api via an `@public` at the top of the file.

    It will generate call function for any api route as defined in the config.
    """

    VersioningModel.ctx = ctx  # TODO: use `configurable` in pydantic v2
    opts = ctx.validate("smithed.versioning", VersioningModel)

    yield

    ctx.require(lambda ctx: run(ctx, opts))

    substitution = opts.refactor.dict()
    del substitution["match"]

    # dynamic renames
    ctx.require(
        find_replace(data_pack={"match": opts.refactor.match}, substitute=substitution)
    )
    ctx.require(rename_files(data_pack={"match": opts.refactor.match} | substitution))

    # we load this afterwards so that dynamic renames don't "touch" it
    ctx.require("beet.contrib.lantern_load.base_data_pack")

    if ctx.project_id.startswith("smithed."):  # TODO: maybe improve this check?
        ctx.require(lambda ctx: smithed_cache(ctx, opts))
