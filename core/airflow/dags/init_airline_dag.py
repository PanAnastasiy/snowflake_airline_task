from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
import os

from utils import consts

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_PATH = os.path.join(CURRENT_DIR, consts.SQL_INIT_FOLDER_NAME)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
}

with DAG(
        'init_airline_dwh',
        default_args=default_args,
        catchup=False,
        template_searchpath=[SQL_PATH],
        tags=['snowflake', 'init']
) as dag:

    common_params = {
        "warehouse": consts.SNOWFLAKE_WH,
        "database": consts.DB_NAME,
        "role": consts.SNOWFLAKE_ROLE
    }

    setup_infra = SQLExecuteQueryOperator(
        task_id='setup_infrastructure',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql='01_initialize_db_infrastructure.sql',
        hook_params=common_params,
    )

    create_tables = SQLExecuteQueryOperator(
        task_id='create_tables_ddl',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql='02_create_dwh_tables_ddl.sql',
        hook_params={"warehouse": consts.SNOWFLAKE_WH},
    )

    create_sp_ingest = SQLExecuteQueryOperator(
        task_id='create_sp_ingest',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql='03_create_sp_ingest_raw_flights.sql',
        hook_params={"warehouse": consts.SNOWFLAKE_WH},
    )

    create_sp_process = SQLExecuteQueryOperator(
        task_id='create_sp_process',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql='04_create_sp_process_normalized_flights.sql',
        hook_params={"warehouse": consts.SNOWFLAKE_WH},
    )

    create_sp_report = SQLExecuteQueryOperator(
        task_id='create_sp_report',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql='05_create_sp_build_flight_stats_report.sql',
        hook_params={"warehouse": consts.SNOWFLAKE_WH},
    )

    create_security = SQLExecuteQueryOperator(
        task_id='setup_security_rls',
        conn_id=consts.SNOWFLAKE_CONN_ID,
        sql='06_setup_security_rls.sql',
        hook_params={
            "warehouse": consts.SNOWFLAKE_WH,
            "database": consts.DB_NAME,
            "role": consts.SNOWFLAKE_ROLE
        },
    )

    setup_infra >> create_tables >> [
        create_sp_ingest,
        create_sp_process,
        create_sp_report,
        create_security
    ]
