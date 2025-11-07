from __future__ import annotations

from abc import abstractclassmethod

from docstring_inheritance import NumpyDocstringInheritanceMeta
from typeguard import typechecked
import pandas as pd

import relational_algebra as ra


class Formula(metaclass=NumpyDocstringInheritanceMeta):
    """
    An abstract class for the formula operators.
    """

    @typechecked
    def __init__(self, children: list[Formula]) -> None:
        """
        Parameters
        ----------
        children : list[Formula]
            The children of the formula.
        """
        self.children = children

    @typechecked
    @abstractclassmethod
    def __repr__(self) -> str:
        """
        Returns a string representation of the formula formatted in Latex Math Mode

        Returns
        -------
        str
            A string representation of the formula formatted in Latex Math Mode
        """
        pass

    @typechecked
    def selection(self, relation: ra.Relation) -> ra.Relation:
        """
        Returns a relation with the selection applied.

        Parameters
        ----------
        relation : ra.Relation
            The relation to apply the selection to.

        Returns
        -------
        ra.Relation
            The relation with the selection applied.
        """
        new_relation = ra.Relation(relation.name, relation.preferred_prefix)
        new_relation.was_evaluated = True
        new_relation.dataframe = relation.dataframe[self.to_series(relation)].copy()
        # drop duplicates
        new_relation.dataframe.drop_duplicates(inplace=True)
        return new_relation

    @typechecked
    @abstractclassmethod
    def to_series(self, relation: ra.Relation) -> pd.Series:
        """
        Evaluates whether the entry satifies the formula

        Parameters
        ----------
        relation : Relation
            The Relation to convert to a pd.Series

        Returns
        -------
        pd.Series
            A pd.Series
        """
        pass

    @typechecked
    def rename_formula(self, name_diff, rename_mapping: dict[str, str]) -> None:
        if isinstance(self, ra.ATOM_TYPES):
            if isinstance(self.left, str) and "." in self.left:
                pre, suff = self.left.split(".", maxsplit=1)
                for pre_partial in pre.split("+"):
                    if pre_partial in name_diff and suff in list(rename_mapping):
                        self.left = self.left.replace(
                            f".{suff}", f".{rename_mapping[suff]}"
                        )
            if isinstance(self.right, str) and "." in self.right:
                pre, suff = self.right.split(".", maxsplit=1)
                for pre_partial in pre.split("+"):
                    if pre_partial in name_diff and suff in list(rename_mapping):
                        self.right = self.right.replace(
                            f".{suff}", f".{rename_mapping[suff]}"
                        )
        elif not isinstance(self, ra.ATOM_TYPES | ra.PRIMITIVE_TYPES):
            for child in self.children:
                child.rename_formula(name_diff, rename_mapping)
