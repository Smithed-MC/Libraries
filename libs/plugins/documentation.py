from collections import namedtuple
import os
import re
from typing import List, Match
from beet import Context
from yaml import parse

DIRECTIVE_REGEX = "^#>? *@{} "
DOC_REGEX = DIRECTIVE_REGEX.format("doc")
INPUT_REGEX = DIRECTIVE_REGEX.format("input")
PARAM_REGEX = DIRECTIVE_REGEX.format("param")


def parse_doc(line: str, search: Match[str], parent_folder: str):
    path = os.path.join(parent_folder, line[search.span(0)[1] :])
    containing_folder = "/".join(path.split("/")[:-1])
    if not os.path.isdir(containing_folder):
        os.makedirs(containing_folder)
    return path


def parse_function(parent_folder: str, lines: List[str]):
    i = 0
    while i < len(lines):
        line = lines[i]
        if search := re.search(DOC_REGEX, line):
            path = parse_doc(line, search, parent_folder)
            i += 1
            i = collect_doc(path, lines, i)
        i += 1


Input = namedtuple(
    "Input", ["name", "type", "source", "target"], defaults=[None, None, None, None]
)


def collect_doc(path: str, lines: List[str], i: int):
    doc = ""
    inputs = [
        Input("Input Name", "Input Type", "Input Source", "Input Objective/Path"),
        Input("---", "---", "---", "---"),
    ]

    while lines[i].startswith("#"):
        line = lines[i]

        if search := re.search(INPUT_REGEX, line):
            args = line[search.span(0)[1] :].strip().split(",")
            print(args)
            input = Input(
                f'"{args[0]}"', args[1].strip(), args[2].strip(), args[3].strip()
            )
            inputs.append(input)
        else:
            doc += lines[i][re.search("^# ?", lines[i]).span(0)[1] :] + "\n"
        i += 1
    with open(path + ".md", "w+") as doc_file:
        if len(inputs) > 2:
            doc_file.write(make_table(inputs))
        doc_file.write(doc)
    return i


def make_table(inputs: List[Input]):
    max_length_column = []
    elements_in_tuple = 4

    for i in range(elements_in_tuple):
        max_length_column.append(max(len(e[i]) + 1 for e in inputs))

    table = ""
    for e in inputs:
        row = "| "
        for i in range(elements_in_tuple):
            row += e[i].ljust(max_length_column[i]) + "| "
        table += row + "\n"
    return table + "\n\n"


def beet_default(ctx: Context):
    yield
    parent_folder = os.path.join("docs", ctx.project_name.lower().replace(" ", "-"))

    for path in ctx.data.functions:
        function = ctx.data.functions[path]
        lines: List[str] = function.text.split("\n")
        parse_function(parent_folder, lines)
