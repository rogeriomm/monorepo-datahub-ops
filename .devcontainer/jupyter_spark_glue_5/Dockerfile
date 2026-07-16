FROM amazon/aws-glue-libs:5

RUN pip install --no-cache-dir \
    pandas parquet-tools kagglehub contexttimer rich findspark jupyterlab

COPY --chown=hadoop:hadoop user-settings/ /home/hadoop/.jupyter/lab/user-settings/
COPY --chown=hadoop:hadoop labconfig/ /home/hadoop/.jupyter/labconfig/

ENV PATH="/home/hadoop/.local/bin:${PATH}"
