# dags/scripts/validate.py
import pandas as pd
from typing import Dict, List, Tuple

class DataValidator:
    def __init__(self):
        self.validation_rules = {
            'temperature': {
                'min': 15,
                'max': 40,
                'type': float
            },
            'pressure': {
                'min': 950,
                'max': 1050,
                'type': float
            },
            'vibration': {
                'min': 0,
                'max': 2,
                'type': float
            },
            'sensor_id': {
                'type': int
            }
        }

    def validate_data(self, data: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Validate sensor data against predefined rules
        Returns: (valid_records, invalid_records)
        """
        valid_records = []
        invalid_records = []

        for record in data:
            is_valid = True
            validation_errors = []

            for field, rules in self.validation_rules.items():
                if field not in record:
                    is_valid = False
                    validation_errors.append(f"Missing field: {field}")
                    continue

                value = record[field]

                # Type validation
                if not isinstance(value, rules['type']):
                    try:
                        record[field] = rules['type'](value)
                    except (ValueError, TypeError):
                        is_valid = False
                        validation_errors.append(f"Invalid type for {field}: expected {rules['type'].__name__}")

                # Range validation
                if 'min' in rules and value < rules['min']:
                    is_valid = False
                    validation_errors.append(f"{field} below minimum: {value} < {rules['min']}")
                if 'max' in rules and value > rules['max']:
                    is_valid = False
                    validation_errors.append(f"{field} above maximum: {value} > {rules['max']}")

            if is_valid:
                valid_records.append(record)
            else:
                record['validation_errors'] = validation_errors
                invalid_records.append(record)

        return valid_records, invalid_records