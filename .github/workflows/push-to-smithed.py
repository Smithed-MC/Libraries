import json
import os
from pathlib import Path
from typing import Any, NamedTuple

import requests
import yaml


class PackVersion(NamedTuple):
    pack: str
    version: str


packs_root = Path("smithed_libraries/packs")

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
    payload = payload_template.copy()

    payload["name"] = version

    payload["downloads"]["datapack"] = download_url.format(
        commit_hash=os.environ["COMMIT_HASH"],
        version=os.environ["MC_VERSION"],
        pack=pack.replace("-", "_"),
        type="dp",
    )
    if "resource_pack" in beet:
        payload["downloads"]["resourcepack"] = download_url.format(
            commit_hash=os.environ["COMMIT_HASH"],
            version=os.environ["MC_VERSION"],
            pack=pack.replace("-", "_"),
            type="rp",
        )

    payload["supports"] = [os.environ["MC_VERSION"]]

    # assemble deps from beet file
    payload["dependencies"] = [
        {"id": f"{dependency}", "version": version}
        for dependency, version in beet.get("meta", {}).get("depends_on", {}).items()
    ]

    # send post request
    resp = requests.post(
        url=post_url.format(pack=pack, version=version),
        headers={"Content-Type": "application/json"},
        data=json.dumps({"data": payload}),
    )

    print(resp.text)
    if resp.status_code != 200:
        print(f"{resp.status_code=} ⚠️ UPLOAD ERROR ⚠️")
        print(f"{pack=} {version=}")
        print(f"{payload=}")
