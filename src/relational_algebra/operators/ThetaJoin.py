from __future__ import annotations

import sqlite3
from typing import Optional

import re

from typeguard import typechecked

import relational_algebra as ra


class ThetaJoin(ra.Operator):
    """
    This class represents a theta join in relational algebra
    """

    @typechecked
    def __init__(
        self,
        left_child: ra.Operator | str,
        right_child: ra.Operator | str,
        formula: ra.Formula,
    ) -> None:
        if isinstance(left_child, str):
            left_child = ra.Relation(left_child)
        if isinstance(right_child, str):
            right_child = ra.Relation(right_child)
        super().__init__(children=[left_child, right_child])
        self.formula = formula

    @typechecked
    def __repr__(self) -> str:
        return f"({self.children[0]} \\bowtie_{{{self.formula}}} {self.children[1]})"

    @typechecked
    def evaluate(self, sql_con: Optional[sqlite3.Connection] = None) -> ra.Relation:
        left_relation = self.children[0].evaluate(sql_con)
        right_relation = self.children[1].evaluate(sql_con)
        partial_formulas = re.split(r"(?: \\land | \\lor |\\neg )", str(self.formula))
        filtered_formulas = [item for item in partial_formulas if item != ""]
        for entry in filtered_formulas:
            left_entry, right_entry = re.split(r" (?:=|\\geq|>|\\leq|<) ", entry)
            left_value_rr = right_relation.get_minimal_attribute_name(left_entry)
            right_value_rr = right_relation.get_minimal_attribute_name(right_entry)
            left_value_lr = left_relation.get_minimal_attribute_name(left_entry)
            right_value_lr = left_relation.get_minimal_attribute_name(right_entry)
            rr_preferred_prefix = None
            if (
                left_entry.split(".", maxsplit=1)[-1]
                == right_entry.split(".", maxsplit=1)[-1]
            ):
                if "." in left_entry:
                    if left_value_rr is not None:
                        rr_preferred_prefix = left_entry.split(".")[0]
                        self.children[1] = ra.Rename(
                            self.children[1], {left_value_rr: left_entry}
                        )
                    if left_value_lr is not None:
                        left_relation.preferred_prefix = left_entry.split(".")[0]
                if "." in right_entry:
                    if right_value_rr is not None:
                        rr_preferred_prefix = right_entry.split(".")[0]
                        self.children[1] = ra.Rename(
                            self.children[1], {right_value_rr: right_entry}
                        )
                    if right_value_lr is not None:
                        left_relation.preferred_prefix = right_entry.split(".")[0]
        right_relation = self.children[1].evaluate(sql_con)
        right_relation.preferred_prefix = rr_preferred_prefix
        return ra.Selection(
            ra.CrossProduct(left_relation, right_relation), self.formula
        ).evaluate()
