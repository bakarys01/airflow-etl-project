# dags/sensor_etl_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from scripts.extract import extract_sensor_data
from scripts.transform import transform_data
from scripts.load import load_to_postgres

if not os.path.exists('/opt/airflow/dags/data/raw'):
    os.makedirs('/opt/airflow/dags/data/raw')
if not os.path.exists('/opt/airflow/dags/data/processed'):
    os.makedirs('/opt/airflow/dags/data/processed')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'sensor_etl_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    catchup=False
)

extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_sensor_data,
    dag=dag
)

transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load = PythonOperator(
    task_id='load_data',
    python_callable=load_to_postgres,
    dag=dag
)

extract >> transform >> load