from typing import Any, ClassVar, Literal

from beet import Context, ListOption
from beet.contrib.rename_files import RenderRenameOption, TextRenameOption
from pydantic import BaseModel, Field, root_validator, validator


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
        return "v" + ".".join(str(value) for value in self.__root__.values())


class VersioningOptions(ContextualModel, extra="forbid"):
    """The `versioning` config of `beet.yaml`"""

    class LanternLoadOptions(ContextualModel):
        step: Literal["pre_load", "load", "post_load"] = "load"
        tag_path: str = "load"
        function_path: str = "impl/load"

    class ApiOptions(ContextualModel):
        match: str = "*"  # type: ignore
        implementation_prefix: str = "{{ ctx.project_id }}:impl/"
        version_check_path: str = "calls"
        tag_path: str = "load"

    scoreholder: str = "#{{ ctx.project_id }}"
    schema_: list[str] = Field(["major", "minor", "patch"], alias="schema")
    scheduled_paths: ListOption[str] = ListOption(__root__=["impl/tick"])
    version: Version = None  # type: ignore
    refactor: TextRenameOption | RenderRenameOption = {
        "match": "{{ ctx.project_id }}:*",
        "find": "{{ ctx.project_id }}:impl/",
        "replace": "{{ ctx.project_id }}:impl/v{{ version }}/",
    }  # type: ignore
    lantern_load: LanternLoadOptions = LanternLoadOptions()
    api: ApiOptions = ApiOptions()

    @property
    def namespace(self):
        return self.ctx.project_id

    @classmethod
    def render(cls, value: str, values: dict[str, Any]):
        return cls.ctx.template.render_string(value, ctx=cls.ctx, **values)

    @validator("version", pre=True, always=True)
    def init_version(cls, value: Any, values: dict[str, Any]):
        match value:
            case None:
                return Version.from_parts(values["schema_"])
            case _:
                return value

    @validator("refactor", pre=True)
    def render_refactor(cls, value: dict[str, str], values: dict[str, Any]):
        match value:
            case {"match": str(match), "find": str(find), "render": str(render)}:
                return {
                    "match": cls.render(match, values),
                    "find": cls.render(find, values),
                    "render": cls.render(render, values),
                }

            case {"match": str(match), "find": str(find), "replace": str(replace)}:
                return {
                    "match": cls.render(match, values),
                    "find": cls.render(find, values),
                    "replace": cls.render(replace, values),
                }

            case dict():
                raise ValueError(f"Invalid refactor configuration: {value!r}")

    @root_validator
    def render_strings(cls, values: dict[str, Any]):
        """This root validator handles the rendering of all structures inside

        In Pydantic V2, we would likely try to generalize this behavior in `beet`.
        For now, we have to match every key-value in our values dict to figure out
         if the string or string within needs to be rendered.
        This was a bit difficult to generalize atm, so it's basically hardcoded.
        """

        for key in values:
            match values[key]:
                case str(value):
                    values[key] = cls.render(value, values)

                case ListOption() as opt:  # type: ignore
                    values[key] = ListOption(
                        __root__=[
                            cls.render(entry, values)  # type: ignore
                            for entry in opt.entries()  # type: ignore
                        ]
                    )

                case VersioningOptions.LanternLoadOptions() as opts:
                    opts.tag_path = cls.render(opts.tag_path, values)
                    opts.function_path = cls.render(opts.function_path, values)

                case VersioningOptions.ApiOptions() as opts:
                    opts.version_check_path = cls.render(
                        opts.version_check_path, values
                    )
                    opts.match = cls.render(opts.match, values)
                    opts.implementation_prefix = cls.render(
                        opts.implementation_prefix, values
                    )
                    opts.tag_path = cls.render(opts.tag_path, values)

                case _:
                    pass

        return values
