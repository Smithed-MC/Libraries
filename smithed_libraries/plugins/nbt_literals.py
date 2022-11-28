# type: ignore

import operator
from dataclasses import dataclass, field
from typing import Any, Dict, Type

from beet import Context
from bolt import AstValue, Runtime
from mecha import Mecha, Parser
from nbtlib import Byte, Double, Float, Long, Numeric, Short
from tokenstream import TokenStream, set_location

SUFFIXED_NUMBER = r"[+-]?(?:[0-9]*?\.[0-9]+|[0-9]+\.[0-9]*?|[1-9][0-9]*|0)(?:[eE][+-]?[0-9]+)?[bslfdBSLFD]\b"


# nbtlib monkey patch :)
def op_method(op, reverse=False):
    def method(self, other):
        value = op(other.real, self.real) if reverse else op(self.real, other.real)
        return self.__class__(value)

    return method


Numeric.__add__ = op_method(operator.add)
Numeric.__radd__ = op_method(operator.add, reverse=True)
Numeric.__sub__ = op_method(operator.sub)
Numeric.__rsub__ = op_method(operator.sub, reverse=True)
Numeric.__mul__ = op_method(operator.mul)
Numeric.__rmul__ = op_method(operator.mul, reverse=True)
Numeric.__truediv__ = op_method(operator.truediv)
Numeric.__rtruediv__ = op_method(operator.truediv, reverse=True)


def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    runtime = ctx.inject(Runtime)
    runtime.globals.update(
        {"Byte": Byte, "Short": Short, "Long": Long, "Float": Float, "Double": Double}
    )
    mc.spec.parsers["bolt:literal"] = NbtLiteralParser(
        parser=mc.spec.parsers["bolt:literal"]
    )


@dataclass
class NbtLiteralParser:
    parser: Parser
    number_suffixes: Dict[str, Type[Any]] = field(
        default_factory=lambda: {
            "b": Byte,
            "s": Short,
            "l": Long,
            "f": Float,
            "d": Double,
        }
    )

    def __call__(self, stream: TokenStream):
        with stream.syntax(nbt_literal=SUFFIXED_NUMBER):
            with stream.checkpoint() as commit:
                number = stream.expect("nbt_literal")
                suffix = number.value[-1].lower()
                value = self.number_suffixes[suffix](number.value[:-1])
                node = AstValue(value=value)
                commit()
                return set_location(node, stream.current)
        return self.parser(stream)
