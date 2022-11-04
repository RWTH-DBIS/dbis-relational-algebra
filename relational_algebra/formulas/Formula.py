from __future__ import annotations
from abc import ABC, ABCMeta, abstractclassmethod
from typeguard import typechecked
from docstring_inheritance import NumpyDocstringInheritanceMeta


class Operator(metaclass=NumpyDocstringInheritanceMeta):
    """
    An abstract class for the formula operators.
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
