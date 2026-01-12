#!/bin/bash

set -e

echo "Starting Airflow for Snowflake pipeline..."

airflow db upgrade

if [[ "$_AIRFLOW_WWW_USER_CREATE" == "true" ]]; then
    echo "Creating admin user..."
    airflow users create \
        --username "${_AIRFLOW_WWW_USER_USERNAME:-admin}" \
        --password "${_AIRFLOW_WWW_USER_PASSWORD:-admin}" \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com || true
    echo "Admin user check completed."
fi

exec "$@"