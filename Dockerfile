FROM apache/airflow:2.7.1

USER root


COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER airflow

RUN pip install --no-cache-dir apache-airflow-providers-snowflake pandas

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint.sh"]