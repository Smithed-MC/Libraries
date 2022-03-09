from typing import Optional

from beet.library.data_pack import Function, FunctionTag
from beet.toolchain.context import Context

import logging

logger = logging.getLogger("versioning")

version_part_names: list[str] = ["major", "minor", "patch"]
next_step_names = [*version_part_names[1:], None]
step_pairs = zip(version_part_names, next_step_names)


def combine_part_names(format: str):
    return "".join(format.format(name=name) for name in version_part_names)


def combine_parts(format: str, version_parts):
    return "".join(
        format.format(name=name, part=part)
        for name, part in zip(version_part_names, version_parts)
    )


def call_if_version_match(scoreholder, version_parts, path):
    return (
        "execute "
        + combine_parts(
            f"if score {scoreholder}.{{name}} load.status matches {{part}} ",
            version_parts,
        )
        + f"run function {path}"
    )


def resolve(ctx: Context, namespace, version, scoreholder, version_parts):
    name = f"{namespace}:calls/{version}/technical/resolve"

    ctx.data[name] = Function(
        f"schedule clear {namespace}:impl/{version}/technical/tick\n"
        + call_if_version_match(
            scoreholder, version_parts, f"{namespace}:impl/{version}/technical/load"
        )
    )

    ctx.data[f"{namespace}:load/resolve"] = FunctionTag({"values": [name]})


def enumerate_step_name(namespace, version, step):
    return f"{namespace}:calls/{version}/technical/enumerate/{step}"


def enumerate(ctx: Context, scoreholder, namespace, version):
    name = f"{namespace}:calls/{version}/technical/enumerate"
    step = version_part_names[0]

    ctx.data[name] = Function(
        f"scoreboard players reset {scoreholder}.set load.status\n"
        + combine_part_names(
            f"scoreboard players add {scoreholder}.{{name}} load.status 0\n"
        )
        + f"function {enumerate_step_name(namespace, version, step)}"
    )

    ctx.data[f"{namespace}:load/enumerate"] = FunctionTag({"values": [name]})


def enumerate_step(
    ctx: Context,
    scoreholder,
    namespace,
    version,
    step,
    next_step: Optional[str],
    value,
    set_version_func,
):
    step_body = (
        "execute"
        f"if score {scoreholder}.{step} load.status matches ..{value} "
        f"unless score {scoreholder}.{step} load.status matches {value} "
        f"run function {set_version_func}"
    )

    if next_step is not None:
        step_body += (
            "\n"
            "execute"
            f"unless score {scoreholder}.set load.status matches 1 "
            f"if score {scoreholder}.{step} load.status matches ..{value} "
            f"if score {scoreholder}.{step} load.status matches {value} "
            f"run function {enumerate_step_name(namespace, version, next_step)}"
        )

    ctx.data[enumerate_step_name(namespace, version, step)] = Function(step_body)


def set_version(ctx: Context, namespace, scoreholder, version, version_parts):
    name = f"{namespace}:calls/{version}/technical/enumerate/set_version"

    ctx.data[name] = Function(
        combine_parts(
            f"scoreboard players set {scoreholder}.{{name}} load.status {{part}}",
            version_parts,
        )
        + f"scoreboard players set {scoreholder}.set load.status 1"
    )

    return name


def replace_version(ctx: Context, namespace, version):
    # TODO: Potentially ctx.data.values() might implement multiple namespaces
    for container in ctx.data[namespace].values():
        for path in list(container):
            if "__version__" not in path:
                container[path.replace(f"__version__", version)] = container.pop(path)


def generate_call(
    ctx: Context,
    path: str,
    version: str,
    version_parts,
    namespace: str,
    scoreholder: str,
):
    api_path = f"#{namespace}:{path.split(version)[1][1:]}"
    call_path = path.replace("impl", "calls")

    logger.info("api: %s", api_path)

    ctx.data[api_path] = FunctionTag({"values": [call_path]})
    ctx.data[call_path] = Function(
        call_if_version_match(scoreholder, version_parts, path)
    )


def generate_api_calls(ctx: Context, version, version_parts, namespace, scoreholder):
    for path in ctx.data.functions.match("impl"):
        # TODO: Support @public on any line of the function doc comment: https://github.com/SpyglassMC/Spyglass/wiki/IMP-Doc
        first_line = ctx.data.functions[path].text.split("\n")[0]
        if first_line.startswith("#") and "@public" in first_line:
            generate_call(ctx, path, version, version_parts, namespace, scoreholder)


def resolve_advancements(ctx: Context, version, version_parts, namespace, scoreholder):
    for path in ctx.data.advancements.match("impl"):
        if (adv := ctx.data.advancements[path]).get("__public__", False):
            adv["rewards"]["function"] = adv["rewards"]["function"].replace(
                "__version__", version
            )

            generate_call(ctx, path, version, version_parts, namespace, scoreholder)


def load_tags(ctx: Context, namespace):
    ctx.data["load:load"] = FunctionTag({"values": [f"#{namespace}:load"]})

    ctx.data[f"{namespace}:load"] = FunctionTag(
        {
            "values": [
                {"id": "#smithed.damage:load/dependencies", "required": False},
                "#smithed.damage:load/enumerate",
                "#smithed.damage:load/resolve",
            ]
        }
    )


def beet_default(ctx: Context):
    version = ctx.template.globals["version"] = f"v{ctx.project_version}"
    scoreholder: str = ctx.meta["versioning"]["scoreholder"]
    namespace: str = ctx.meta["versioning"]["namespace"]
    version_parts: list[str] = ctx.project_version.split(".")

    yield

    load_tags(ctx, namespace)

    replace_version(ctx, namespace, version)
    generate_api_calls(ctx, version, version_parts, namespace, scoreholder)
    resolve_advancements(ctx, version, version_parts, namespace, scoreholder)

    # TODO: other load tags
    resolve(ctx, namespace, version, scoreholder, version_parts)
    enumerate(ctx, scoreholder, namespace, version)

    set_version_func = set_version(ctx, namespace, scoreholder, version, version_parts)

    for (step, next_step), part in zip(step_pairs, version_parts):
        enumerate_step(
            ctx,
            scoreholder,
            namespace,
            version,
            step,
            next_step,
            part,
            set_version_func,
        )
