from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class Intersection(Operator):
    """
    This class represents an intersection in relational algebra
    """

    @typechecked
    def __init__(self, left_child: Operator, right_child: Operator) -> None:
        super().__init__(children=[left_child, right_child])

    @typechecked
    def __repr__(self) -> str:
        return f"({self.children[0]} \\cap {self.children[1]})"
