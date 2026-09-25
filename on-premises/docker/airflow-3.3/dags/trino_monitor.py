"""Monitor the Compose Trino service from Airflow 3.3."""

from __future__ import annotations

import logging
import os
from datetime import timedelta

import pendulum

from airflow.providers.trino.hooks.trino import TrinoHook
from airflow.sdk import dag, task


LOGGER = logging.getLogger(__name__)
TRINO_CONNECTION_ID = "trino_default"


@dag(
    dag_id="trino_monitor",
    description="Monitor Trino availability, cluster nodes, queries, and transactions.",
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    is_paused_upon_creation=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=4),
    tags=["monitoring", "trino", "airflow-3.3"],
)
def trino_monitor():
    @task(
        retries=2,
        retry_delay=timedelta(seconds=30),
        execution_timeout=timedelta(minutes=2),
    )
    def collect_and_check_metrics() -> dict[str, object]:
        maximum_queued_queries = int(os.environ.get("TRINO_QUEUED_QUERIES_MAX", "10"))
        if maximum_queued_queries < 1:
            raise ValueError("TRINO_QUEUED_QUERIES_MAX must be at least 1")

        row = TrinoHook(trino_conn_id=TRINO_CONNECTION_ID).get_first(
            """
            WITH node_metrics AS (
                SELECT
                    count(*) AS total_nodes,
                    count_if(coordinator) AS coordinator_nodes,
                    count_if(lower(state) = 'active') AS active_nodes,
                    max(node_version) AS node_version
                FROM system.runtime.nodes
            ),
            query_metrics AS (
                SELECT
                    count_if(state = 'RUNNING') AS running_queries,
                    count_if(state = 'QUEUED') AS queued_queries,
                    count_if(state = 'FAILED') AS failed_queries,
                    count_if(
                        state = 'RUNNING'
                        AND created < current_timestamp - interval '5' minute
                    ) AS long_running_queries
                FROM system.runtime.queries
            ),
            transaction_metrics AS (
                SELECT count(*) AS open_transactions
                FROM system.runtime.transactions
            )
            SELECT
                nodes.total_nodes,
                nodes.coordinator_nodes,
                nodes.active_nodes,
                nodes.node_version,
                queries.running_queries,
                queries.queued_queries,
                queries.failed_queries,
                queries.long_running_queries,
                transactions.open_transactions
            FROM node_metrics AS nodes
            CROSS JOIN query_metrics AS queries
            CROSS JOIN transaction_metrics AS transactions
            """
        )
        if row is None:
            raise RuntimeError("Trino returned no monitoring metrics")

        metrics = {
            "total_nodes": int(row[0]),
            "coordinator_nodes": int(row[1]),
            "active_nodes": int(row[2]),
            "node_version": row[3],
            "running_queries": int(row[4]),
            "queued_queries": int(row[5]),
            "failed_queries": int(row[6]),
            "long_running_queries": int(row[7]),
            "open_transactions": int(row[8]),
        }

        LOGGER.info("Trino monitoring metrics: %s", metrics)

        if metrics["failed_queries"]:
            LOGGER.warning(
                "Trino reports %s recently failed queries",
                metrics["failed_queries"],
            )

        if metrics["long_running_queries"]:
            LOGGER.warning(
                "Trino has %s queries running for more than five minutes",
                metrics["long_running_queries"],
            )

        if metrics["total_nodes"] < 1 or metrics["coordinator_nodes"] < 1:
            raise RuntimeError("Trino has no visible active coordinator")

        if metrics["active_nodes"] != metrics["total_nodes"]:
            raise RuntimeError(
                f"Only {metrics['active_nodes']} of {metrics['total_nodes']} "
                "Trino nodes are active"
            )

        if metrics["queued_queries"] >= maximum_queued_queries:
            raise RuntimeError(
                f"Trino has {metrics['queued_queries']} queued queries; configured "
                f"maximum is {maximum_queued_queries}"
            )

        return metrics

    collect_and_check_metrics()


trino_monitor()
