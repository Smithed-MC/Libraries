import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, NamedTuple

import requests
import yaml


class PackVersion(NamedTuple):
    pack: str
    version: str


packs_root = Path("src/smithed_libraries/packs")
minecraft_version = str(yaml.safe_load(Path("beet.yaml").read_text())["minecraft"])

get_url = "https://api.smithed.dev/v2/packs/{pack}"
create_url = (
    f"https://api.smithed.dev/v2/packs?&id={{pack}}&token={os.environ['SMITHED_TOKEN']}"
)
post_url = (
    "https://api.smithed.dev/v2/packs/{pack}/versions?"
    "&version={version}"
    f"&token={os.environ['SMITHED_TOKEN']}"
)
download_url = (
    "https://github.com/Smithed-MC/Libraries/blob/"
    "{commit_hash}/{version}/{pack}/smithed_{pack}_{type}.zip?raw=true"
)
source_url = (
    "https://github.com/Smithed-MC/Libraries/blob/main/"
    "src/smithed_libraries/packs/{pack}/{file}?raw=true"
)

headers = {"Content-Type": "application/json"}

payload_template: Any = {
    "name": "",
    "breaking": True,
    "downloads": {"datapack": ""},
    "supports": [],
    "dependencies": [],
}

packs = [
    PackVersion(*pack.strip().split(":"))
    for pack in os.environ["BUILT_PACKS"].split(",")
]


def ensure_pack_exists(pack: str, beet: Any, first_version: Any) -> bool:
    """Create the pack on smithed if it doesn't exist yet.

    Smithed requires at least one version on creation, so the pack is created with
    `first_version`. Returns True if it was, meaning the version is already uploaded.
    """

    try:
        resp = requests.get(url=get_url.format(pack=pack), timeout=30)
    except requests.RequestException as exc:
        raise SystemExit(f"Failed to fetch {pack}: {type(exc).__name__}") from None

    if resp.status_code != 404:
        if not 200 <= resp.status_code < 300:
            raise SystemExit(f"Failed to fetch {pack}: HTTP {resp.status_code}")
        return False

    readme = packs_root / pack / "README.md"
    pack_data = {
        "id": pack,
        "display": {
            "name": beet["name"].removeprefix("Smithed "),
            "description": beet.get("description", ""),
            "icon": source_url.format(pack=pack, file="pack.png"),
            "hidden": False,
            "webPage": (
                source_url.format(pack=pack, file="README.md")
                if readme.exists()
                else ""
            ),
        },
        "versions": [first_version],
        "categories": ["Library"],
    }

    try:
        resp = requests.post(
            url=create_url.format(pack=pack),
            headers=headers,
            data=json.dumps({"data": pack_data}),
            timeout=30,
        )
    except requests.RequestException as exc:
        raise SystemExit(f"Failed to create {pack}: {type(exc).__name__}") from None

    print(resp.text)
    # 409 means the pack was created in the meantime, so the version still needs
    # to be uploaded
    if resp.status_code == 409:
        return False
    if not 200 <= resp.status_code < 300:
        raise SystemExit(f"Failed to create {pack}: HTTP {resp.status_code}")
    return True


# upload packs to smithed
for pack, version in packs:
    # load in beet file from pack directory
    beet = yaml.safe_load((packs_root / pack / "beet.yaml").read_text())

    payload = deepcopy(payload_template)

    payload["name"] = version

    payload["downloads"]["datapack"] = download_url.format(
        commit_hash=os.environ["COMMIT_HASH"],
        version=minecraft_version,
        pack=pack.replace("-", "_"),
        type="dp",
    )
    if "resource_pack" in beet:
        payload["downloads"]["resourcepack"] = download_url.format(
            commit_hash=os.environ["COMMIT_HASH"],
            version=minecraft_version,
            pack=pack.replace("-", "_"),
            type="rp",
        )

    payload["supports"] = [minecraft_version]

    # assemble deps from beet file
    payload["dependencies"] = [
        {"id": f"{dependency}", "version": version}
        for dependency, version in beet.get("meta", {}).get("depends_on", {}).items()
    ]

    if ensure_pack_exists(pack, beet, payload):
        continue

    # send post request
    try:
        resp = requests.post(
            url=post_url.format(pack=pack, version=version),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"data": payload}),
            timeout=30,
        )
    except requests.RequestException as exc:
        raise SystemExit(
            f"Failed to upload {pack}@{version}: {type(exc).__name__}"
        ) from None

    print(resp.text)
    if not 200 <= resp.status_code < 300:
        raise SystemExit(f"Failed to upload {pack}@{version}: HTTP {resp.status_code}")
