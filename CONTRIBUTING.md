# Contributing

Contributions are welcome! Make sure to first open an issue discussing the problem or the new feature before creating a pull request. This project uses [poetry](https://python-poetry.org/) and [beet](https://mcbeet.dev) for building and publishing to pypi.

## Setup
Make sure you install [poetry](https://python-poetry.org/docs/) via the official instructions. Then, setup can proceed like so:

```bash
$ git clone https://github.com/Smithed-MC/Libraries
$ cd Libraries
$ poetry install

# To build all projects
$ beet

# To build just one library
$ beet -s "broadcast: smithed_libraries/packs/actionbar"
# or
$ cd smithed_libraries/packs/actionbar
$ beet
```

## Code Style
The code follows the [black](https://github.com/psf/black) code style. Import statements are sorted with [isort](https://pycqa.github.io/isort/). The project must type-check with [pyright](https://github.com/microsoft/pyright). We recommend running the type-checker via the VSCode Python extension (discussed below).

**Format**
```bash
# omit `poetry run` if u have the virtualenv activated
$ poetry run isort smithed_libraries
$ poetry run black smithed_libraries
```

**Check**
```bash
# omit `poetry run` if u have the virtualenv activated
$ poetry run black --check smithed_libraries
$ poetry run isort --check-only smithed_libraries
```

You can run `poetry self add 'poethepoet[poetry_plugin]'` to get access to an easier set of commands:
```bash
# omit `poetry` if u have the virtualenv activated
$ poetry poe format
$ poetry poe check
```

## IDE
We recommend using [VSCode](https://code.visualstudio.com/). The following recommendations are made based on if you are making minecraft pack and/or python contributions.

### Minecraft
We recommend using the [Bolt Syntax Definition](https://ptb.discord.com/channels/900530660677156924/900545626549387286/973086846227718185) (This links to the [Beet Discord Server](https://discord.gg/98MdSGMm8j) - Github coming soon). This extension is compatible with normal `mcfunction` commands while also allowing for multiline and bolt support.

> You can use DHP / Spyglass for most of the libraries as currently, only some libraries use `bolt` extensively.

### Python
We recommend using the official [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension. This extension comes with type-checking support alongside automatic formatting and import sorting via the settings (coming soon).

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
- **crafter**-addon (*lib*)
- **damage** (*lib*)
- **enchanter** (*lib*)
- **item** (*lib*)
- **prevent-aggression** (*lib*)
- **plugins** (*beet*): custom plugins that power smithed

### Extras
- The start of <body> can be BREAKING CHANGE to indicate a **major** version bump
- Keep each line under 100 characters


## Versioning
Each library pack has their own version as well as the entire repo itself. Using the `Release` Github Action will bump the cooresponding versions in each file.

These can be found in the following files:
- `packs/<pack-name>/beet.yaml` -> `version` field
- `pyproject.toml` -> `tool.poetry.version` field

## Releasing
To make a new release, run the Github Action `Release` flow. This will produce a new set of `zips` for `Smithed` alongside pushing the library to `pypi`.
