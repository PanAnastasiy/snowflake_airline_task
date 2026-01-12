# ✈️ Snowflake + Airflow Airline DWH Project

![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=Snowflake&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Проект по построению корпоративного **Data Warehouse (DWH)** для анализа авиаперевозок.  
Реализован полный **ELT-цикл** с использованием **Snowflake** (хранение и вычисления) и **Apache Airflow** (оркестрация).

Проект демонстрирует production-подход к построению DWH с нативными возможностями Snowflake:  
**Streams, Stored Procedures, Internal Stages, Secure Views и Time Travel**.

---

## 🏗 Архитектура и решения

Проект реализует **многослойную архитектуру обработки данных**, построенную полностью на SQL и нативных механизмах Snowflake без использования dbt.

### 🔄 Data Flow (Поток данных)

#### 1️⃣ Ingestion (Загрузка данных)
- Исходный CSV-файл `airline_dataset.csv`
- Загружается в **Internal Stage Snowflake** с помощью команды `PUT`
- Контролируемая загрузка без внешних ETL-инструментов

#### 2️⃣ Layer 1: RAW (Landing Zone)
- Таблица: `RAW_FLIGHTS`
- Хранит сырые данные без трансформаций
- Используются **Snowflake Streams (`STR_RAW_FLIGHTS`)** для:
    - отслеживания новых вставок
    - инкрементальной обработки данных (CDC)

#### 3️⃣ Layer 2: INTEGRATION (Normalized)
- Трансформации выполняются через **SQL Stored Procedures**
- Данные нормализуются и разделяются на:
    - **Dimensions**: `DIM_PASSENGER`, `DIM_AIRPORT`
    - **Facts**: `FACT_FLIGHTS`
- Реализована логика **SCD Type 1 (UPSERT)** для измерений

#### 4️⃣ Layer 3: MART (Reporting)
- Агрегация данных для аналитики и отчетности
- Витрина: `RPT_FLIGHT_STATS`
- Примеры метрик:
    - статистика перелётов по континентам
    - задержки рейсов
    - распределение типов билетов

---

## 🛡 Ключевые особенности

### 🔐 Security
- **Row Level Security (RLS)**
- Реализована фильтрация данных по типу билета
- Используются:
    - Secure Views
    - Access Policies Snowflake

### 🧾 Audit & Logging
- Кастомная таблица `ETL_LOGS`
- Логируются:
    - статус выполнения процедур
    - количество обработанных строк
    - время выполнения

### 🕒 Time Travel
- Используется Snowflake Time Travel
- Возможности:
    - восстановление удалённых таблиц (`UNDROP`)
    - запросы данных «в прошлом»

---

## 📂 Структура проекта

```text

snowflake_airline_task/
│
├── core/
│   ├── airflow/
│   │   └── dags/
│   │      ├── data/                     # Data-related assets used by DAGs (e.g. CSV files)
│   │      ├── sql/                      # SQL scripts (DDL, Stored Procedures, Streams)
│   │      ├── utils/                    # Shared utilities, constants, helpers
│   │      ├── init_airline_dag.py       # DAG for Snowflake infrastructure initialization
│   │      ├── process_airline_dag.py    # Main ELT processing DAG
│   │      └── cleanup_airline_dag.py    # DAG for full DWH cleanup (DROP DATABASE)
│   │   
├── docker_compose/
│   └── app.yml                           # Docker Compose configuration for Airflow stack
│
├── Dockerfile                            # Custom Airflow Docker image
├── entrypoint.sh                         # Container entrypoint script
└── Makefile                              # Project CLI commands (Docker, Airflow, linting)

```

# Справочник команд

Если нужен ручной контроль, используйте отдельные команды:

| Команда | Описание |
| ----------------- | ------------------------------------------ |
| make up | Собрать и запустить Docker контейнеры |
| make down | Остановить и удалить Docker контейнеры |
| make shell | Зайти внутрь контейнера Airflow (bash) |
| make logs-airflow | Просмотр логов Airflow в реальном времени |
| make lint | Проверка SQL кода (SQLFluff) |
