# Airflow ETL Pipeline for IoT Sensor Data

## Overview
ETL pipeline processing IoT sensor data (temperature, pressure, vibration) using Apache Airflow.

## Features
- Real-time sensor data simulation
- Data transformation and aggregation
- PostgreSQL storage
- Scheduled execution (5-minute intervals)

## Tech Stack
- Apache Airflow 2.7.1
- PostgreSQL 13
- Python 3.8
- Docker & Docker Compose

## Project Structure
```
airflow-etl-project/
├── dags/
│   ├── scripts/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   └── sensor_etl_dag.py
├── data/
│   ├── raw/
│   └── processed/
├── docker/
└── docker-compose.yml
```

## Setup
1. Clone repository
2. Install Docker and Docker Compose
3. Run:
```bash
echo "AIRFLOW_UID=50000" > .env
docker-compose build
docker-compose up -d
```

## Pipeline Details
1. Extract: Generates simulated sensor data
2. Transform: Aggregates and cleans data
3. Load: Stores in PostgreSQL

## Monitoring
Access Airflow UI: http://localhost:8080
- Username: admin
- Password: admin

## Sample Output
```sql
SELECT * FROM sensor_metrics LIMIT 3;
```

## Future Improvements
- Add data validation
- Implement alerts
- Add visualization dashboards
- Real sensor data integration