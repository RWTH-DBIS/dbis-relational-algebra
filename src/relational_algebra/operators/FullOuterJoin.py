from __future__ import annotations

import pandas as pd
import re

import sqlite3
from typing import Optional

from typeguard import typechecked

import relational_algebra as ra


class FullOuterJoin(ra.Operator):
    """
    This class represents a full outer join in relational algebra
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
        return f"({self.children[0]} ⟗ {self.children[1]})"

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
        left_df = left_relation.dataframe
        right_df = right_relation.dataframe

        left_df.columns = left_attributes
        right_df.columns = right_attributes

        common_attributes = [
            attribute for attribute in left_attributes if attribute in right_attributes
        ]

        new_relation = ra.Relation(
            f"{left_relation.name}+{right_relation.name}",
            left_relation.preferred_prefix,
            right_relation.preferred_prefix,
        )

        try:
            if common_attributes:
                new_relation.dataframe = left_df.merge(
                    right_df, how="outer", on=common_attributes
                )
            else:
                new_relation.dataframe = pd.concat([left_df, right_df], sort=False)
        except ValueError as e:
            msg = str(e)
            m = re.search(r"merge on (\w+) and (\w+) columns for key '([^']+)'", msg)
            if m:
                dtype1, dtype2, col = m.groups()
                raise ValueError(
                    f"Cannot perform {self.__class__.__name__} on Relations '{left_relation.name}' and '{right_relation.name}': incompatible attribute types {dtype1} and {dtype2} for column '{col}'."
                ) from None
            else:
                raise ValueError(
                    f"Cannot perform {self.__class__.__name__} on Relations '{left_relation.name}' and '{right_relation.name}': incompatible attribute types for atleast one column."
                ) from None

        new_relation.dataframe.drop_duplicates(inplace=True)
        new_relation.dataframe.columns = [
            f"{left_relation.name}+{right_relation.name}.{col}"
            for col in new_relation.dataframe.columns
        ]
        if not new_relation.dataframe.empty:
            with pd.option_context("future.no_silent_downcasting", True):
                new_relation.dataframe = new_relation.dataframe.fillna("-")
        return new_relation
