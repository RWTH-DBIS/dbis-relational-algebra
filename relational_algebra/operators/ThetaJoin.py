from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class ThetaJoin(Operator):
    """
    This class represents a theta join in relational algebra
    """

    @typechecked
    def __init__(
        self, left_child: Operator, right_child: Operator, formula: Formula
    ) -> None:
        super().__init__(children=[left_child, right_child])
        self.formula = formula

    @typechecked
    def __repr__(self) -> str:
        return f"({self.children[0]} \\bowtie_{self.formula} {self.children[1]})"
