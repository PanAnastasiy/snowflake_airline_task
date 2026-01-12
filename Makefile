PROJECT_NAME = airflow_snowflake
DC = docker compose

AIRFLOW_COMPOSE = docker_compose/app.yml
AIRFLOW_CONTAINER = docker_compose-airflow-webserver-1

.PHONY: up
up:
	@echo "Starting Airflow containers..."
	$(DC) -f $(AIRFLOW_COMPOSE) up --build -d
	@echo "Airflow started! UI: http://localhost:8080"

.PHONY: down
down:
	@echo "Stopping containers..."
	$(DC) -f $(AIRFLOW_COMPOSE) down
	@echo "Stopped."

.PHONY: logs-airflow
logs-airflow:
	@echo "Streaming logs from Webserver..."
	$(DC) -f $(AIRFLOW_COMPOSE) logs -f airflow-webserver

.PHONY: install
install:
	@echo "Installing python dependencies locally..."
	poetry install --with dev

.PHONY: lint
lint:
	poetry run black .
	poetry run isort .
	poetry run flake8 .

.PHONY: clean-docker
clean-docker:
	@echo "Removing volumes and orphans..."
	$(DC) -f $(AIRFLOW_COMPOSE) down --volumes --remove-orphans
