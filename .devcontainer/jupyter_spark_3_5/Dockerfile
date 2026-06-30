FROM jupyter/pyspark-notebook:x86_64-spark-3.5.0

USER root
RUN pip install cassandra-driver

RUN PYSPARK_HADOOP_VERSION=3 pip install "pyspark==3.5.8"

USER jovyan
