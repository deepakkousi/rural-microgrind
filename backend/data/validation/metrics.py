"""
Energy Disaggregation Validation Metrics.
Provides standard, mathematically robust error metrics for comparing
aggregate and reconstructed submeter energy consumption channels.
"""
import numpy as np
from typing import Dict, Any, Union

FILTER_MIN_KWI = 0.05

def calculate_mae(actual: np.ndarray, estimated: np.ndarray) -> float:
    errors = np.abs(actual - estimated)
    return float(round(np.mean(errors), 4))

def calculate_rmse(actual: np.ndarray, estimated: np.ndarray) -> float:
    squared_errors = (actual - estimated) ** 2
    return float(round(np.sqrt(np.mean(squared_errors)), 4))

def calculate_mape(actual: np.ndarray, estimated: np.ndarray, min_threshold_kw: float = 0.05) -> float:
    mask = actual >= min_threshold_kw
    if np.sum(mask) == 0:
        return 0.0
    abs_pct_errors = np.abs(actual[mask] - estimated[mask]) / actual[mask]
    return float(round(np.mean(abs_pct_errors) * 100.0, 2))

def calculate_wape(actual: np.ndarray, estimated: np.ndarray) -> float:
    total_actual = float(np.sum(actual))
    if total_actual <= 0.0:
        return 0.0
    total_abs_error = float(np.sum(np.abs(actual - estimated)))
    return float(round((total_abs_error / total_actual) * 100.0, 2))

def calculate_energy_explained_ratio(actual: np.ndarray, component_sum: np.ndarray) -> float:
    total_actual = float(np.sum(actual))
    if total_actual <= 0.0:
        return 0.0
    return float(round((float(np.sum(component_sum)) / total_actual) * 100.0, 2))

def evaluate_disaggregation_performance(actual, estimated) -> Dict[str, Any]:
    act = np.asarray(actual, dtype=float)
    est = np.asarray(estimated, dtype=float)
    if len(act) == 0 or len(est) == 0 or len(act) != len(est):
        raise ValueError("Arrays must be non-empty and of matching length.")

    return {
        "sample_count": int(len(act)),
        "mae_kw": calculate_mae(act, est),
        "rmse_kw": calculate_rmse(act, est),
        "mape_pct": calculate_mape(act, est),
        "wape_pct": calculate_wape(act, est),
        "energy_explained_pct": calculate_energy_explained_ratio(act, est)
    }
