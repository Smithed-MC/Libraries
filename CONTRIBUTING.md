# Contributing
Contributions are welcome! Make sure to first open an issue discussing the problem or the new feature before creating a pull request. This project uses [uv](https://docs.astral.sh/uv/) and [beet](https://mcbeet.dev) for building and publishing to pypi.

## Setup
Make sure you install [uv](https://docs.astral.sh/uv/getting-started/installation/) via the official instructions. Then, setup can proceed like so:

```bash
$ git clone https://github.com/Smithed-MC/Libraries
$ cd Libraries
$ uv sync

# To build all projects
$ uv run beet

# To build just one library
$ uv run beet -p smithed_libraries/packs/actionbar
# or
$ cd smithed_libraries/packs/actionbar && uv run beet
```

The rest of this guide will purely use `beet` but you may need `uv run beet` if your `.venv` isn't auto-activated by your terminal.

## Developing
Since we leverage the beet toolchain, there are a couple of useful commands you can use while developing the libraries!

```bash
# Links to your .minecraft folder directly into your world
$ beet link "Minecraft World Name"

# Watches all data packs for changes
# Builds then reloads world
$ beet watch --reload

# Watch only on library
$ beet -p smithed_libraries/packs/actionbar watch --reload
# or
$ cd smithed_libraries/packs/actionbar && beet watch --reload
```

## New Library
Copy the [`template`][./template] to the `src/smithed_libraries/packs` folder. Configure the library id and update the `beet.yaml` file.

> (soon) A `beet` subcommand to easily add new libraries!


## Code Style
For all `python` code (generally written for `beet` plugins), we follow standard PEP-8 conventions via [ruff](https://docs.astral.sh/ruff/). The project must type-check with [ty](https://docs.astral.sh/ty/). We recommend running the type-checker via the VSCode Python extension (discussed below).

**Format**
```bash
$ ruff format src
```

**Check**
```bash
$ ruff check src
```

### Minecraft
We recommend using the standard [syntax-mcfunction](https://github.com/MinecraftCommands/syntax-mcfunction) for syntax highlighting.

> You can use DHP / Spyglass for most of the libraries as currently, only some libraries use `bolt` extensively.

## Commits
When committing code, follow the [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) style for writing commit messages:

```md
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

### Examples
- feat(damage): added new `apply` function
- docs(actionbar): add usage information to API functions
- fix(*): versioning hiccup in rare situations
- feat(plugins): add new `nbt-literals` plugin for packs to use

> Note 

Here are the types and scopes we'll be using (adapted from [here](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)):


### Types
> **type** [*version*]: description

- **feat** [*minor*]: A new feature
- **fix** [*patch*]: A bug fix
- **perf** [*patch*]: A code change that improves performance
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **test**: Adding missing or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

### Scopes
> **name** (*type)*: description?

- **\*** (*special*): bumps every library
- **actionbar** (*lib*)
- **crafter** (*lib*)
- **crafter-addon** (*lib*)
- **damage** (*lib*)
- **enchanter** (*lib*)
- **item** (*lib*)
- **prevent-aggression** (*lib*)
- **plugins** (*beet*): custom plugins that power smithed

### Extras
- The start of <body> can be BREAKING CHANGE to indicate a **major** version bump
- Keep each line under 100 characters


## Versioning
Each library pack has their own version as well as the entire repo itself. When producing new releases, you'll need to ensure you properly bump the versions for the libraries you've edited.

These can be found in the following files:
- `packs/<pack-name>/beet.yaml` -> `version` field
    - only bump this only for specific library
- `pyproject.toml` -> `tool.poetry.version` field
    - automatically bumped when release is made or "Release PYPI" workflow is ran

We follow the [semantic versioning](https://semver.org/) format for versioning:
- `major` reserved for breaking changes (needs maintainer approval)
- `minor` for new features and larger tweaks (usually changing user experience like updating crafter recipe)
- `patch` for bug fixes and smaller tweaks (usually doesn't affect user experience)

> The commit guide provides a table of contents to indicate whether a bump should be `patch` or `minor`.


## Releasing
Making a new release happens automatically once you've bumped the version number of a specific library (or multiple).
