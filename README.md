# Airflow ETL Pipeline for IoT Sensor Data

## Overview
ETL pipeline processing IoT sensor data (temperature, pressure, vibration) using Apache Airflow with Grafana monitoring dashboards.

## Features
- Real-time sensor data simulation
- Data validation and quality checks
- Data transformation and aggregation
- PostgreSQL storage
- Scheduled execution (5-minute intervals)
- Real-time monitoring with Grafana dashboards:
  - Temperature trends by location
  - Current pressure monitoring
  - Vibration analysis
  - Statistical overview

## Tech Stack
- Apache Airflow 2.7.1
- PostgreSQL 13
- Python 3.8
- Docker & Docker Compose
- Grafana (latest)

## Project Structure
```
airflow-etl-project/
├── dags/
│   ├── scripts/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   ├── validate.py
│   │   ├── alerts.py
│   │   └── metrics.py
│   └── sensor_etl_dag.py
├── data/
│   ├── raw/
│   └── processed/
├── grafana/
│   ├── provisioning/
│   │   ├── dashboards/
│   │   │   └── dashboard.yml
│   │   └── datasources/
│   │       └── postgresql.yml
│   └── dashboards/
│       └── sensor_metrics.json
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

## Accessing Services
* Airflow UI: http://localhost:8080
   * Username: admin
   * Password: admin
* Grafana Dashboard: http://localhost:3000
   * Username: admin
   * Password: admin

## Pipeline Details
1. Extract: Generates simulated sensor data
2. Validate: Checks data quality and rules
3. Transform: Aggregates and cleans data
4. Calculate Metrics: Computes statistics and detects anomalies
5. Load: Stores in PostgreSQL

## Monitoring
The Grafana dashboard provides:
* Real-time temperature monitoring by location
* Pressure gauge with thresholds
* Vibration trend analysis
* Statistical overview of all metrics

## Data Validation Rules
* Temperature range: 15-40°C
* Pressure range: 950-1050 hPa
* Vibration range: 0-2 units
* Timestamp validation
* Sensor ID verification

## Future Improvements
- [x] Data validation
- [x] Metrics calculation
- [x] Alerting system
- [x] Grafana dashboards
- [ ] AWS integration
- [ ] Unit tests
- [ ] API documentation

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.