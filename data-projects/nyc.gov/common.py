import pyspark
import rich
import sys, os
import subprocess
import squid
from squid.spark.session import get_spark


def run(cmd:str):
    print(f"Command: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    print(result.stdout)
    return result.stdout

def show_spark_config(spark, names: list[str]):
    for name in names:
        value = spark.conf.get(name)
        print(f"{name}: {value}")

def sql(spark, query: str):
    df = spark.sql(query)
    df.show(truncate=False)

def run(cmd:str):
    print(f"Command: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    print(result.stdout)
    return result.stdout