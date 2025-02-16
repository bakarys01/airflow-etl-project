# dags/scripts/metrics.py
from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta


class MetricsCalculator:
    def calculate_daily_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate daily aggregated metrics"""
        print("Available columns:", df.columns.tolist())  # Debug

        # Adapter les noms de colonnes en fonction de la transformation précédente
        metrics = {}

        # Vérifier et ajouter les métriques disponibles
        temperature_cols = [col for col in df.columns if 'temperature' in col.lower()]
        if temperature_cols:
            metrics['temperature'] = {
                'mean': df[temperature_cols[0]].mean(),
                'min': df[temperature_cols[0]].min(),
                'max': df[temperature_cols[0]].max()
            }

        pressure_cols = [col for col in df.columns if 'pressure' in col.lower()]
        if pressure_cols:
            metrics['pressure'] = {
                'mean': df[pressure_cols[0]].mean(),
                'min': df[pressure_cols[0]].min(),
                'max': df[pressure_cols[0]].max()
            }

        vibration_cols = [col for col in df.columns if 'vibration' in col.lower()]
        if vibration_cols:
            metrics['vibration'] = {
                'mean': df[vibration_cols[0]].mean(),
                'min': df[vibration_cols[0]].min(),
                'max': df[vibration_cols[0]].max()
            }

        return metrics

    def detect_anomalies(self, df: pd.DataFrame, window: int = 10) -> List[Dict]:
        """Detect anomalies using rolling statistics"""
        anomalies = []

        # Identifier la colonne de température
        temp_cols = [col for col in df.columns if 'temperature' in col.lower()]
        if not temp_cols:
            return anomalies  # Retourner une liste vide si pas de données de température

        temp_col = temp_cols[0]

        # Calculer les statistiques
        rolling_mean = df[temp_col].rolling(window=window, min_periods=1).mean()
        rolling_std = df[temp_col].rolling(window=window, min_periods=1).std()

        # Définir les seuils
        upper_bound = rolling_mean + 2 * rolling_std
        lower_bound = rolling_mean - 2 * rolling_std

        # Détecter les anomalies
        anomaly_indices = df[
            (df[temp_col] > upper_bound) |
            (df[temp_col] < lower_bound)
            ].index

        for idx in anomaly_indices:
            anomalies.append({
                'timestamp': str(df.index[idx]) if isinstance(df.index[idx], datetime) else str(idx),
                'value': float(df.loc[idx, temp_col]),
                'mean': float(rolling_mean[idx]),
                'std': float(rolling_std[idx]),
                'upper_bound': float(upper_bound[idx]),
                'lower_bound': float(lower_bound[idx])
            })

        return anomalies