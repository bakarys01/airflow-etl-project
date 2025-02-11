# dags/scripts/transform.py
import pandas as pd
import json
from datetime import datetime


def clean_sensor_data(df):
    """Clean and validate sensor data."""
    # Remove duplicates
    df = df.drop_duplicates()

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filter out invalid readings
    df = df[
        (df['temperature'].between(15, 40)) &
        (df['pressure'].between(950, 1050)) &
        (df['vibration'].between(0, 2))
        ]

    return df


def aggregate_sensor_data(df):
    """Aggregate sensor data by location and status."""
    agg_data = df.groupby(['location', 'status']).agg({
        'temperature': ['mean', 'min', 'max'],
        'pressure': ['mean', 'min', 'max'],
        'vibration': ['mean', 'min', 'max'],
        'sensor_id': 'count'
    }).reset_index()

    # Flatten column names
    agg_data.columns = ['_'.join(col).strip() for col in agg_data.columns.values]

    return agg_data


def transform_data(**context):
    """Transform sensor data from JSON file."""
    # Get input file path from previous task
    input_path = context['task_instance'].xcom_pull(task_ids='extract_data')

    # Read JSON file
    with open(input_path, 'r') as f:
        data = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Clean data
    df_cleaned = clean_sensor_data(df)

    # Aggregate data
    df_aggregated = aggregate_sensor_data(df_cleaned)

    # Save transformed data
    output_path = f"/opt/airflow/dags/data/processed/sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_aggregated.to_csv(output_path, index=False)

    return output_path
