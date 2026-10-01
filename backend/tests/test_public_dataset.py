import os
import sys
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pytest
import pandas as pd
from data.validation.public_dataset_validation import PublicDatasetValidator, public_validator
from data.validation.metrics import calculate_mae, calculate_rmse, calculate_wape, calculate_mape

def test_public_dataset_file_exists():
    path = os.path.join(backend_dir, "data", "public", "redd_house1_sample.csv")
    assert os.path.exists(path), f"Public dataset file not found at {path}"

def test_public_dataset_loading_and_cleaning():
    path = os.path.join(backend_dir, "data", "public", "redd_house1_sample.csv")
    validator = PublicDatasetValidator()
    df = validator.load_and_validate(path)
    
    assert len(df) == 672
    assert "parsed_timestamp" in df.columns
    # Check no negative power values in consumption columns
    for col in ["mains_power_kw", "hvac_kw", "lighting_kw", "kitchen_kw", "electronics_kw"]:
        assert (df[col] >= 0.0).all()
        assert not df[col].isnull().any()

def test_public_dataset_schema_validation_failure(tmp_path):
    invalid_csv = tmp_path / "invalid_dataset.csv"
    # Missing hvac_kw and electronics_kw
    pd.DataFrame({"timestamp": ["2011-04-18T00:00:00"], "mains_power_kw": [1.2]}).to_csv(invalid_csv, index=False)
    
    validator = PublicDatasetValidator()
    with pytest.raises(ValueError, match="Missing required columns"):
        validator.load_and_validate(str(invalid_csv))

def test_public_dataset_tier_mapping():
    path = os.path.join(backend_dir, "data", "public", "redd_house1_sample.csv")
    validator = PublicDatasetValidator()
    df = validator.load_and_validate(path)
    df_mapped = validator.map_to_platform_tiers(df)
    
    assert "critical_kw" in df_mapped.columns
    assert "essential_kw" in df_mapped.columns
    assert "flexible_kw" in df_mapped.columns
    assert "reconstructed_kw" in df_mapped.columns
    assert (df_mapped["reconstructed_kw"] > 0).all()

def test_public_dataset_pipeline_execution():
    report = public_validator.evaluate_public_dataset()
    assert report["status"] == "VALIDATED"
    assert report["dataset_stats"]["record_count"] == 672
    assert report["dataset_stats"]["duration_days"] == 7.0
    
    metrics = report["evaluation_metrics"]
    assert metrics["sample_count"] == 672
    assert 0.05 < metrics["mae_kw"] < 0.15
    assert 0.05 < metrics["rmse_kw"] < 0.15
    assert metrics["wape_pct"] > 0.0
    assert metrics["energy_explained_pct"] > 80.0

def test_metrics_edge_cases():
    import numpy as np
    actual = np.array([1.0, 2.0, 3.0])
    estimated = np.array([1.0, 2.0, 3.0])
    assert calculate_mae(actual, estimated) == 0.0
    assert calculate_rmse(actual, estimated) == 0.0
    assert calculate_wape(actual, estimated) == 0.0
    assert calculate_mape(actual, estimated) == 0.0
