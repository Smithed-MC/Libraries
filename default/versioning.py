from typing import Optional

from beet.library.data_pack import Function, FunctionTag
from beet.toolchain.context import Context

import logging

logger = logging.getLogger(__name__)

version_part_names: list[str] = ["major", "minor", "patch"]
next_step_names = [*version_part_names[1:], None]
step_pairs = zip(version_part_names, next_step_names)
# print(version_part_names, next_step_names, list(step_pairs))


def combine_part_names(format: str):
    return "".join(format.format(name=name) for name in version_part_names)


def combine_parts(format: str, version_parts):
    return "".join(
        format.format(name=name, part=part)
        for name, part in zip(version_part_names, version_parts)
    )

def clear_schedule_loops(namespace, version, scheduled):
    func = ""
    for function in scheduled:
        func += f"schedule clear {namespace}:impl/{version}/technical/{function}\n"
    return func

def call_if_version_match(scoreholder, version_parts, path):
    return (
        "execute "
        + combine_parts(
            f"if score {scoreholder}.{{name}} load.status matches {{part}} ",
            version_parts,
        )
        + f"run function {path}"
    )


def resolve(ctx: Context, namespace, version, scoreholder, version_parts, scheduled):
    name = f"{namespace}:calls/{version}/technical/resolve"

    ctx.data[name] = Function(
        clear_schedule_loops(namespace, version, scheduled)
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
        "execute "
        f"if score {scoreholder}.{step} load.status matches ..{value} "
        f"unless score {scoreholder}.{step} load.status matches {value} "
        f"run function {set_version_func}"
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


def set_version(ctx: Context, namespace, scoreholder, version, version_parts):
    name = f"{namespace}:calls/{version}/technical/enumerate/set_version"

    ctx.data[name] = Function(
        combine_parts(
            f"scoreboard players set {scoreholder}.{{name}} load.status {{part}}\n",
            version_parts,
        )
        + f"\nscoreboard players set {scoreholder}.set load.status 1"
    )

    return name


def replace_version(ctx: Context, namespace, version):
    # TODO: Potentially ctx.data.values() might implement multiple namespaces
    for container in ctx.data[namespace].values():
        for path in list(container):
            container[path.replace(f"__version__", version)] = container.pop(path)


def generate_call(
    ctx: Context,
    path: str,
    version: str,
    version_parts,
    namespace: str,
    scoreholder: str,
):
    api_path = f"{namespace}:{path.split(version)[1][1:]}"
    call_path = path.replace("impl", "calls")

    logger.debug("api: %s", api_path)

    ctx.data[api_path] = FunctionTag({"values": [call_path]})
    ctx.data[call_path] = Function(
        call_if_version_match(scoreholder, version_parts, path)
    )


def generate_api_calls(ctx: Context, version, version_parts, namespace, scoreholder):
    for path in ctx.data.functions.match(f"{namespace}:impl"):
        # TODO: Support @public on any line of the function doc comment: https://github.com/SpyglassMC/Spyglass/wiki/IMP-Doc
        first_line = ctx.data.functions[path].text.split("\n")[0]
        if first_line.startswith("#") and "@public" in first_line:
            generate_call(ctx, path, version, version_parts, namespace, scoreholder)


def resolve_json(d, version):
    if isinstance(d, list):
        i = 0
        for v in d:
            if isinstance(v, str) and "__version__" in v:
                d[i] = v.replace("__version__", version)
            elif isinstance(v, dict) or isinstance(v, list):
                resolve_json(v, version)
            i += 1
    else:
        for k, v in d.items():
            if isinstance(v, str) and "__version__" in v:
                d[k] = v.replace("__version__", version)
            elif isinstance(v, dict) or isinstance(v, list):
                resolve_json(v, version)

def resolve_advancements(ctx: Context, version, version_parts, namespace, scoreholder):
    # breakpoint()
    for path in ctx.data.advancements.match(f"{namespace}:impl"):
        adv = ctx.data.advancements[path]

        resolve_json(adv.data, version)
        
        # add version checking to advancement conditions
        criteria = adv.data["criteria"]
        for requirement in criteria:
            try:
                player_conditions = criteria[requirement]["conditions"]["player"]
            except:
                try:
                    criteria[requirement]["conditions"]["player"] = []
                    player_conditions = criteria[requirement]["conditions"]["player"]
                except:
                    criteria[requirement]["conditions"] = {"player":[]}
                    player_conditions = criteria[requirement]["conditions"]["player"]
            
            i = 0
            for part in version_part_names:
                found = False
                scoreholder_part = f"{scoreholder}.{part}"
                version_check = {
                                    "condition": "minecraft:value_check",
                                    "value": {
                                        "type": "minecraft:score",
                                        "target": {
                                            "type": "minecraft:fixed",
                                            "name": scoreholder_part
                                        },
                                        "score": "load.status"
                                    },
                                    "range": int(version_parts[i])
                                }
                                
                for condition in player_conditions:
                    try:
                        if condition["condition"] == "minecraft:value_check" and \
                        condition["value"]["target"]["name"] == scoreholder_part:
                            condition["range"] = int(version_parts[i])
                            found = True
                    except:
                        pass
                if not found:
                    player_conditions.append(version_check)
                i+=1
            
def resolve_other(ctx: Context, version):
    # predicates
    for path in ctx.data.predicates:
        predicate = ctx.data.predicates[path]

        resolve_json(predicate.data, version)

    # loot tables
    for path in ctx.data.loot_tables:
        loot_table = ctx.data.loot_tables[path]

        resolve_json(loot_table.data, version)

    # block tags
    for path in ctx.data.block_tags:
        tag = ctx.data.block_tags[path]

        resolve_json(tag.data, version)

    # entity type tags
    for path in ctx.data.entity_type_tags:
        tag = ctx.data.entity_type_tags[path]

        resolve_json(tag.data, version)

    # item tags
    for path in ctx.data.item_tags:
        tag = ctx.data.item_tags[path]

        resolve_json(tag.data, version)

    # function tags
    for path in ctx.data.function_tags:
        tag = ctx.data.function_tags[path]

        resolve_json(tag.data, version)

    # item modifiers
    for path in ctx.data.item_modifiers:
        modifier = ctx.data.item_modifiers[path]

        resolve_json(modifier.data, version)

    # recipes
    for path in ctx.data.recipes:
        recipe = ctx.data.recipes[path]

        resolve_json(recipe.data, version)


def load_tags(ctx: Context, namespace):
    ctx.data["load:load"] = FunctionTag({"values": [f"#{namespace}:load"]})

    ctx.data[f"{namespace}:load"] = FunctionTag(
        {
            "values": [
                {"id": f"#{namespace}:load/dependencies", "required": False},
                f"#{namespace}:load/enumerate",
                f"#{namespace}:load/resolve",
            ]
        }
    )


def beet_default(ctx: Context):
    version = ctx.template.globals["version"] = f"v{ctx.project_version}"
    namespace: str = ctx.meta["versioning"]["namespace"]
    ctx.meta["generate_namespace"] = namespace
    ctx.meta["generate_prefix"] = f"impl/{version}"

    yield

    ctx.require(run)


def run(ctx: Context):
    version = ctx.template.globals["version"]
    namespace: str = ctx.meta["versioning"]["namespace"]
    scoreholder: str = ctx.meta["versioning"]["scoreholder"]
    version_parts: list[str] = ctx.project_version.split(".")
    try:
        scheduled: list[str] = ctx.meta["scheduled"]
    except:
        scheduled = []

    load_tags(ctx, namespace)

    replace_version(ctx, namespace, version)
    generate_api_calls(ctx, version, version_parts, namespace, scoreholder)
    resolve_advancements(ctx, version, version_parts, namespace, scoreholder)
    resolve_other(ctx, version)

    # TODO: other load tags
    resolve(ctx, namespace, version, scoreholder, version_parts, scheduled)
    enumerate(ctx, scoreholder, namespace, version)

    set_version_func = set_version(ctx, namespace, scoreholder, version, version_parts)

    for i in range(len(version_parts)):
        step = version_part_names[i]
        next_step = next_step_names[i]
        part = version_parts[i]

        # print(step, next_step)
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

