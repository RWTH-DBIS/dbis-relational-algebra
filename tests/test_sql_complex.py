import pytest

from relational_algebra import *


def test_track_refs(session):
    r = session.execute("SELECT circuitRef FROM circuits;")
    solution = set(r.fetchall())
    assert len(solution) > 0

    cR = Projection("circuits", "circuitRef").evaluate(sql_con=session)

    assert len(cR.rows) == len(solution)
    assert set(cR.rows) == solution


def test_tracks_germany(session):
    r = session.execute(
        "SELECT Name, Location FROM circuits WHERE Country = 'Germany';"
    )
    solution = set(r.fetchall())
    assert len(solution) > 0

    ra = Projection(
        Selection("circuits", Equals("Country", "Germany")), ["Name", "Location"]
    ).evaluate(sql_con=session)

    assert len(ra.rows) == len(solution)
    assert set(ra.rows) == solution


def test_tracks_northeast_southwest(session):
    r = session.execute(
        "SELECT * FROM circuits WHERE (Lat >= 0 AND Lng >= 0) OR (Lat < 0 AND Lng < 0);"
    )
    solution = set(r.fetchall())
    assert len(solution) > 0

    ra = Selection(
        "circuits",
        Or(
            And(GreaterEquals("Lat", 0), GreaterEquals("Lng", 0)),
            And(LessThan("Lat", 0), LessThan("Lng", 0)),
        ),
    ).evaluate(sql_con=session)

    assert len(ra.rows) == len(solution)
    assert set(ra.rows) == solution


@pytest.mark.skip("TDD: Not implemented yet")
def test_fastest_race_laps(session):
    r = session.execute(
        """SELECT circuits.name, drivers.forename, drivers.surname, lapTimes.milliseconds
        FROM circuits
        JOIN races ON circuits.circuitId = races.circuitId
        JOIN lapTimes ON races.raceId = lapTimes.raceId
        JOIN drivers ON lapTimes.driverId = drivers.driverId
        WHERE NOT EXISTS (
            SELECT *
            FROM lapTimes lT
            WHERE lT.raceId = lapTimes.raceId
            AND (lapTimes.driverID != lT.driverID OR lapTimes.lap != lT.lap)
            AND lapTimes.milliseconds < lT.milliseconds
        );"""
    )
    solution = set(r.fetchall())
    assert len(solution) > 0

    ra = Projection(
        NaturalJoin(
            NaturalJoin("circuits", "races"), NaturalJoin("lapTimes", "drivers")
        ),
        [
            "circuits.name",
            "drivers.forename",
            "drivers.surname",
            "lapTimes.milliseconds",
        ],
    ) - Projection(
        ThetaJoin(
            NaturalJoin(
                NaturalJoin("circuits", "races"), NaturalJoin("lapTimes", "drivers")
            ),
            Rename("lapTimes", "lT"),
            And(
                And(
                    Equals("lT.raceId", "lapTimes.raceId"),
                    Or(
                        Not(Equals("lapTimes.driverID", "lT.driverID")),
                        Not(Equals("lapTimes.lap", "lT.lap")),
                    ),
                ),
                LessThan("lapTimes.milliseconds", "lT.milliseconds"),
            ),
        ),
        [
            "circuits.name",
            "drivers.forename",
            "drivers.surname",
            "lapTimes.milliseconds",
        ],
    )
    ra = ra.evaluate(sql_con=session)

    assert len(ra.rows) == len(solution)
    assert set(ra.rows) == solution
