# Libraries

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Discord](https://img.shields.io/discord/511303648119226382?color=%236d82cc&label=Discord&logo=discord&logoColor=white)](https://discord.gg/gkp6UqEUph)

> Collection of Libraries for the Smithed Ecosystem

## Downloading

You can download it from [Stable](https://smithed.dev/libraries) | [Nightly](https://nightly.link/Smithed-MC/Libraries/workflows/nightly-build/main/packs.zip)<br/>
or<br/>
You can build it from source using the [beet](https://github.com/mcbeet/beet) via the [Contributing](#contributing) instructions.

### Contributing

Contributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. This project uses [poetry](https://python-poetry.org/) and [beet](https://mcbeet.dev) for building and publishing to pypi.

```bash
$ git clone https://github.com/Smithed-MC/Libraries
$ cd Libraries && poetry install
$ beet  # Builds all libraries by default
# or
$ beet -s "broadcast = smithed_libraries/packs/damage"
```

The code follows the [black](https://github.com/psf/black) code style. Import statements are sorted with [isort](https://pycqa.github.io/isort/).

```bash
$ poetry run isort libs
$ poetry run black libs
$ poetry run black --check libs
```
