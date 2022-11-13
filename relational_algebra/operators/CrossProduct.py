from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class CrossProduct(Operator):
    """
    This class represents a cross product in relational algebra
    """

    @typechecked
    def __init__(self, left_child: Operator | str, right_child: Operator | str) -> None:
        if isinstance(left_child, str):
            left_child = Relation(left_child)
        if isinstance(right_child, str):
            right_child = Relation(right_child)
        super().__init__(children=[left_child, right_child])

    @typechecked
    def __repr__(self) -> str:
        return f"({self.children[0]} \\times {self.children[1]})"
