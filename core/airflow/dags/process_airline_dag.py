from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

from utils import consts

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
}

with DAG(
        'process_airline_data',
        default_args=default_args,
        catchup=False,
        tags=['snowflake', 'etl']
) as dag:

    upload_to_stage = SQLExecuteQueryOperator(
        task_id='upload_to_stage',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql=f"PUT file://{consts.FULL_FILE_PATH} @{consts.STAGE_NAME} AUTO_COMPRESS=FALSE OVERWRITE=TRUE;",
        hook_params={"warehouse": consts.SNOWFLAKE_WH},
    )

    ingest_raw = SQLExecuteQueryOperator(
        task_id='l1_ingest_raw',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql=f"CALL {consts.DB_NAME}.{consts.SCHEMA_RAW}.SP_INGEST_FLIGHTS_FROM_STAGE('{consts.FILE_NAME}')",
        hook_params={"warehouse": consts.SNOWFLAKE_WH},
    )

    process_integration = SQLExecuteQueryOperator(
        task_id='l2_process_integration',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql=f"CALL {consts.DB_NAME}.{consts.SCHEMA_INTEGRATION}.SP_TRANSFORM_AND_LOAD_FLIGHTS()",
        hook_params={"warehouse": consts.SNOWFLAKE_WH},
    )

    build_report = SQLExecuteQueryOperator(
        task_id='l3_build_report',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql=f"CALL {consts.DB_NAME}.{consts.SCHEMA_MART}.SP_BUILD_REPORT_FLIGHT_STATS()",
        hook_params={"warehouse": consts.SNOWFLAKE_WH},
    )

    upload_to_stage >> ingest_raw >> process_integration >> build_report
