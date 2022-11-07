from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class Select(Operator):
    """
    This class represents a select in relational algebra
    """

    @typechecked
    def __init__(self, child: Operator, condition: Formula) -> None:
        super().__init__(children=[child])
        self.condition = condition

    @typechecked
    def __repr__(self) -> str:
        return f"\\sigma_{{{self.condition}}}({self.children[0]})"
