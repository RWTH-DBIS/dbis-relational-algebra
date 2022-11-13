from __future__ import annotations
from typeguard import typechecked

from relational_algebra import *


class Projection(Operator):
    """
    This class represents a projection in relational algebra
    """

    @typechecked
    def __init__(
        self, child: Operator | str, attributes: str | tuple[str] | list[str]
    ) -> None:
        if isinstance(child, str):
            child = Relation(child)
        super().__init__(children=[child])
        if isinstance(attributes, str):
            attributes = [attributes]
        self.attributes = attributes

    @typechecked
    def __repr__(self) -> str:
        return f"\\prod_{{{','.join(self.attributes)}}}({self.children[0]})"

    @typechecked
    def evaluate(self) -> Relation:
        child_relation = self.children[0].evaluate()
        return child_relation[("b", "a")]
