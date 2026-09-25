"""Test the Compose S3 connection from Airflow 3.3."""

from __future__ import annotations

import logging
from datetime import timedelta

import pendulum

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk import dag, task


LOGGER = logging.getLogger(__name__)
S3_CONNECTION_ID = "aws_default"


@dag(
    dag_id="s3_connection_test",
    description="Check the TLS-enabled SeaweedFS S3 connection every five minutes.",
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    is_paused_upon_creation=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=4),
    tags=["test", "s3", "seaweedfs", "airflow-3.3"],
)
def s3_connection_test():
    @task(
        retries=2,
        retry_delay=timedelta(seconds=30),
        execution_timeout=timedelta(minutes=2),
    )
    def list_buckets() -> dict[str, object]:
        response = S3Hook(aws_conn_id=S3_CONNECTION_ID).get_conn().list_buckets()
        bucket_names = sorted(bucket["Name"] for bucket in response.get("Buckets", []))
        result = {
            "connection_id": S3_CONNECTION_ID,
            "bucket_count": len(bucket_names),
            "bucket_names": bucket_names,
        }
        LOGGER.info("S3 connection test result: %s", result)
        return result

    list_buckets()


s3_connection_test()
