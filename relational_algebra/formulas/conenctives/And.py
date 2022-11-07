from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class And(Formula):
    """
    This class represents a conjunction
    """

    @typechecked
    def __init__(self, left_child: Formula, right_child: Formula) -> None:
        super().__init__(children=[left_child, right_child])

    @typechecked
    def __repr__(self) -> str:
        left = self.children[0]
        right = self.children[1]

        if isinstance(self.children[0], And):
            left = (
                f"{self.children[0].children[0]} \\land {self.children[0].children[1]}"
            )
        elif not isinstance(self.children[0], Not | ATOM_TYPES):
            left = f"({left})"

        if isinstance(self.children[1], And):
            right = (
                f"{self.children[1].children[0]} \\land {self.children[1].children[1]}"
            )
        elif not isinstance(self.children[1], Not | ATOM_TYPES):
            right = f"({right})"

        return f"{left} \\land {right}"
