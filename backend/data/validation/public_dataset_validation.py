"""
Public Energy Dataset Validation Pipeline.
Validates the data-processing and disaggregation evaluation pipeline
against real-world energy datasets (e.g., REDD House 1).

Keeps public-data validation strictly separate from the synthetic microgrid experiment.
"""
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from data.validation.metrics import (
        calculate_mae,
        calculate_rmse,
        calculate_mape,
        calculate_wape,
        calculate_energy_explained_ratio,
        evaluate_disaggregation_performance
    )
except ImportError:
    from backend.data.validation.metrics import (
        calculate_mae,
        calculate_rmse,
        calculate_mape,
        calculate_wape,
        calculate_energy_explained_ratio,
        evaluate_disaggregation_performance
    )

class PublicDatasetValidator:
    REQUIRED_COLUMNS = [
        'timestamp',
        'mains_power_kw',
        'hvac_kw',
        'lighting_kw',
        'kitchen_kw',
        'electronics_kw'
    ]

    def __init__(self, dataset_name: str = "REDD House 1 Standardized"):
        self.dataset_name = dataset_name
        self.metadata = {
            "dataset_name": dataset_name,
            "source": "J. Zico Kolter and Matthew J. Johnson (MIT/Stanford, SustKDD 2011)",
            "url": "http://redd.csail.mit.edu/",
            "data_type": "Real-world residential building submetered power",
            "sampling_interval": "15-minute standard intervals",
            "classification": {
                "real_public_data": ["mains_power_kw", "hvac_kw", "lighting_kw", "kitchen_kw", "electronics_kw"],
                "synthetic_context_data": "NONE (ToU tariffs and student occupancy are NOT injected into public dataset)",
                "derived_data": ["MAE", "RMSE", "MAPE", "WAPE", "Energy Explained Ratio"]
            },
            "limitations": (
                "REDD is from a residential home in Cambridge, MA, USA, not a rural Indian microgrid. "
                "It validates algorithm robustness, schema validation, data cleaning, and disaggregation "
                "metrics on external real-world telemetry, keeping results strictly separate from the "
                "synthetic rural microgrid scenario."
            )
        }

    def load_and_validate(self, filepath: str) -> pd.DataFrame:
        """
        Loads public dataset CSV, validates schema, cleans missing/negative values,
        and ensures valid ISO-8601 timestamp index.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Public dataset not found at: {filepath}")

        df = pd.read_csv(filepath)

        # Validate schema
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Schema validation failed. Missing required columns: {missing_cols}")

        # Parse and validate timestamps
        try:
            df['parsed_timestamp'] = pd.to_datetime(df['timestamp'])
        except Exception as e:
            raise ValueError(f"Invalid timestamp format in dataset: {e}")

        # Sort and clean
        df = df.sort_values('parsed_timestamp').reset_index(drop=True)

        # Handle missing or null values via interpolation
        numeric_cols = [c for c in df.columns if c not in ['timestamp', 'parsed_timestamp']]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].interpolate(method='linear').bfill().ffill()
            # Enforce non-negative physical power bounds for consumption channels
            df[col] = df[col].clip(lower=0.0)

        return df

    def map_to_platform_tiers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Maps real submeter channels to the platform's load tiers:
        - Critical: electronics_kw (computing / networking)
        - Essential: lighting_kw + kitchen_kw
        - Flexible: hvac_kw (cooling / space conditioning)
        """
        df_mapped = df.copy()
        df_mapped['critical_kw'] = np.round(df_mapped['electronics_kw'], 3)
        df_mapped['essential_kw'] = np.round(df_mapped['lighting_kw'] + df_mapped['kitchen_kw'], 3)
        df_mapped['flexible_kw'] = np.round(df_mapped['hvac_kw'], 3)
        df_mapped['reconstructed_kw'] = np.round(
            df_mapped['critical_kw'] + df_mapped['essential_kw'] + df_mapped['flexible_kw'], 3
        )
        return df_mapped

    def evaluate_public_dataset(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes end-to-end public dataset validation pipeline and computes
        standardized disaggregation performance metrics against ground truth mains.
        """
        if filepath is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = os.path.join(base_dir, 'public', 'redd_house1_sample.csv')

        df = self.load_and_validate(filepath)
        df_mapped = self.map_to_platform_tiers(df)

        actual_mains = df_mapped['mains_power_kw'].to_numpy()
        reconstructed = df_mapped['reconstructed_kw'].to_numpy()

        # Compute standard evaluation metrics
        metrics = evaluate_disaggregation_performance(actual_mains, reconstructed)

        # Channel contribution breakdown
        total_energy_kwh = float(np.sum(actual_mains) * 0.25) # 15-min intervals = 0.25 hr
        channel_breakdown = {
            "hvac": {
                "mean_kw": float(round(df_mapped['hvac_kw'].mean(), 3)),
                "energy_kwh": float(round(df_mapped['hvac_kw'].sum() * 0.25, 2)),
                "percentage": float(round((df_mapped['hvac_kw'].sum() / max(0.1, df_mapped['mains_power_kw'].sum())) * 100, 1))
            },
            "lighting": {
                "mean_kw": float(round(df_mapped['lighting_kw'].mean(), 3)),
                "energy_kwh": float(round(df_mapped['lighting_kw'].sum() * 0.25, 2)),
                "percentage": float(round((df_mapped['lighting_kw'].sum() / max(0.1, df_mapped['mains_power_kw'].sum())) * 100, 1))
            },
            "kitchen": {
                "mean_kw": float(round(df_mapped['kitchen_kw'].mean(), 3)),
                "energy_kwh": float(round(df_mapped['kitchen_kw'].sum() * 0.25, 2)),
                "percentage": float(round((df_mapped['kitchen_kw'].sum() / max(0.1, df_mapped['mains_power_kw'].sum())) * 100, 1))
            },
            "electronics": {
                "mean_kw": float(round(df_mapped['electronics_kw'].mean(), 3)),
                "energy_kwh": float(round(df_mapped['electronics_kw'].sum() * 0.25, 2)),
                "percentage": float(round((df_mapped['electronics_kw'].sum() / max(0.1, df_mapped['mains_power_kw'].sum())) * 100, 1))
            },
            "unmetered_residual": {
                "mean_kw": float(round((df_mapped['mains_power_kw'] - df_mapped['reconstructed_kw']).mean(), 3)),
                "energy_kwh": float(round((df_mapped['mains_power_kw'] - df_mapped['reconstructed_kw']).sum() * 0.25, 2)),
                "percentage": float(round(((df_mapped['mains_power_kw'] - df_mapped['reconstructed_kw']).sum() / max(0.1, df_mapped['mains_power_kw'].sum())) * 100, 1))
            }
        }

        report = {
            "status": "VALIDATED",
            "timestamp": datetime.now().isoformat(),
            "metadata": self.metadata,
            "dataset_stats": {
                "record_count": len(df_mapped),
                "time_range_start": str(df_mapped['timestamp'].iloc[0]),
                "time_range_end": str(df_mapped['timestamp'].iloc[-1]),
                "duration_days": round(len(df_mapped) / 96.0, 1),
                "average_mains_kw": float(round(df_mapped['mains_power_kw'].mean(), 3)),
                "peak_mains_kw": float(round(df_mapped['mains_power_kw'].max(), 3)),
                "total_energy_kwh": round(total_energy_kwh, 2)
            },
            "evaluation_metrics": metrics,
            "channel_breakdown": channel_breakdown
        }

        return report

public_validator = PublicDatasetValidator()

if __name__ == "__main__":
    rep = public_validator.evaluate_public_dataset()
    print(json.dumps(rep, indent=2))
