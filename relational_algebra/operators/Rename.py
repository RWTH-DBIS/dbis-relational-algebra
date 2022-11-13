from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class Rename(Operator):
    """
    This class represents a rename in relational algebra
    """

    @typechecked
    def __init__(self, child: Operator, mapping: dict[str, str] | str) -> None:
        if isinstance(child, str):
            child = Relation(child)
        super().__init__(children=[child])
        self.mapping = mapping

    @typechecked
    def __repr__(self) -> str:
        if isinstance(self.mapping, str):
            return f"\\rho_{{{self.mapping}}}({self.children[0]})"
        else:
            # there cannot be \ in f-string in f-string (says formatter)
            tmp = [f"{v} \\leftarrow {k}" for k, v in self.mapping.items()]
            return f"\\rho_{{{','.join(tmp)}}}({self.children[0]})"
