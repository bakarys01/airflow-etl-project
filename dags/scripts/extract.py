# dags/scripts/extract.py
import requests
import json
from datetime import datetime
import random
from faker import Faker

fake = Faker()


def generate_sensor_data(num_records=100):
    """Generate synthetic IoT sensor data."""
    data = []
    for _ in range(num_records):
        timestamp = datetime.now().isoformat()
        sensor_id = random.randint(1, 10)
        record = {
            "timestamp": timestamp,
            "sensor_id": sensor_id,
            "temperature": round(random.uniform(20, 35), 2),
            "pressure": round(random.uniform(980, 1020), 2),
            "vibration": round(random.uniform(0, 1), 3),
            "location": fake.city(),
            "status": random.choice(["active", "maintenance", "error"])
        }
        data.append(record)
    return data


def extract_sensor_data(**context):
    """Extract sensor data and save to a JSON file."""
    data = generate_sensor_data()
    output_path = f"/opt/airflow/dags/data/raw/sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_path, 'w') as f:
        json.dump(data, f)

    return output_path