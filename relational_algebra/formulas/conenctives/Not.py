from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class And(Formula):
    """
    This class represents a negation
    """

    @typechecked
    def __init__(self, child: Formula) -> None:
        super().__init__(children=[child])

    @typechecked
    def __repr__(self) -> str:
        if isinstance(self.children[0], And | Or):
            return f"\\neg({self.children[0]})"
        return f"\\neg {self.children[0]}"
