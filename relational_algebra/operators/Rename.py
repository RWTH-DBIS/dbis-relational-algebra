from __future__ import annotations

import sqlite3
from typing import Optional

from typeguard import typechecked

import relational_algebra as ra


class Rename(ra.Operator):
    """
    This class represents a rename in relational algebra
    """

    @typechecked
    def __init__(self, child: ra.Operator | str, mapping: dict[str, str] | str) -> None:
        if isinstance(child, str):
            child = ra.Relation(child)
        super().__init__(children=[child])
        self.mapping = mapping

    @typechecked
    def __repr__(self) -> str:
        if isinstance(self.mapping, str):
            return f"\\rho_{{{self.mapping}}}({self.children[0]})"
        else:
            # there cannot be \ in f-string in f-string (says formatter)
            tmp = [f"{v} \\leftarrow {k}" for k, v in self.mapping.items()]
            return f"\\rho_{{{','.join(tmp)}}}({self.children[0]})"

    @typechecked
    def evaluate(self, sql_con: Optional[sqlite3.Connection] = None) -> ra.Relation:
        relation = self.children[0].evaluate(sql_con)

        if isinstance(self.mapping, str):
            # rename the relation
            new_relation = ra.Relation(self.mapping)
            new_relation.attributes = relation.attributes
            # add the rows
            new_relation.add_rows(relation.rows)
            return new_relation

        # find correct attribute names
        new_mapping = {}
        for key, value in self.mapping.items():
            # check if key is attribute in the relation
            key = relation.get_attribute_name(key)
            if key is None:
                raise KeyError(
                    f"The attribute {key} is not in the relation {relation.name}"
                )
            # check if value is not already an attribute in the relation
            v = relation.get_attribute_name(value)
            if v is not None:
                raise ValueError(
                    f"The attribute {value} is already in the relation {relation.name}"
                )
            # check if key is not already in the mapping
            if key in new_mapping.keys():
                raise KeyError(f"The attribute {key} is already in the mapping")
            # check if value is not already in the mapping
            if value in new_mapping.values():
                raise ValueError(f"The attribute {value} is already in the mapping")
            # rename the attribute
            new_mapping[key] = value

        # create the new relation
        new_relation = ra.Relation(relation.name)
        # rename the attributes
        for attribute in relation.attributes:
            if relation.get_attribute_name(attribute) not in new_mapping.keys():
                new_relation.attributes.append(attribute)
            else:
                new_relation.attributes.append(
                    new_mapping[relation.get_attribute_name(attribute)]
                )
        # add the rows
        new_relation.add_rows(relation.rows)
        return new_relation
