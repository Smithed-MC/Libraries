from .models import Version


def call_if_version_match(scoreholder: str, version: Version, path: str):
    """Generates a version check for `{opts.lantern_load.version_check}` functions

    Checks each versioning score exactly before running `impl` function.
    """

    inner_execute = " ".join(
        f"if score {scoreholder}.{name} load.status matches {part}"
        for name, part in version.named_parts()
    )

    return f"execute {inner_execute} run function {path}\n"
