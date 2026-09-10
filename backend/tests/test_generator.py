import pytest
from app.engines.data_generator import generate_microgrid_dataset

def test_meter_data_shape():
    df = generate_microgrid_dataset(days=90, interval_minutes=15)
    assert df.shape[0] == 90 * 96 # 8640 intervals
    assert 'timestamp' in df.columns
    assert 'total_kw' in df.columns
    assert 'hvac_kw' in df.columns
    assert 'water_pump_kw' in df.columns
    assert 'lab_equipment_kw' in df.columns
    assert 'tariff_period' in df.columns

def test_equipment_metadata():
    df = generate_microgrid_dataset()
    assert (df['total_kw'] > 0).all()
    assert (df['occupancy'] >= 0).all() and (df['occupancy'] <= 100).all()

def test_tariff_periods():
    df = generate_microgrid_dataset()
    periods = df['tariff_period'].unique()
    assert 'OFF_PEAK' in periods
    assert 'SHOULDER' in periods
    assert 'PEAK' in periods

def test_occupancy_correlation():
    df = generate_microgrid_dataset()
    weekday_occ = df[df['timestamp'].str.contains('T10:00:00')]['occupancy'].mean()
    assert weekday_occ > 50.0 # High daytime occupancy expected
