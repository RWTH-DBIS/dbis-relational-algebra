from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class Projection(Operator):
    """
    This class represents a projection in relational algebra
    """

    @typechecked
    def __init__(self, child: Operator, attributes: list[str]) -> None:
        super().__init__(children=[child])
        self.attributes = attributes

    @typechecked
    def __repr__(self) -> str:
        return f"\\prod_{{{','.join(self.attributes)}}}({self.children[0]})"
