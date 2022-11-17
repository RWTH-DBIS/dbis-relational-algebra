import pytest

from relational_algebra import *


def test_basic_relation(session):
    # see conftest.py
    r = Relation("basic").evaluate(sql_con=session)
    assert r.name == "basic"
    assert r.get_minimal_attribute_names(r.attributes) == ["id", "name", "age"]
    assert len(r.rows) == 5
    assert set(r.rows) == {
        (1, "John", 25),
        (2, "Jane", 30),
        (3, "Jack", 35),
        (4, "Jill", 40),
        (5, "Joe", 45),
    }
