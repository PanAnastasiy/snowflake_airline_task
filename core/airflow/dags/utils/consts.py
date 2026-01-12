import os

from .snowflake_config import SnowflakeEnvConfig

_config = SnowflakeEnvConfig()

SNOWFLAKE_CONN_ID = 'snowflake_default'

SNOWFLAKE_WH = _config.warehouse
SNOWFLAKE_ROLE = _config.role
DB_NAME = _config.database

SCHEMA_RAW = 'RAW'
SCHEMA_INTEGRATION = 'INTEGRATION'
SCHEMA_MART = 'MART'
SCHEMA_UTILS = 'UTILS'

STAGE_NAME = f"{DB_NAME}.{SCHEMA_UTILS}.RAW_DATA_STAGE"

DATA_DIR = "/opt/airflow/data/raw"
FILE_NAME = "airline_dataset.csv"
FULL_FILE_PATH = os.path.join(DATA_DIR, FILE_NAME)

SQL_INIT_FOLDER_NAME = 'sql/init'
