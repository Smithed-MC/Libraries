# smithed.wiki
The main plugin for generating Smithed Wiki books. The datapack & resourcepack in `smithed_libraries/packs/wiki` serve as boot-strapping and basic resources. 

## Structure
- `__init__.py` - The Beet plugin entry point
- `models.py` - The Pydantic models for validating the books and sections
- `plugin.py` - The main logic for building a wiki book
- `resources.py` - The Beet resources for loading the files from a datapack

## Building
### Pre-requisites 
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Steps
Clone the repository and checkout the `feat/wiki` branch
```sh
git clone https://github.com/Smithed-MC/Libraries -b feat/wiki
```
Move into the repo
```sh
cd Libraries
```
Install the dependencies
```sh
uv sync
```
Build the libraries
```sh
uv run beet -s "data_pack.zipped = False" -s "resource_pack.zipped = False"
```
