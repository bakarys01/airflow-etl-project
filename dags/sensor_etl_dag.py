# dags/sensor_etl_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
import json
from scripts.extract import extract_sensor_data
from scripts.transform import transform_data
from scripts.load import load_to_postgres
from scripts.validate import DataValidator
from scripts.alerts import AlertManager
from scripts.metrics import MetricsCalculator
import json
from scripts.extract import extract_sensor_data
from scripts.transform import transform_data
from scripts.load import load_to_postgres
from scripts.validate import DataValidator
from scripts.alerts import AlertManager
from scripts.metrics import MetricsCalculator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False  # Désactivons les emails pour le moment
}

dag = DAG(
    'sensor_etl_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    catchup=False,
    tags=['sensors', 'iot']
)


def validate_and_alert(**context):
    """Validate data and generate alerts"""
    # Get data from previous task
    task_instance = context['task_instance']
    data_file = task_instance.xcom_pull(task_ids='extract_data')

    with open(data_file, 'r') as f:
        sensor_data = json.load(f)

    # Validate data
    validator = DataValidator()
    valid_records, invalid_records = validator.validate_data(sensor_data)

    # Check for alerts
    alert_manager = AlertManager()
    alerts = []
    for record in valid_records:
        record_alerts = alert_manager.check_alerts(record)
        if record_alerts:
            alerts.extend(record_alerts)

    # Send alerts if any
    if alerts:
        alert_message = "\n".join(alerts)
        alert_manager.send_alert(
            subject="Sensor Alert",
            message=alert_message,
            to_email=default_args['email'][0]
        )

    # Save validation results
    validation_result = {
        'total_records': len(sensor_data),
        'valid_records': len(valid_records),
        'invalid_records': len(invalid_records),
        'alerts': alerts
    }

    validation_file = f"/opt/airflow/data/validation/validation_{context['ts_nodash']}.json"
    with open(validation_file, 'w') as f:
        json.dump(validation_result, f)

    # Pass only valid records to next task
    output_file = f"/opt/airflow/data/raw/valid_sensor_data_{context['ts_nodash']}.json"
    with open(output_file, 'w') as f:
        json.dump(valid_records, f)

    return output_file


def calculate_metrics(**context):
    """Calculate and store metrics"""
    # Créer le répertoire metrics s'il n'existe pas
    os.makedirs("/opt/airflow/data/metrics", exist_ok=True)
    task_instance = context['task_instance']
    processed_data_file = task_instance.xcom_pull(task_ids='transform_data')

    # Read processed data
    df = pd.read_csv(processed_data_file)

    # Calculate metrics
    metrics_calculator = MetricsCalculator()
    daily_metrics = metrics_calculator.calculate_daily_metrics(df)
    anomalies = metrics_calculator.detect_anomalies(df)

    # Store metrics
    metrics_data = {
        'timestamp': context['ts'],
        'daily_metrics': daily_metrics,
        'anomalies': anomalies
    }

    metrics_file = f"/opt/airflow/data/metrics/metrics_{context['ts_nodash']}.json"
    with open(metrics_file, 'w') as f:
        json.dump(metrics_data, f)

    return metrics_file


# Tasks
extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_sensor_data,
    dag=dag
)

validate = PythonOperator(
    task_id='validate_data',
    python_callable=validate_and_alert,
    dag=dag
)

transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

calculate_metrics = PythonOperator(
    task_id='calculate_metrics',
    python_callable=calculate_metrics,
    dag=dag
)

load = PythonOperator(
    task_id='load_data',
    python_callable=load_to_postgres,
    dag=dag
)

# Set task dependencies
extract >> validate >> transform >> calculate_metrics >> load