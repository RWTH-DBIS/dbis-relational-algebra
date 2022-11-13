from __future__ import annotations
from abc import ABC, ABCMeta, abstractclassmethod
from typeguard import typechecked
from docstring_inheritance import NumpyDocstringInheritanceMeta

from relational_algebra import *


class Operator(metaclass=NumpyDocstringInheritanceMeta):
    """
    An abstract class for the relational algebra operators.
    """

    @typechecked
    def __init__(self, children: list[Operator]) -> None:
        """
        Parameters
        ----------
        children : list[Operator]
            The children of the operator.
        """
        self.children = children

    @typechecked
    @abstractclassmethod
    def __repr__(self) -> str:
        """
        Returns a string representation of the operator formatted in Latex Math Mode

        Returns
        -------
        str
            A string representation of the operator formatted in Latex Math Mode
        """
        pass

    @typechecked
    def __sub__(self, other: Operator) -> Operator:
        """
        Returns the difference of two operators

        Parameters
        ----------
        other : Operator
            The operator to subtract from the current operator

        Returns
        -------
        Operator
            The difference of two operators
        """
        return Difference(self, other)

    @typechecked
    def __mul__(self, other: Operator) -> Operator:
        """
        Returns the cross product of two operators

        Parameters
        ----------
        other : Operator
            The operator to cross product with the current operator

        Returns
        -------
        Operator
            The cross product of two operators
        """
        return CrossProduct(self, other)

    @typechecked
    def union(self, other: Operator) -> Operator:
        """
        Returns the union of two operators

        Parameters
        ----------
        other : Operator
            The operator to union with the current operator

        Returns
        -------
        Operator
            The union of two operators
        """
        return Union(self, other)

    @typechecked
    def intersection(self, other: Operator) -> Operator:
        """
        Returns the intersection of two operators

        Parameters
        ----------
        other : Operator
            The operator to intersect with the current operator

        Returns
        -------
        Operator
            The intersection of two operators
        """
        return Intersection(self, other)

    @typechecked
    def evaluate(self) -> Relation:
        """
        Evaluates the operator

        Returns
        -------
        Relation
            The evaluated operator
        """
        pass
