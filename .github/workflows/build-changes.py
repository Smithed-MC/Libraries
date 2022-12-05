import json
import os
import subprocess
from pathlib import Path

import yaml

# Load manifest
manifest = json.loads(Path("dist/manifest.json").read_text())
last_commit = manifest["last_commit"]

# Initialize the list of packs to build
broadcast = []

# Get a list of all the packs in the "smithed_libraries/packs" directory
for pack in Path("smithed_libraries/packs").glob("*"):
    # Gather beet yaml path and parse it
    beet_yaml_path = pack / "beet.yaml"
    beet_yaml = yaml.safe_load(beet_yaml_path.read_text())

    # Parse the "beet.yaml" file for the previous commit
    old_beet_yaml = yaml.safe_load(
        subprocess.check_output(
            ["git", "show", f"{last_commit}:" + str(beet_yaml_path)]
        ).decode()
    )

    # Check if the pack's version number has changed and add pack to list of builds
    if beet_yaml["version"] != old_beet_yaml["version"]:
        broadcast.append(f"-s pipeline[0].broadcast[] = {pack}")


# Build the packs (if there are any to build)
os.environ["GITHUB_OUTPUT"] = f"packs="
if broadcast:
    subprocess.run(
        [
            "poetry",
            "run",
            "beet",
            "--log",
            "INFO",
            "-p",
            "beet-release.yaml",
            *broadcast,
        ]
    )
    os.environ["GITHUB_OUTPUT"] += ", ".join(broadcast)
