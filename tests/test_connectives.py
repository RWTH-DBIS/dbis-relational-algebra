import pytest

from relational_algebra import *


def test_not():
    r = Relation("R")
    r.attributes = ["a", "b", "c"]
    r.add_rows([["a", "b", "a"], ["d", "e", "f"]])
    formula = Equals(f"{r.name}.a", f"{r.name}.c")
    not_formula = Not(formula)
    rows = list(r.rows)
    for row in rows:
        assert bool(formula.evaluate(row)) ^ bool(not_formula.evaluate(row))


def test_and():
    r = Relation("R")
    r.attributes = ["a", "b", "c"]
    r.add_rows([["a", "b", "a"], ["d", "e", "f"], ["b", "b", "b"]])
    formula1 = Equals(f"{r.name}.a", f"{r.name}.c")
    formula2 = Equals(f"{r.name}.a", f"{r.name}.b")
    and_formula = And(formula1, formula2)
    rows = list(r.rows)
    # and_formula true for exactly one row
    assert sum([bool(and_formula.evaluate(row)) for row in rows]) == 1


def test_or():
    r = Relation("R")
    r.attributes = ["a", "b", "c"]
    r.add_rows([["a", "b", "a"], ["d", "e", "f"], ["b", "b", "b"]])
    formula1 = Equals(f"{r.name}.a", f"{r.name}.c")
    formula2 = Equals(f"{r.name}.a", f"{r.name}.b")
    or_formula = Or(formula1, formula2)
    rows = list(r.rows)
    # or_formula true for exactly two rows
    assert sum([bool(or_formula.evaluate(row)) for row in rows]) == 2
