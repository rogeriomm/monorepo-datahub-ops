from pathlib import Path
import sys

from IPython import get_ipython


ipython = get_ipython()

if ipython is not None:
    spark_dir = Path(__file__).resolve().parents[3] / "spark"
    spark_dir_str = str(spark_dir)

    if spark_dir.exists() and spark_dir_str not in sys.path:
        sys.path.insert(0, spark_dir_str)

    ipython.run_line_magic("load_ext", "lib")
