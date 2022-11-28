from typing import Any, ClassVar, Literal

from beet import Context, ListOption, PathSpecOption
from beet.contrib.rename_files import RenderRenameOption, TextRenameOption
from pydantic import BaseModel, Field, validator

from .types import JsonDict, JsonType


class ContextualModel(BaseModel):
    ctx: ClassVar[Context]


class Version(ContextualModel):
    """Provides methods and fields for the version for ease of use"""

    __root__: dict[str, int]

    @classmethod
    def from_parts(cls, names: list[str]):
        numbers = [int(num) for num in cls.ctx.project_version.split(".")]
        combined = dict(zip(names, numbers))

        if len(combined) != len(numbers) or len(combined) != len(names):
            raise ValueError(
                f"The schema: {names!r} does not match the version {cls.ctx.project_version!r}"
            )

        return cls(__root__=combined)

    @validator("__root__")
    def ensure_version_parts(cls, value: dict[str, int]):
        for name, number in value.items():
            if number < 0:
                raise ValueError(f"{name} had an invalid version value: {number}")

        return value

    def named_parts(self):
        return list(self.__root__.items())

    def __str__(self):
        return ".".join(str(value) for value in self.__root__.values())


class VersioningOptions(ContextualModel, extra="forbid"):
    """The `versioning` config of `beet.yaml`"""

    class LanternLoadOptions(ContextualModel):
        step: Literal["pre_load", "load", "post_load"] = "load"
        tag_path: str = "load"
        function_path: str = "impl/load"

    class ApiOptions(ContextualModel):
        match: PathSpecOption = "{{ project_id }}:v{{ version }}/*"  # type: ignore
        implementation_prefix: str = "{{ project_id }}:v{{ version }}/"
        version_check_path: str = "v{{ version }}/calls"
        tag_path: str = ""

    scoreholder: str = "#{{ project_id }}"
    schema_: list[str] = Field(["major", "minor", "patch"], alias="schema")
    scheduled_paths: ListOption[str] = ListOption(__root__=["impl/tick"])
    version: Version = None  # type: ignore
    refactor: TextRenameOption | RenderRenameOption = {
        "match": "{{ project_id }}:*",
        "find": "{{ project_id }}:impl/",
        "replace": "{{ project_id }}:impl/v{{ version }}/",
    }  # type: ignore
    lantern_load: LanternLoadOptions = LanternLoadOptions()
    api: ApiOptions = ApiOptions()

    @property
    def namespace(self):
        return self.ctx.project_id

    @classmethod
    def render(cls, value: str, values: dict[str, Any]):
        return cls.ctx.template.render_string(value, **values)

    @validator("version", pre=True, always=True)
    def init_version(cls, value: Any, values: dict[str, Any]):
        return value or Version.from_parts(values["schema_"])

    @classmethod
    def render_value(cls, val: JsonType, all_values: JsonDict) -> JsonType:
        match val:
            case str(value):
                return cls.render(value, all_values)

            case list(vals):
                return [cls.render_value(val, all_values) for val in vals]

            case dict(vals):
                return {
                    key: cls.render_value(val, all_values) for key, val in vals.items()
                }

            case _ as val:
                return val

    @validator("*", pre=True, always=True)
    def render_all(cls, value: JsonType, values: JsonDict):
        """This validator handles the rendering of all structures inside

        In Pydantic V2, we would likely try to generalize this behavior in `beet`.
        For now, we have to match every key-value in our values dict to figure out
         if the string or string within needs to be rendered.
        """

        return cls.render_value(value, all_values=values)


class Versioning:
    opts: VersioningOptions

    def __init__(self, ctx: Context):
        self.opts = ctx.validate("smithed.versioning", VersioningOptions)
