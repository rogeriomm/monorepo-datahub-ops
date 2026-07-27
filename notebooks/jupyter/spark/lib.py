from __future__ import annotations

import shlex
import sys
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame
from IPython.display import display

from dataclasses import dataclass, field
from typing import Mapping
from pyspark.sql import DataFrame, SparkSession
import warnings
from itables import show

from IPython.core.magic import register_line_magic, register_cell_magic


# Directories searched, in order, when %run_nb receives a bare file name.
# An empty string has the same meaning as an empty entry in PATH: the current
# working directory.
RUN_NB_PATH: list[str | Path] = ["", "/home/jovyan/work/spark"]

# Prevent SQL result display from collecting an unbounded DataFrame on the
# Jupyter driver. Override this module-level value if a different limit is needed.
SQL_DISPLAY_LIMIT = 1000


def _find_notebook(notebook_name: str, search_paths: Sequence[str | Path]) -> str:
    path = Path(notebook_name).expanduser()

    if path.suffix.lower() == ".ipynb":
        raise ValueError("Pass the notebook name without the .ipynb extension")

    path = path.with_name(f"{path.name}.ipynb")

    # As with a shell command containing '/', an explicitly qualified path is
    # not looked up in the search path.
    if path.is_absolute() or path.parent != Path("."):
        return str(path)

    for directory in search_paths:
        candidate = Path(directory or ".").expanduser() / path
        if candidate.is_file():
            return str(candidate)

    searched = ", ".join(str(Path(directory or ".").expanduser()) for directory in search_paths)
    raise FileNotFoundError(
        f"Notebook {path.name!r} was not found in RUN_NB_PATH: {searched or '(empty)'}"
    )


def viewdf(
    df: DataFrame,
    limit: int = 1000,
    page_length: int = 25
) -> None:
    """
    Display a Spark DataFrame as an interactive Jupyter table.

    Only `limit` rows are collected to the driver.
    """
    show(
        df.limit(limit).toPandas(),
        scrollX=True,
        scrollY="500px",
        scrollCollapse=True,
        pageLength=page_length,
        lengthMenu=[10, 25, 50, 100],
    )

def viewdf_pandas(
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


def run_nb(
    ipython,
    line: str,
    search_paths: Sequence[str | Path] | None = None,
):
    """
    Run an .ipynb notebook by name while forwarding arguments through sys.argv.

    Example:
        %run_nb ../start --data-format iceberg --port-offset 2

    The notebook name must not include the .ipynb extension. Bare names are
    searched for in RUN_NB_PATH, in order. Names that include a directory
    component are used directly.
    """
    arguments = shlex.split(line)

    if not arguments:
        raise ValueError(
            "Usage: %run_nb notebook-name [arguments]"
        )

    notebook = _find_notebook(arguments[0], RUN_NB_PATH if search_paths is None else search_paths)
    notebook_arguments = arguments[1:]

    original_argv = sys.argv.copy()

    try:
        sys.argv = [notebook, *notebook_arguments]
        return ipython.run_line_magic("run", notebook)
    finally:
        sys.argv = original_argv


def _split_sql_statements(sql: str) -> list[str]:
    """Split SQL on semicolons outside quoted strings and comments."""
    statements = []
    current = []
    quote = None
    in_line_comment = False
    block_comment_depth = 0
    has_code = False
    index = 0

    while index < len(sql):
        char = sql[index]
        following = sql[index + 1] if index + 1 < len(sql) else ""

        if in_line_comment:
            current.append(char)
            if char == "\n":
                in_line_comment = False
            index += 1
            continue

        if block_comment_depth:
            current.append(char)
            if char == "/" and following == "*":
                current.append(following)
                block_comment_depth += 1
                index += 2
            elif char == "*" and following == "/":
                current.append(following)
                block_comment_depth -= 1
                index += 2
            else:
                index += 1
            continue

        if quote:
            current.append(char)
            if char == "\\" and following:
                current.append(following)
                index += 2
            elif char == quote and following == quote:
                current.append(following)
                index += 2
            elif char == quote:
                quote = None
                index += 1
            else:
                index += 1
            continue

        if char == "-" and following == "-":
            current.extend((char, following))
            in_line_comment = True
            index += 2
        elif char == "/" and following == "*":
            current.extend((char, following))
            block_comment_depth = 1
            index += 2
        elif char in ("'", '"', "`"):
            current.append(char)
            quote = char
            has_code = True
            index += 1
        elif char == ";":
            if has_code:
                statements.append("".join(current).strip())
            current = []
            has_code = False
            index += 1
        else:
            current.append(char)
            has_code = has_code or not char.isspace()
            index += 1

    if has_code:
        statements.append("".join(current).strip())

    return statements


def run_sql(ipython, line: str, cell: str | None = None) -> None:
    """Run one or more SQL statements using ``spark`` from the notebook namespace."""
    sql = line if cell is None else "\n".join(part for part in (line, cell) if part)

    statements = _split_sql_statements(sql)
    if not statements:
        raise ValueError("Usage: %sql SQL-statement or %%sql followed by SQL")

    spark = ipython.user_ns.get("spark")
    if spark is None or not callable(getattr(spark, "sql", None)):
        raise RuntimeError(
            "The %sql and %%sql magics require a valid Spark session named 'spark'"
        )

    statement_count = len(statements)
    for number, statement in enumerate(statements, start=1):
        try:
            result = spark.sql(statement)
            viewdf(result, limit=SQL_DISPLAY_LIMIT)
        except Exception as error:
            context = f"SQL statement {number} of {statement_count} failed"
            if hasattr(error, "add_note"):
                error.add_note(context)
                raise
            raise RuntimeError(context) from error


def load_ipython_extension(ipython):
    ipython.register_magic_function(
        lambda line: run_nb(ipython, line),
        magic_kind="line",
        magic_name="run_nb",
    )
    ipython.register_magic_function(
        lambda line, cell=None: run_sql(ipython, line, cell),
        magic_kind="line_cell",
        magic_name="sql",
    )
