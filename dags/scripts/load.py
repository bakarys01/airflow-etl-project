# dags/scripts/load.py
import pandas as pd
from sqlalchemy import create_engine


def load_to_postgres(**context):
    """Load transformed data to PostgreSQL."""
    # Get input file path from previous task
    input_path = context['task_instance'].xcom_pull(task_ids='transform_data')

    # Read CSV file
    df = pd.read_csv(input_path)

    # Create database connection
    engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres/airflow')

    # Load data to PostgreSQL
    table_name = 'sensor_metrics'
    df.to_sql(
        table_name,
        engine,
        if_exists='append',
        index=False
    )

    return f"Loaded {len(df)} records to {table_name}"