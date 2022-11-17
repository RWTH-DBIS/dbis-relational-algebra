from __future__ import annotations

import sqlite3
from typing import Optional

from typeguard import typechecked

import relational_algebra as ra


class CrossProduct(ra.Operator):
    """
    This class represents a cross product in relational algebra
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
        return f"({self.children[0]} \\times {self.children[1]})"

    @typechecked
    def evaluate(self, sql_con: Optional[sqlite3.Connection] = None) -> ra.Relation:
        left_relation = self.children[0].evaluate(sql_con)
        right_relation = self.children[1].evaluate(sql_con)
        left_attributes = left_relation.attributes
        right_attributes = right_relation.attributes
        # create new ordered list of attributes
        new_attributes = list()
        for attribute in left_attributes:
            new_attributes.append(f"{left_relation.name}.{attribute}")
        for attribute in right_attributes:
            new_attributes.append(f"{right_relation.name}.{attribute}")
        # create the new relation
        new_relation = ra.Relation("")
        new_relation.attributes = new_attributes
        # add the rows
        for left_row in left_relation.rows:
            for right_row in right_relation.rows:
                new_row = list()
                for attribute in left_attributes:
                    new_row.append(left_row[attribute])
                for attribute in right_attributes:
                    new_row.append(right_row[attribute])
                new_relation.add_row(new_row)
        return new_relation
