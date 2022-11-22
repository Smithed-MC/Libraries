from contextlib import suppress

from beet import Advancement, Context, Function, FunctionTag, Generator

from .models import Versioning, VersioningOptions
from .utils import call_if_version_match


def load_tags(
    ctx: Context,
    opts: VersioningOptions,
    dependencies: str,
    enumerate: str,
    resolve: str,
):
    """Sets the Lantern Load tags for deps, enumeration, and resolution"""

    load_tag = ctx.generate(
        opts.lantern_load.tag_path,
        merge=FunctionTag(
            {
                "values": [
                    {"id": f"#{dependencies}", "required": False},
                    f"#{enumerate}",
                    f"#{resolve}",
                ]
            }
        ),
    )

    with ctx.override(generate_namespace="load", generate_prefix=""):
        ctx.generate(
            opts.lantern_load.step, merge=FunctionTag({"values": [f"#{load_tag}"]})
        )


def clear_schedule_loops(scheduled: list[str]):
    """Ensures every schedule loop is disabled"""

    return "".join(f"schedule clear {function}\n" for function in scheduled)


def resolve_func(ctx: Context, opts: VersioningOptions):
    """Resolves the best version"""

    schedules = [ctx.generate.path(path) for path in opts.scheduled_paths.entries()]

    resolve_function = ctx.generate[opts.lantern_load.function_path](
        "resolve",
        Function(
            clear_schedule_loops(schedules)
            + call_if_version_match(
                opts.scoreholder,
                opts.version,
                ctx.generate.path(opts.lantern_load.function_path),
            )
        ),
    )

    return ctx.generate[opts.lantern_load.tag_path](
        "resolve", merge=FunctionTag({"values": [resolve_function]})
    )


def set_version(generate: Generator, opts: VersioningOptions):
    return generate(
        "set_version",
        Function(
            "".join(
                f"scoreboard players set {opts.scoreholder}.{name} load.status {part}\n"
                for name, part in opts.version.named_parts()
            )
            + f"scoreboard players set {opts.scoreholder}.set load.status 1"
        ),
    )


def resolve_advancements(ctx: Context, opts: VersioningOptions):
    """Select packs that match refactor statement"""

    for advancement in ctx.select(match=opts.refactor.match, extend=Advancement):
        resolve_advancement(advancement, opts)


def resolve_advancement(advancement: Advancement, opts: VersioningOptions):
    """Adds version checking to advancement conditions

    We do this by adding new value checks to the criteria. Within the player
      conditions, we attempt to append our version_check OR edit the existing
      check for the correct scoreholder_part (TODO: make this clearer probably).
    """

    criteria = advancement.data["criteria"]
    for requirement in criteria.values():
        conditions = requirement.setdefault("conditions", {})
        player_conditions = conditions.setdefault("player", [])

        for name, number in opts.version.named_parts():
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
                with suppress(KeyError, TypeError):
                    if (
                        cond["condition"] == "minecraft:value_check"
                        and cond["value"]["target"]["name"] == scoreholder_part
                    ):
                        cond["range"] = number
                        break

            else:  # only when there's no break
                player_conditions.append(version_check)


def enumerate_func(ctx: Context, opts: VersioningOptions) -> str:
    """The enumeration function which sets the best version

    Enumeration works by chaining calls. First, we need to check the major
      version (or which ever is the highest one). If it's equivalent to our
      already highest version, then we go down to the next step.

    This goes until we've reached the end of each version step.
    """

    # context generators
    generate_function = ctx.generate[opts.lantern_load.function_path]
    generate_tag = ctx.generate[opts.lantern_load.tag_path]
    generate_enumerate = generate_function["enumerate"]

    set_version_path = set_version(generate_enumerate, opts)

    # We iterate through our version parts (we'll use major, minor, patch) **backwards**:
    #  `enumerate` calls major which calls minor which calls patch
    #  Make `enumerate/patch` first, return the path as the `last_step_function`
    #  Then make `enumerate/minor`, using `last_step_function`
    #  Finally, make `enumerate/major`..
    #  At the very end, `enerumate` can use the path of `enumerate/major`!
    last_step_function = None
    for step, value in reversed(opts.version.named_parts()):
        last_step_function = enumerate_step(
            generate_enumerate,
            opts.scoreholder,
            set_version_path,
            step,
            value,
            last_step_function,
        )

    enumerate_function = generate_function(
        "enumerate",
        Function(
            f"scoreboard players reset {opts.scoreholder}.set load.status\n"
            + "".join(
                f"scoreboard players add {opts.scoreholder}.{name} load.status 0\n"
                for name, _ in opts.version.named_parts()
            )
            + f"function {last_step_function}"
        ),
    )

    return generate_tag(
        "enumerate", merge=FunctionTag({"values": [enumerate_function]})
    )


def enumerate_step(
    generate: Generator,
    scoreholder: str,
    set_version_path: str,
    step: str,
    value: int,
    last_step_path: str | None,
):
    """A single step in the enumerate function

    A step cooresponds to a version part (major, minor, etc).
    """

    step_body = (
        "execute "
        f"if score {scoreholder}.{step} load.status matches ..{value} "
        f"unless score {scoreholder}.{step} load.status matches {value} "
        f"run function {set_version_path}"
    )

    if last_step_path is not None:
        step_body += (
            "\n"
            "execute "
            f"unless score {scoreholder}.set load.status matches 1 "
            f"if score {scoreholder}.{step} load.status matches ..{value} "
            f"if score {scoreholder}.{step} load.status matches {value} "
            f"run function {last_step_path}"
        )

    return generate(step, Function(step_body))


def generate_load(ctx: Context):
    """This is the main versioning plugin

    There are 3 parts to integrating lantern load for library support:
     - Basic load tags
        - Sets the step of the lantern load process to run everything else
     - Enumeration
        - Runs through every single pack of different versions
        - Sets the highest version amongst them all
     - Resolution
        - Uses highest version to run the correct load file
        - Disables the rest
    """

    opts = ctx.inject(Versioning).opts

    with ctx.override(generate_namespace=opts.namespace, generate_prefix=""):
        dependencies = ctx.generate[opts.lantern_load.tag_path].path("dependencies")

        # Enumeration starts on the main version part
        #  Then it checks sub-parts if the current part is the same
        enumerate = enumerate_func(ctx, opts)

        # Resolving involves using the highest version and booting off
        #  cooresponding resources while killing off others
        # Advancements get patched to "disable" if version check is **wrong**
        resolve = resolve_func(ctx, opts)
        resolve_advancements(ctx, opts)

        load_tags(ctx, opts, dependencies, enumerate, resolve)
