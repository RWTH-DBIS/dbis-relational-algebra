from __future__ import annotations

import sqlite3
from typing import Optional

from typeguard import typechecked

import relational_algebra as ra


class RightOuterJoin(ra.Operator):
    """
    This class represents a right outer join in relational algebra
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
        return f"({self.children[0]} ⟖ {self.children[1]})"

    @typechecked
    def evaluate(self, sql_con: Optional[sqlite3.Connection] = None) -> ra.Relation:
        left_relation = self.children[0].evaluate(sql_con)
        right_relation = self.children[1].evaluate(sql_con)
        # determine attribute names
        left_attributes = left_relation.get_minimal_attribute_names(
            left_relation.attributes
        )
        right_attributes = right_relation.get_minimal_attribute_names(
            right_relation.attributes
        )
        # check if attributes are not null
        assert left_attributes is not None
        assert right_attributes is not None
        # matched entries
        join = ra.NaturalJoin(left_relation, right_relation).evaluate(sql_con)
        # unmatched right entries
        right_unmatched = ra.Difference(
            right_relation, ra.Projection(join, right_attributes)
        ).evaluate(sql_con)
        left_nulls = ra.Relation.constant_nulls(
            left_relation.name,
            [attr for attr in left_attributes if attr not in right_attributes],
            len(right_unmatched.rows),
        )
        right_padded = ra.CrossProduct(left_nulls, right_unmatched).evaluate(sql_con)
        suffix_map_right_padded = {
            attr.split(".")[1]: attr for attr in right_padded.attributes
        }
        new_order_right_padded = [
            suffix_map_right_padded[attr.split(".")[1]] for attr in join.attributes
        ]
        right_padded.dataframe = right_padded.dataframe[new_order_right_padded]
        return ra.Union(join, right_padded).evaluate()
