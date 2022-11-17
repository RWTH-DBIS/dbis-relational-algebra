from __future__ import annotations

from typeguard import typechecked

import relational_algebra as ra


class Not(ra.Formula):
    """
    This class represents a negation
    """

    @typechecked
    def __init__(self, child: ra.Formula) -> None:
        super().__init__(children=[child])

    @typechecked
    def __repr__(self) -> str:
        if isinstance(self.children[0], ra.And | ra.Or):
            return f"\\neg({self.children[0]})"
        return f"\\neg {self.children[0]}"

    @typechecked
    def evaluate(self, entry: ra.RelationEntry) -> bool:
        return not self.children[0].evaluate(entry)
