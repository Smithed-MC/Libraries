import json
import os
import subprocess
from pathlib import Path
from typing import Any

import github_action_utils as gha
import yaml

# Load manifest
manifest = json.loads(Path("dist/manifest.json").read_text())
last_commit = manifest["last_commit"]

# Make sure the last commit is reachable, otherwise every pack would look new
subprocess.run(["git", "cat-file", "-e", f"{last_commit}^{{commit}}"], check=True)


def read_old_beet_yaml(beet_yaml_path: Path) -> Any | None:
    """Parse the "beet.yaml" file at the last commit, or None if the pack is new."""

    # Packs lived at the repo root before being moved under "src"
    for path in (beet_yaml_path, beet_yaml_path.relative_to("src")):
        try:
            data = subprocess.check_output(
                ["git", "show", f"{last_commit}:{path}"],
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            continue
        return yaml.safe_load(data.decode())

    return None


# Initialize the list of packs to build
packs: list[tuple[Path, str]] = []

# Get a list of all the packs in the "smithed_libraries/packs" directory
for pack in Path("src/smithed_libraries/packs").glob("*"):
    # Gather beet yaml path and parse it
    beet_yaml_path = pack / "beet.yaml"
    beet_yaml = yaml.safe_load(beet_yaml_path.read_text())
    old_beet_yaml = read_old_beet_yaml(beet_yaml_path)

    # Build new packs and packs whose version number has changed
    if old_beet_yaml is None or beet_yaml["version"] != old_beet_yaml["version"]:
        packs.append((pack, beet_yaml["version"]))

# Build the packs (if there are any to build)
if packs:
    subprocess.run(
        [
            "uv",
            "run",
            "--locked",
            "--no-default-groups",
            "--group",
            "github-workflows",
            "beet",
            "--log",
            "INFO",
            "-p",
            "beet-release.yaml",
            *[f"-s pipeline[0].broadcast[] = {pack}" for pack, _ in packs],
        ],
        check=True,
    )

build_changes = str(bool(packs)).lower()
built_packs = ",".join(f"{pack.stem}:{version}" for pack, version in packs)

if "GITHUB_ACTIONS" in os.environ:
    gha.set_output("build_changes", build_changes)
    gha.set_output("built_packs", built_packs)
else:
    print(f"{build_changes=}")
    print(f"{built_packs=}")
