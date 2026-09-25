"""Ingest OpenSky state vectors into PostgreSQL from Airflow 3.3."""

from __future__ import annotations

import logging
from contextlib import closing
from datetime import timedelta
from typing import Any

import pendulum
import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, task


LOGGER = logging.getLogger(__name__)
POSTGRES_CONNECTION_ID = "postgres_default"
OPENSKY_STATES_URL = "https://opensky-network.org/api/states/all"

OPENSKY_COLUMNS = (
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
    "category",
)

INSERT_COLUMNS = OPENSKY_COLUMNS + ("time",)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS opensky_api_states_all (
    icao24                TEXT,
    callsign              TEXT,
    origin_country        TEXT,
    time_position         BIGINT,
    last_contact          BIGINT,
    longitude             DOUBLE PRECISION,
    latitude              DOUBLE PRECISION,
    baro_altitude         DOUBLE PRECISION,
    on_ground             BOOLEAN,
    velocity              DOUBLE PRECISION,
    true_track            DOUBLE PRECISION,
    vertical_rate         DOUBLE PRECISION,
    sensors               BIGINT[],
    geo_altitude          DOUBLE PRECISION,
    squawk                TEXT,
    spi                   BOOLEAN,
    position_source       INTEGER,
    category              INTEGER,
    time                  BIGINT
)
"""


def normalize_state(state: list[Any], snapshot_time: int) -> tuple[Any, ...]:
    if len(state) not in (17, 18):
        raise ValueError(f"OpenSky returned a state vector with {len(state)} fields")

    values = dict(zip(OPENSKY_COLUMNS, state, strict=False))
    return tuple(values.get(column) for column in OPENSKY_COLUMNS) + (snapshot_time,)


def fetch_opensky_states() -> tuple[list[tuple[Any, ...]], int]:
    response = requests.get(OPENSKY_STATES_URL, timeout=30)
    response.raise_for_status()

    payload = response.json()
    snapshot_time = int(payload["time"])
    states = payload.get("states") or []
    return [normalize_state(state, snapshot_time) for state in states], snapshot_time


@dag(
    dag_id="opensky_ingest",
    description="Ingest OpenSky state vectors into the Airflow PostgreSQL connection.",
    schedule="*/20 * * * *",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    is_paused_upon_creation=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=10),
    tags=["opensky", "postgres", "airflow-3.3"],
)
def opensky_ingest():
    @task(
        retries=2,
        retry_delay=timedelta(minutes=1),
        execution_timeout=timedelta(minutes=5),
    )
    def fetch_and_insert() -> dict[str, int]:
        records, snapshot_time = fetch_opensky_states()
        if not records:
            LOGGER.info("OpenSky returned no state vectors for snapshot %s", snapshot_time)
            return {"snapshot_time": snapshot_time, "inserted_rows": 0}

        hook = PostgresHook(postgres_conn_id=POSTGRES_CONNECTION_ID)
        placeholders = ", ".join(["%s"] * len(INSERT_COLUMNS))
        insert_sql = (
            f"INSERT INTO opensky_api_states_all ({', '.join(INSERT_COLUMNS)}) "
            f"VALUES ({placeholders})"
        )

        with closing(hook.get_conn()) as connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_TABLE_SQL)
                    cursor.executemany(insert_sql, records)

        LOGGER.info(
            "Inserted %s OpenSky state vectors for snapshot %s",
            len(records),
            snapshot_time,
        )
        return {"snapshot_time": snapshot_time, "inserted_rows": len(records)}

    fetch_and_insert()


opensky_ingest()
