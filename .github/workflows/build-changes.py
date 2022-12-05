import os
import subprocess
from pathlib import Path

import yaml

# Initialize the list of packs to build
broadcast = []

# Get a list of all the packs in the "smithed_libraries/packs" directory
for pack in Path("smithed_libraries/packs").glob("*"):
    # Get the "beet.yaml" file for the pack
    beet_yaml_path = pack / "beet.yaml"

    # Parse the "beet.yaml" file for the current commit using the pyyaml library
    with open(beet_yaml_path) as f:
        beet_yaml = yaml.safe_load(f)

    # Get the version number of the pack from the "beet.yaml" file for the current commit
    pack_version = beet_yaml["version"]
    
    last_commit = beet_yaml["last_commit"]

    # Parse the "beet.yaml" file for the previous commit using the pyyaml library
    old_beet_yaml = yaml.safe_load(
        subprocess.check_output(
            ["git", "show", f"{last_commit}:" + str(beet_yaml_path)]
        ).decode()
    )

    # Get the version number of the pack from the "beet.yaml" file for the previous commit
    old_pack_version = old_beet_yaml["version"]

    # Check if the pack's version number has changed
    if pack_version != old_pack_version:
        # Add the pack to the list of packs to build
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
