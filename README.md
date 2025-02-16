# Airflow ETL Pipeline for IoT Sensor Data

## Overview
ETL pipeline processing IoT sensor data (temperature, pressure, vibration) using Apache Airflow. Features data validation, metrics calculation, and anomaly detection.

## Features
- Real-time sensor data simulation
- Data validation with configurable rules
- Anomaly detection and alerting
- Metrics calculation and monitoring
- Data transformation and aggregation
- PostgreSQL storage
- Scheduled execution (5-minute intervals)

## Tech Stack
- Apache Airflow 2.7.1
- PostgreSQL 13
- Python 3.8
- Docker & Docker Compose
- Pandas for data processing
- JSON for data exchange

## Project Structure
```
airflow-etl-project/
├── dags/
│   ├── scripts/
│   │   ├── extract.py      # Data generation and extraction
│   │   ├── transform.py    # Data transformation
│   │   ├── load.py         # Database operations
│   │   ├── validate.py     # Data validation
│   │   ├── metrics.py      # Metrics calculation
│   │   └── alerts.py       # Alerting system
│   └── sensor_etl_dag.py   # Main DAG definition
├── data/
│   ├── raw/                # Raw sensor data
│   ├── processed/          # Transformed data
│   ├── validation/         # Validation results
│   └── metrics/           # Calculated metrics
├── docker/
└── docker-compose.yml
```

## Pipeline Details
1. **Extract**: Generates simulated sensor data with configurable parameters
2. **Validate**: Checks data quality and validates against predefined rules
3. **Transform**: Cleans and aggregates sensor data
4. **Calculate Metrics**: Computes statistics and detects anomalies
5. **Load**: Stores processed data in PostgreSQL

## Setup
1. Clone repository
```bash
git clone https://github.com/yourusername/airflow-etl-project.git
cd airflow-etl-project
```

2. Install Docker and Docker Compose

3. Configure environment:
```bash
echo "AIRFLOW_UID=50000" > .env
```

4. Start services:
```bash
docker-compose build
docker-compose up -d
```

## Monitoring
Access Airflow UI: http://localhost:8080
- Username: admin
- Password: admin

### Available Metrics
- Temperature statistics (min, max, average)
- Pressure trends
- Vibration anomalies
- Sensor health status

## Data Validation Rules
- Temperature range: 15-40°C
- Pressure range: 950-1050 hPa
- Vibration range: 0-2 units
- Timestamp validation
- Sensor ID verification

## Future Improvements
- [x] Data validation
- [x] Metrics calculation
- [x] Alerting system
- [ ] Grafana dashboards
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