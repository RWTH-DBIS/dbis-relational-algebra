from __future__ import annotations
from typeguard import typechecked

import relational_algebra as ra


class Selection(ra.Operator):
    """
    This class represents a select in relational algebra
    """

    @typechecked
    def __init__(self, child: ra.Operator | str, condition: ra.Formula) -> None:
        if isinstance(child, str):
            child = ra.Relation(child)
        super().__init__(children=[child])
        self.condition = condition

    @typechecked
    def __repr__(self) -> str:
        return f"\\sigma_{{{self.condition}}}({self.children[0]})"

    @typechecked
    def evaluate(self) -> ra.Relation:
        relation = self.children[0].evaluate()
        # create the new relation
        new_relation = ra.Relation(relation.name)
        new_relation.attributes = relation.attributes
        # add the rows
        for row in relation.rows:
            if self.condition.evaluate(row):
                new_relation.add_row(row)
        return new_relation
