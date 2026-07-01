FROM jupyter/pyspark-notebook:x86_64-spark-3.5.0

USER root
RUN pip install --no-cache-dir \
    pandas parquet-tools kagglehub contexttimer rich findspark \
    # Jupyter "%load_ext autotime" \
    ipython-autotime \
    humanize

RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/jovyan \
  && chmod 0440 /etc/sudoers.d/jovyan

USER jovyan
