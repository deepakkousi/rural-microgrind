import pytest
import pandas as pd
import numpy as np
from app.engines.data_generator import generate_microgrid_dataset

def test_meter_data_shape():
    df = generate_microgrid_dataset(days=90, interval_minutes=15)
    assert df.shape[0] == 90 * 96 # Exactly 8640 intervals
    assert 'timestamp' in df.columns
    assert 'total_kw' in df.columns
    assert 'hvac_kw' in df.columns
    assert 'water_pump_kw' in df.columns
    assert 'lab_equipment_kw' in df.columns
    assert 'lighting_kw' in df.columns
    assert 'kitchen_kw' in df.columns
    assert 'it_network_kw' in df.columns
    assert 'solar_gen_kw' in df.columns
    assert 'tariff_period' in df.columns
    assert 'tariff_rate' in df.columns
    assert 'day_index' in df.columns

def test_timestamps_continuous_and_unique():
    df = generate_microgrid_dataset()
    # No duplicate timestamps
    assert df['timestamp'].nunique() == 8640
    # Continuous 15-minute steps
    ts_series = pd.to_datetime(df['timestamp'])
    diffs = ts_series.diff().dropna()
    assert (diffs == pd.Timedelta(minutes=15)).all()

def test_day_index_continuity():
    df = generate_microgrid_dataset()
    assert df['day_index'].min() == 1
    assert df['day_index'].max() == 90
    assert df['day_index'].nunique() == 90

def test_solar_and_grid_physics():
    df = generate_microgrid_dataset()
    assert (df['solar_gen_kw'] >= 0.0).all()
    assert (df['net_grid_kw'] >= 0.0).all()
    assert (df['total_kw'] > 0.0).all()

def test_tariff_periods_and_rates():
    df = generate_microgrid_dataset()
    periods = df['tariff_period'].unique()
    assert 'OFF_PEAK' in periods
    assert 'SHOULDER' in periods
    assert 'PEAK' in periods
    
    # Peak tariff rate must match 12.0
    peak_rates = df[df['tariff_period'] == 'PEAK']['tariff_rate'].unique()
    assert peak_rates[0] == 12.0
    
    # Off-peak tariff rate must match 4.5
    offpeak_rates = df[df['tariff_period'] == 'OFF_PEAK']['tariff_rate'].unique()
    assert offpeak_rates[0] == 4.5

def test_component_sum_explains_total():
    df = generate_microgrid_dataset()
    components = (df['it_network_kw'] + df['kitchen_kw'] + df['lighting_kw'] + 
                  df['water_pump_kw'] + df['hvac_kw'] + df['lab_equipment_kw'])
    # Subject to synthetic Gaussian noise (sigma=0.3), max residual should be within 1.5 kW
    residuals = np.abs(df['total_kw'] - components)
    assert residuals.mean() < 0.5
    assert residuals.max() < 2.0

def test_occupancy_correlation():
    df = generate_microgrid_dataset()
    assert (df['occupancy'] >= 0).all() and (df['occupancy'] <= 100).all()
    weekday_daytime = df[df['timestamp'].str.contains('T10:00:00')]['occupancy'].mean()
    assert weekday_daytime > 50.0 # High daytime occupancy
