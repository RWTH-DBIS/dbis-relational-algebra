from __future__ import annotations
from typeguard import typechecked

import relational_algebra as ra


class NaturalJoin(ra.Operator):
    """
    This class represents a natural join in relational algebra
    """

    @typechecked
    def __init__(
        self, left_child: ra.Operator | str, right_child: ra.Operator | str
    ) -> None:
        if isinstance(left_child, str):
            left_child = ra.Relation(left_child)
        if isinstance(right_child, str):
            right_child = ra.Relation(right_child)
        super().__init__(children=[left_child, right_child])

    @typechecked
    def __repr__(self) -> str:
        return f"({self.children[0]} \\bowtie {self.children[1]})"

    @typechecked
    def evaluate(self) -> ra.Relation:
        left_relation = self.children[0].evaluate()
        right_relation = self.children[1].evaluate()
        # determine attribute names
        left_attributes = left_relation.get_attribute_names(left_relation.attributes)
        right_attributes = right_relation.get_attribute_names(right_relation.attributes)
        # determine common attributes
        common_attributes = set(left_attributes).intersection(right_attributes)
        # determine new attribute names
        new_attributes = list(left_attributes)
        for attribute in right_attributes:
            if attribute not in common_attributes:
                new_attributes.append(attribute)
        # create new relation
        new_relation = ra.Relation("")
        new_relation.attributes = new_attributes
        # add rows
        for left_row in left_relation.rows:
            for right_row in right_relation.rows:
                add_attribute = True
                for attribute in common_attributes:
                    if left_row[attribute] != right_row[attribute]:
                        add_attribute = False
                        break
                if add_attribute:
                    new_row = list(left_row)
                    for attribute in right_attributes:
                        if attribute not in common_attributes:
                            new_row.append(right_row[attribute])
                    new_relation.add_row(new_row)
        return new_relation
