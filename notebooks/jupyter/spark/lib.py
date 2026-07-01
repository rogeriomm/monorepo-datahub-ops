from __future__ import annotations
from typing import Optional
import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame
from IPython.display import display

from dataclasses import dataclass, field
from typing import Mapping
from pyspark.sql import DataFrame, SparkSession
import warnings

from IPython.core.magic import register_line_magic, register_cell_magic

def dispdf(
    df: SparkDataFrame,
    limit: int | None = None,
    max_columns: Optional[int] = None,
    max_rows: Optional[int] = None,
    width: int = 200,
) -> None:
    """
    Display a Spark DataFrame in Jupyter as a Pandas DataFrame.

    Args:
        df: Spark DataFrame
        limit: Number of rows to display (default: 20)
        max_columns: Max columns to display (None = unlimited)
        max_rows: Max rows to display (None = unlimited)
        width: Display width
    """
    warnings.filterwarnings("ignore")

    # Configure display options
    pd.set_option("display.max_columns", max_columns)
    pd.set_option("display.max_rows", max_rows)
    pd.set_option("display.width", width)

    # Convert safely
    if limit is None:
        pdf = df.toPandas()
    else:
        pdf = df.limit(limit).toPandas()

    display(pdf)
