from __future__ import annotations

from typeguard import typechecked

import relational_algebra as ra


class LessThan(ra.Formula):
    """
    This class represents a the comparison '<'
    """

    @typechecked
    def __init__(self, left: ra.PRIMITIVE_TYPES, right: ra.PRIMITIVE_TYPES) -> None:
        super().__init__(children=[])
        self.left = left
        self.right = right
        if not (isinstance(left, str) or isinstance(right, str)):
            raise ValueError(
                "At least one of the arguments must be a string referring to an attribute"
            )

    @typechecked
    def __repr__(self) -> str:
        return f"{self.left} < {self.right}"

    @typechecked
    def evaluate(self, entry: ra.RelationEntry) -> bool:
        left_is_attr = False
        left_value = self.left
        if isinstance(self.left, str):
            try:
                left_value = entry[self.left]
                left_is_attr = True
            except KeyError:
                left_is_attr = False
                left_value = self.left

        right_is_attr = False
        right_value = self.right
        if isinstance(self.right, str):
            try:
                right_value = entry[self.right]
                right_is_attr = True
            except KeyError:
                right_value = False
                right_value = self.right

        if not left_is_attr and not right_is_attr:
            raise ValueError(
                "At least one of the arguments must be a string referring to an attribute"
            )

        return left_value < right_value
