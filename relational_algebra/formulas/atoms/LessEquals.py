from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class LessEquals(Formula):
    """
    This class represents a the comparison '<='
    """

    @typechecked
    def __init__(self, left: PRIMITIVE_TYPES, right: PRIMITIVE_TYPES) -> None:
        super().__init__(children=[])
        self.left = left
        self.right = right

    @typechecked
    def __repr__(self) -> str:
        return f"{self.left} \\leq {self.right}"
