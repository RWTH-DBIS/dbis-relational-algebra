from __future__ import annotations

from abc import abstractclassmethod

from docstring_inheritance import NumpyDocstringInheritanceMeta
from typeguard import typechecked

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
    @abstractclassmethod
    def evaluate(self, entry: ra.RelationEntry) -> bool:
        """
        Evaluates whether the entry satifies the formula

        Parameters
        ----------
        entry : RelationEntry
            The entry to evaluate the formula for

        Returns
        -------
        bool
            The result of the evaluation
        """
        pass
