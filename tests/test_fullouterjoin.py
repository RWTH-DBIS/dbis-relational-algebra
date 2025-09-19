import pytest

from relational_algebra import *


def test_Both_No_Attributes():
    r1 = Relation("R1")
    r2 = Relation("R2")
    t = FullOuterJoin(r1, r2)
    result = t.evaluate()
    assert result.attributes == []
    assert result.rows == set()


def test_Left_No_Attributes_Right_Has_Attributes():
    r1 = Relation("R1")
    r2 = Relation("R2")
    r2.add_attributes(["a"])
    r2.add_rows([[1]])
    t = FullOuterJoin(r1, r2)
    result = t.evaluate()
    assert result.get_attribute_names(result.attributes) == ["R1+R2.a"]
    assert set(result.rows) == {(1,)}


def test_Left_Has_Attributes_Right_No_Attributes():
    r1 = Relation("R1")
    r2 = Relation("R2")
    r1.add_attributes(["a"])
    r1.add_rows([[1]])
    t = FullOuterJoin(r1, r2)
    result = t.evaluate()
    assert result.get_attribute_names(result.attributes) == ["R1+R2.a"]
    assert set(result.rows) == {(1,)}


def test_No_Matching_Rows():
    r1 = Relation("R1")
    r2 = Relation("R2")
    r1.add_attributes(["a"])
    r1.add_rows([[1], [2]])
    r2.add_attributes(["a"])
    r2.add_rows([[3], [4]])
    t = FullOuterJoin(r1, r2)
    result = t.evaluate()
    assert result.get_attribute_names(result.attributes) == ["R1+R2.a"]
    assert set(result.rows) == {(1,), (2,), (3,), (4,)}


def test_Partial_Match():
    r1 = Relation("R1")
    r2 = Relation("R2")
    r1.add_attributes(["a"])
    r1.add_rows([[1], [2]])
    r2.add_attributes(["a"])
    r2.add_rows([[2], [3]])
    t = FullOuterJoin(r1, r2)
    result = t.evaluate()
    assert result.get_attribute_names(result.attributes) == ["R1+R2.a"]
    assert set(result.rows) == {(1,), (2,), (3,)}


def test_Different_Attributes():
    r1 = Relation("R1")
    r2 = Relation("R2")
    r1.add_attributes(["a"])
    r1.add_rows([[1], [2]])
    r2.add_attributes(["b"])
    r2.add_rows([[10], [20]])
    t = FullOuterJoin(r1, r2)
    result = t.evaluate()
    assert set(result.get_attribute_names(result.attributes)) == {"R1+R2.a", "R1+R2.b"}
    expected_rows = {(1, 10), (1, 20), (2, 10), (2, 20)}
    assert set(result.rows) == expected_rows


def test_fullouterjoin_typical_case():
    r1 = Relation("R1")
    r1.add_attributes(["a", "b"])
    r1.add_rows(
        [
            [1, "a"],
            [2, "b"],
            [3, "c"],
        ]
    )
    r2 = Relation("R2")
    r2.add_attributes(["a", "c"])
    r2.add_rows(
        [
            [2, "B"],
            [3, "C"],
            [4, "D"],
        ]
    )
    t = FullOuterJoin(r1, r2)
    result = t.evaluate()
    assert result.get_attribute_names(result.attributes) == [
        "R1+R2.a",
        "R1+R2.b",
        "R1+R2.c",
    ]
    assert set(result.rows) == {
        (1, "a", None),
        (2, "b", "B"),
        (3, "c", "C"),
        (4, None, "D"),
    }
