from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class Relation(Operator):
    """
    This class represents a relation in relational algebra
    """

    @typechecked
    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the relation
        """
        super().__init__(children=[])
        self.name = name

    @typechecked
    def __repr__(self) -> str:
        return f"(\\text{{{self.name}}})"
