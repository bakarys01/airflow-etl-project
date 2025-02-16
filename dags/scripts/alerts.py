# dags/scripts/alerts.py
import logging
from typing import List, Dict


class AlertManager:
    def __init__(self):
        self.logger = logging.getLogger('airflow.task')
        self.alert_thresholds = {
            'temperature': {'min': 18, 'max': 35},
            'pressure': {'min': 970, 'max': 1030},
            'vibration': {'min': 0, 'max': 1.5}
        }

    def check_alerts(self, data: Dict) -> List[str]:
        """Check if any measurements exceed alert thresholds"""
        alerts = []

        for metric, thresholds in self.alert_thresholds.items():
            if metric in data:
                value = data[metric]
                if value < thresholds['min']:
                    alert_msg = f"LOW {metric.upper()}: {value} < {thresholds['min']}"
                    alerts.append(alert_msg)
                    self.logger.warning(alert_msg)
                if value > thresholds['max']:
                    alert_msg = f"HIGH {metric.upper()}: {value} > {thresholds['max']}"
                    alerts.append(alert_msg)
                    self.logger.warning(alert_msg)

        return alerts

    def send_alert(self, subject: str, message: str, to_email: str = None):
        """Log alert message"""
        self.logger.warning(f"ALERT - {subject}: {message}")