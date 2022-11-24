import pytest

from relational_algebra import *


@pytest.mark.skip(reason="not implemented")
def test_tautology():
    r = Relation("R")
    r.attributes = ["a", "b", "c"]
    r.add_rows([["a", "b", "c"], ["d", "e", "f"]])
    tautology_formula = Equals("a", "a")
    s = Selection(r, tautology_formula)
    result = s.evaluate()
    rows = result.rows
    assert set(rows) == {("a", "b", "c"), ("d", "e", "f")}


@pytest.mark.skip(reason="not implemented")
def test_contradiction():
    r = Relation("R")
    r.add_attributes(["a", "b", "c"])
    r.add_rows([["a", "b", "c"], ["d", "e", "f"]])
    contradiction_formula = Not(Equals("a", "a"))
    s = Selection(r, contradiction_formula)
    result = s.evaluate()
    rows = result.rows
    assert set(rows) == set()


@pytest.mark.skip(reason="not implemented")
def test_partial():
    r = Relation("R")
    r.add_attributes(["a", "b", "c"])
    r.add_rows([["a", "b", "c"], ["d", "e", "f"]])
    partial_formula = Equals("b", "e")
    s = Selection(r, partial_formula)
    result = s.evaluate()
    rows = result.rows
    assert set(rows) == {("d", "e", "f")}
