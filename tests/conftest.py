import os
import sqlite3

import pandas as pd
import pytest


@pytest.fixture
def session():
    con = sqlite3.connect(":memory:", isolation_level="IMMEDIATE")
    cur = con.cursor()
    cur.execute("PRAGMA synchronous = 0;")
    cur.execute("PRAGMA journal_mode = OFF;")
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("PRAGMA automatic_index = ON;")

    # minimal basic table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS basic (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);"
    )
    cur.execute("INSERT INTO basic (name, age) VALUES ('John', 25);")
    cur.execute("INSERT INTO basic (name, age) VALUES ('Jane', 30);")
    cur.execute("INSERT INTO basic (name, age) VALUES ('Jack', 35);")
    cur.execute("INSERT INTO basic (name, age) VALUES ('Jill', 40);")
    cur.execute("INSERT INTO basic (name, age) VALUES ('Joe', 45);")
    con.commit()

    # circuits
    circuits_file_path = os.path.abspath("tests/resources/f1-dataset/circuits.csv")
    cur.execute(
        """CREATE TABLE circuits (
            circuitId serial PRIMARY KEY,
            circuitRef varchar(255),
            name varchar(255),
            location varchar(255),
            country varchar(255),
            lat real,
            lng real
        );"""
    )
    circuits = pd.read_csv(circuits_file_path)
    circuits.to_sql("circuits", con, if_exists="append", index=False)
    cur.execute(
        "CREATE UNIQUE INDEX circuits_circuitID_uindex ON circuits (circuitId);"
    )
    cur.execute("CREATE INDEX circuits_circuitRef_index ON circuits (circuitRef);")
    cur.execute("CREATE INDEX circuits_name_index ON circuits (name);")
    cur.execute("CREATE INDEX circuits_location_index ON circuits (location);")
    cur.execute("CREATE INDEX circuits_country_index ON circuits (country);")
    cur.execute("CREATE INDEX circuits_lat_index ON circuits (lat);")
    cur.execute("CREATE INDEX circuits_lng_index ON circuits (lng);")
    con.commit()

    # drivers
    drivers_file_path = os.path.abspath("tests/resources/f1-dataset/drivers.csv")
    cur.execute(
        """CREATE TABLE drivers (
            driverId serial PRIMARY KEY,
            driverRef varchar(255),
            number int,
            code varchar(255),
            forename varchar(255),
            surname varchar(255),
            dob varchar(255),
            nationality varchar(255)
        );"""
    )
    drivers = pd.read_csv(drivers_file_path)
    drivers.to_sql("drivers", con, if_exists="append", index=False)
    cur.execute("CREATE UNIQUE INDEX drivers_driverID_uindex ON drivers (driverId);")
    cur.execute("CREATE INDEX drivers_driverRef_index ON drivers (driverRef);")
    cur.execute("CREATE INDEX drivers_number_index ON drivers (number);")
    cur.execute("CREATE INDEX drivers_code_index ON drivers (code);")
    cur.execute("CREATE INDEX drivers_forename_index ON drivers (forename);")
    cur.execute("CREATE INDEX drivers_surname_index ON drivers (surname);")
    cur.execute("CREATE INDEX drivers_dob_index ON drivers (dob);")
    cur.execute("CREATE INDEX drivers_nationality_index ON drivers (nationality);")
    con.commit()

    # races
    races_file_path = os.path.abspath("tests/resources/f1-dataset/races.csv")
    cur.execute(
        """CREATE TABLE races (
            raceId serial PRIMARY KEY,
            year int,
            round int,
            circuitId int,
            name varchar(255),
            date varchar(255),
            time varchar(255),
            FOREIGN KEY (circuitId) REFERENCES circuits (circuitId)
        );"""
    )
    races = pd.read_csv(races_file_path)
    races.to_sql("races", con, if_exists="append", index=False)
    cur.execute("CREATE UNIQUE INDEX races_raceID_uindex ON races (raceId);")
    cur.execute("CREATE INDEX races_year_index ON races (year);")
    cur.execute("CREATE INDEX races_round_index ON races (round);")
    cur.execute("CREATE INDEX races_circuitId_index ON races (circuitId);")
    cur.execute("CREATE INDEX races_name_index ON races (name);")
    cur.execute("CREATE INDEX races_date_index ON races (date);")
    cur.execute("CREATE INDEX races_time_index ON races (time);")
    cur.execute(
        "CREATE INDEX races_raceID_circuitID_uindex ON races (raceId, circuitId)"
    )
    con.commit()

    # lapTimes
    lapTimes_file_path = os.path.abspath(
        "tests/resources/f1-dataset/lapTimes_reduced.csv"
    )
    cur.execute(
        """CREATE TABLE lapTimes (
            raceId int,
            driverId int,
            lap int,
            position int,
            time varchar(255),
            milliseconds int,
            FOREIGN KEY (raceID) REFERENCES races(raceID),
            FOREIGN KEY (driverID) REFERENCES drivers(driverID)
        );"""
    )
    lapTimes = pd.read_csv(lapTimes_file_path)
    lapTimes.to_sql("lapTimes", con, if_exists="append", index=False)
    cur.execute("CREATE INDEX lapTimes_raceId_index ON lapTimes (raceId);")
    cur.execute("CREATE INDEX lapTimes_driverId_index ON lapTimes (driverId);")
    cur.execute("CREATE INDEX lapTimes_lap_index ON lapTimes (lap);")
    cur.execute("CREATE INDEX lapTimes_position_index ON lapTimes (position);")
    cur.execute("CREATE INDEX lapTimes_time_index ON lapTimes (time);")
    cur.execute("CREATE INDEX lapTimes_milliseconds_index ON lapTimes (milliseconds);")
    cur.execute(
        "CREATE INDEX lapTimes_raceID_driverID_uindex ON lapTimes (raceId, driverId)"
    )
    cur.execute("CREATE INDEX lapTimes_lap_driverID_uindex ON lapTimes (lap, driverId)")
    cur.execute(
        "CREATE INDEX lapTimes_raceID_driverID_lap_uindex ON lapTimes (raceId, driverId, lap)"
    )
    con.commit()

    cur.execute("PRAGMA optimize;")
    con.commit()

    yield con

    con.close()
