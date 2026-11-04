import logging
import re
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import NamedTuple

from beet import Context

logger = logging.getLogger(__name__)

DIRECTIVE_REGEX = "#>? *@{} (.+)"
COMMENT_REGEX = re.compile("#")
DOC_REGEX = re.compile(DIRECTIVE_REGEX.format("doc"))
INPUT_REGEX = re.compile(DIRECTIVE_REGEX.format("input"))
PARAM_REGEX = re.compile(DIRECTIVE_REGEX.format("param"))


class Input(NamedTuple):
    name: str
    type: str
    source: str
    target: str


type DocEntry = str | Input


def get_doc_path(parent: Path, match: re.Match[str]):
    """Attaches `@doc path/to/doc` to parent doc `Path`

    Creates folder w/ parent folders if it doesn't exist.
    """

    path: Path = parent / match[1]
    path.parent.mkdir(parents=True, exist_ok=True)

    return path


def parse_function(ctx: Context, parent: Path, lines: list[str]):
    """Parses function comments for @directives to producing docs"""

    lines_iter = iter(lines)

    for line in lines_iter:
        if match := DOC_REGEX.search(line):
            path = get_doc_path(parent, match)
            doc: list[str] = []
            inputs: list[Input] = []
            for entry in collect_doc(lines_iter):
                if isinstance(entry, Input):
                    inputs.append(entry)
                else:
                    doc.append(entry)
            write_doc(ctx, path, "\n".join(doc), inputs)


def write_doc(ctx: Context, path: Path, doc: str, inputs: list[Input]):
    """Write doc"""

    with path.with_suffix(".md").open("w+") as file:
        if inputs:
            table = make_table(
                [
                    Input(
                        "Input Name",
                        "Input Type",
                        "Input Source",
                        "Input Objective/Path",
                    ),
                    Input("---", "---", "---", "---"),
                ]
                + inputs
            )
            file.write(table)
        logger.info(
            "New Doc: %s", str(path).partition(str(ctx.output_directory) + "/")[-1]
        )
        file.write(doc)


def collect_doc(lines: Iterable[str]) -> Iterator[DocEntry]:
    """Collects @directives for docstrings"""

    for line in lines:
        if not COMMENT_REGEX.match(line):
            break

        if match := INPUT_REGEX.match(line):
            input_title, *args = match[1].strip().split(",")
            yield Input(repr(input_title), *(arg.strip() for arg in args))
        else:
            yield line[2:]


def make_table(inputs: list[Input]):
    """Make markdown table"""

    max_length_column = []
    elements_in_tuple = 4

    for i in range(elements_in_tuple):
        max_length_column.append(max(len(input[i]) + 1 for input in inputs))

    table = ""
    for input in inputs:
        row = "| "
        for i in range(elements_in_tuple):
            row += input[i].ljust(max_length_column[i]) + "| "
        table += row + "\n"
    return table + "\n\n"


def beet_default(ctx: Context):
    """Parses functions in smithed library datapacks to produce documentation

    > Plugin executes in the "exit" phase for beet plugins

    Start a documentation comment via a `@doc path/to/doc`.
    Then continue your documentation in the same comment block.
    Use `@input input_title, arg1, arg2, ...` to indicate inputs

    >>> # @doc entity/apply
    >>> # @input Amount of damage, score, @s, smithed.damage
    >>> #
    >>> # This function applies damage to an entity, ...
    """

    if ctx.output_directory is None:
        return

    output_path = ctx.output_directory.resolve()
    for path, function in ctx.data.functions.items():
        id = path.partition(":")[0].replace("smithed.", "")
        parse_function(ctx, output_path / id, function.lines)
