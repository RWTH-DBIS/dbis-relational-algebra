import pytest

from relational_algebra import *


@pytest.mark.skip(reason="not implemented")
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


@pytest.mark.skip(reason="not implemented")
def test_crossproduct(session):
    r = session.execute("SELECT * FROM circuits c1, circuits c2;")
    solution = set(r.fetchall())
    assert len(solution) > 0

    cR = (
        Rename(Relation("circuits"), "c1") * Rename(Relation("circuits"), "c2")
    ).evaluate(sql_con=session)

    assert len(cR.rows) == len(solution)
    assert set(cR.rows) == solution


@pytest.mark.skip(reason="not implemented")
def test_projection(session):
    r = session.execute("SELECT lt.raceId, lt.lap FROM lapTimes lt;")
    solution = set(r.fetchall())
    assert len(solution) > 0

    cR = Projection(
        Rename(Relation("LapTimes"), "lt"), ["lt.raceId", "lt.lap"]
    ).evaluate(sql_con=session)

    assert len(cR.rows) == len(solution)
    assert set(cR.rows) == solution


@pytest.mark.skip(reason="Taking way too long")
def test_big_naturaljoin(session):
    from datetime import datetime

    now = datetime.now()
    r = session.execute(
        "SELECT * FROM drivers NATURAL JOIN lapTimes NATURAL JOIN (SELECT raceId,year,round,circuitId,name,date FROM races);"
    )
    solution = set(r.fetchall())
    print(datetime.now() - now)
    assert len(solution) > 0

    now = datetime.now()
    cR = NaturalJoin(
        NaturalJoin("drivers", "lapTimes"),
        Projection("races", ["raceId", "year", "round", "circuitId", "name", "date"]),
    ).evaluate(sql_con=session)
    print(datetime.now() - now)
    assert len(cR.rows) == len(solution)
    assert set(cR.rows) == solution
