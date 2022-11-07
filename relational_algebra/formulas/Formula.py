from __future__ import annotations
from abc import ABC, ABCMeta, abstractclassmethod
from typeguard import typechecked
from docstring_inheritance import NumpyDocstringInheritanceMeta


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
