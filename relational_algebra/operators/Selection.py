from __future__ import annotations
from typeguard import typechecked

import relational_algebra as ra


class Selection(ra.Operator):
    """
    This class represents a select in relational algebra
    """

    @typechecked
    def __init__(self, child: ra.Operator, condition: ra.Formula) -> None:
        if isinstance(child, str):
            child = ra.Relation(child)
        super().__init__(children=[child])
        self.condition = condition

    @typechecked
    def __repr__(self) -> str:
        return f"\\sigma_{{{self.condition}}}({self.children[0]})"
