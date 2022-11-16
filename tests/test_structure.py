import pytest
from relational_algebra import *


def test_projection():
    r = Relation("R")
    r.attributes = ["a", "b", "c"]
    r.add_rows([["a", "b", "c"], ["d", "e", "f"]])
    p = Projection(r, ["b", "a"])
    pr = p.evaluate()
    rows = pr.rows
    assert set(rows) == {("b", "a"), ("e", "d")}
