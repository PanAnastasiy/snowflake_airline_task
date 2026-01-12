from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
from utils import consts

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
}

with DAG(
        'reset_airline_dwh',
        default_args=default_args,
        catchup=False
) as dag:

    drop_database = SQLExecuteQueryOperator(
        task_id='drop_airline_database',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql=f"DROP DATABASE IF EXISTS {consts.DB_NAME} CASCADE;",
        hook_params={
            'warehouse': consts.SNOWFLAKE_WH,
        }
    )

    drop_database
