"""Monitor the Compose PostgreSQL service from Airflow 3.3."""

from __future__ import annotations

import logging
import os
from datetime import timedelta

import pendulum

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, task


LOGGER = logging.getLogger(__name__)
POSTGRES_CONNECTION_ID = "postgres_default"


@dag(
    dag_id="postgres_monitor",
    description="Monitor PostgreSQL availability, capacity, and activity.",
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    is_paused_upon_creation=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=4),
    tags=["monitoring", "postgres", "airflow-3.3"],
)
def postgres_monitor():
    @task(
        retries=2,
        retry_delay=timedelta(seconds=30),
        execution_timeout=timedelta(minutes=2),
    )
    def collect_and_check_metrics() -> dict[str, object]:
        maximum_connection_usage = float(
            os.environ.get("POSTGRES_CONNECTION_USAGE_MAX_PERCENT", "90")
        )
        if not 0 < maximum_connection_usage <= 100:
            raise ValueError(
                "POSTGRES_CONNECTION_USAGE_MAX_PERCENT must be greater than 0 "
                "and less than or equal to 100"
            )

        row = PostgresHook(postgres_conn_id=POSTGRES_CONNECTION_ID).get_first(
            """
            WITH connection_limit AS (
                SELECT setting::integer AS max_connections
                FROM pg_settings
                WHERE name = 'max_connections'
            ),
            connection_activity AS (
                SELECT
                    count(*)::integer AS total_connections,
                    count(*) FILTER (WHERE state = 'active')::integer
                        AS active_connections,
                    count(*) FILTER (
                        WHERE pid <> pg_backend_pid()
                          AND state <> 'idle'
                          AND query_start < clock_timestamp() - interval '5 minutes'
                    )::integer AS long_running_queries
                FROM pg_stat_activity
            )
            SELECT
                current_database(),
                version(),
                pg_is_in_recovery(),
                extract(epoch FROM clock_timestamp() - pg_postmaster_start_time())::bigint,
                activity.total_connections,
                activity.active_connections,
                limits.max_connections,
                round(
                    100.0 * activity.total_connections
                    / NULLIF(limits.max_connections, 0),
                    2
                ),
                pg_database_size(current_database()),
                coalesce(database_stats.deadlocks, 0),
                activity.long_running_queries
            FROM connection_activity AS activity
            CROSS JOIN connection_limit AS limits
            LEFT JOIN pg_stat_database AS database_stats
                ON database_stats.datname = current_database()
            """
        )
        if row is None:
            raise RuntimeError("PostgreSQL returned no monitoring metrics")

        metrics = {
            "database": row[0],
            "server_version": row[1],
            "in_recovery": bool(row[2]),
            "uptime_seconds": int(row[3]),
            "total_connections": int(row[4]),
            "active_connections": int(row[5]),
            "max_connections": int(row[6]),
            "connection_usage_percent": float(row[7]),
            "database_size_bytes": int(row[8]),
            "deadlocks": int(row[9]),
            "long_running_queries": int(row[10]),
        }

        LOGGER.info("PostgreSQL monitoring metrics: %s", metrics)

        if metrics["long_running_queries"]:
            LOGGER.warning(
                "PostgreSQL has %s non-idle queries running for more than five minutes",
                metrics["long_running_queries"],
            )

        if metrics["connection_usage_percent"] >= maximum_connection_usage:
            raise RuntimeError(
                "PostgreSQL connection usage is "
                f"{metrics['connection_usage_percent']:.2f}%; configured maximum is "
                f"{maximum_connection_usage:.2f}%"
            )

        return metrics

    collect_and_check_metrics()


postgres_monitor()
