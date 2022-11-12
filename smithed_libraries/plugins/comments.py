from dataclasses import dataclass

from beet import Context
from mecha import Mecha, Parser
from tokenstream import TokenStream


@dataclass
class CommentParser:
    parser: Parser

    def __call__(self, stream: TokenStream):
        index = stream.index
        node = self.parser(stream)

        while index >= 0:
            token = stream.tokens[index]

            if token.match("comment"):
                print(token)
            elif not token.match("indent", "dedent", "whitespace", "newline"):
                break

            index -= 1

        return node


def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    mc.spec.parsers["command"] = CommentParser(mc.spec.parsers["command"])
