from typing import Any, ClassVar, Literal

from beet import Context, ListOption, PathSpecOption
from beet.contrib.rename_files import RenderRenameOption, TextRenameOption
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    ValidationInfo,
    field_validator,
    model_validator,
)

from .types import JsonDict, JsonType


class ContextualModel(BaseModel):
    ctx: ClassVar[Context]


class Version(ContextualModel, RootModel[dict[str, int]]):
    """Provides methods and fields for the version for ease of use"""

    @classmethod
    def from_parts(cls, names: list[str]):
        numbers = [int(num) for num in cls.ctx.project_version.split(".")]
        combined = dict(zip(names, numbers))

        if len(combined) != len(numbers) or len(combined) != len(names):
            raise ValueError(
                f"The schema: {names!r} does not match the version {cls.ctx.project_version!r}"
            )

        return cls(combined)

    @field_validator("root")
    @classmethod
    def ensure_version_parts(cls, value: dict[str, int]):
        for name, number in value.items():
            if number < 0:
                raise ValueError(f"{name} had an invalid version value: {number}")

        return value

    def named_parts(self):
        return list(self.root.items())

    def __str__(self):
        return ".".join(str(value) for value in self.root.values())


class VersioningOptions(ContextualModel):
    """The `versioning` config of `beet.yaml`"""

    model_config = ConfigDict(extra="forbid")

    class LanternLoadOptions(ContextualModel):
        step: Literal["pre_load", "load", "post_load"] = "load"
        tag_path: str = "load"
        function_path: str = "impl/load"

    class ApiOptions(ContextualModel):
        match: PathSpecOption = "{{ project_id }}:v{{ project_version }}/*"  # type: ignore
        implementation_prefix: str = "{{ project_id }}:v{{ project_version }}/"
        version_check_path: str = "v{{ project_version }}/calls"
        tag_path: str = ""

    scoreholder: str = "#{{ project_id }}"
    schema_: list[str] = Field(["major", "minor", "patch"], alias="schema")
    scheduled_paths: ListOption[str] = ListOption(["impl/tick"])
    
    # In V2, use validate_default=True instead of always=True on the validator
    version: Version | None = Field(default=None, validate_default=True)
    
    refactor: TextRenameOption | RenderRenameOption = {
        "match": "{{ project_id }}:*",
        "find": "{{ project_id }}:impl/",
        "replace": "{{ project_id }}:impl/v{{ version }}/",
    }  # type: ignore
    
    lantern_load: LanternLoadOptions = Field(default_factory=LanternLoadOptions)
    api: ApiOptions = Field(default_factory=ApiOptions)

    @property
    def namespace(self):
        return self.ctx.project_id

    @classmethod
    def render(cls, value: str, values: dict[str, Any]):
        return cls.ctx.template.render_string(value, **values)

    @field_validator("version", mode="before")
    @classmethod
    def init_version(cls, value: Any, info: ValidationInfo):
        if value:
            return value
        # Access previously validated fields via info.data
        schema = info.data.get("schema_", ["major", "minor", "patch"])
        return Version.from_parts(schema)

    @classmethod
    def render_value(cls, val: JsonType, all_values: JsonDict) -> JsonType:
        match val:
            case str(value):
                return cls.render(value, all_values)

            case list(vals):
                return [cls.render_value(v, all_values) for v in vals]

            case dict(vals):
                return {
                    key: cls.render_value(v, all_values) for key, v in vals.items()
                }

            case _ as v:
                return v

    @model_validator(mode="before")
    @classmethod
    def render_all(cls, data: Any) -> Any:
        """This validator handles the rendering of all structures inside

        In Pydantic V2, a before-mode model_validator takes the whole raw
        input dict before individual field validation, replacing the V1 `*` wildcard.
        """
        if isinstance(data, dict):
            return {
                key: cls.render_value(val, data) for key, val in data.items()
            }
        return data


class Versioning:
    opts: VersioningOptions

    def __init__(self, ctx: Context):
        self.opts = ctx.validate("smithed.versioning", VersioningOptions)