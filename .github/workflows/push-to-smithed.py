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

post_url = (
    "https://api.smithed.dev/v2/packs/{pack}/versions?"
    "&version={version}"
    f"&token={os.environ['SMITHED_TOKEN']}"
)
download_url = (
    "https://github.com/Smithed-MC/Libraries/blob/"
    "{commit_hash}/{version}/{pack}/smithed_{pack}_{type}.zip?raw=true"
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
