import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from app.core.config import settings

def generate_microgrid_dataset(days: int = 90, interval_minutes: int = 15) -> pd.DataFrame:
    """
    Generates a 90-day synthetic dataset with 15-minute intervals (8,640 records).
    Distinguishes ENERGY REDUCTION (HVAC setback, Classroom lighting dimming)
    from COST REDUCTION / LOAD SHIFTING (Water Pump peak shift, CNC lab shift).
    """
    np.random.seed(42) # Reproducible synthetic dataset
    
    records_per_day = (24 * 60) // interval_minutes
    total_records = days * records_per_day
    
    start_time = datetime(2026, 6, 1, 0, 0, 0)
    timestamps = [start_time + timedelta(minutes=i * interval_minutes) for i in range(total_records)]
    
    df = pd.DataFrame({'timestamp': timestamps})
    df['day_index'] = (df.index // records_per_day) + 1
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    df['is_weekend'] = df['timestamp'].dt.weekday >= 5
    
    # 1. Unified Tariff Assignment from settings.TARIFF_RATES (in ₹ / kWh)
    # Off-Peak: 22:00 - 06:00 (₹4.5/kWh)
    # Shoulder: 06:00 - 14:00, 19:00 - 22:00 (₹7.0/kWh)
    # Peak: 14:00 - 19:00 (₹12.0/kWh)
    rates = settings.TARIFF_RATES
    def get_tariff_info(hour):
        if 14 <= hour < 19:
            return 'PEAK', rates.get('PEAK', 12.0)
        elif 22 <= hour or hour < 6:
            return 'OFF_PEAK', rates.get('OFF_PEAK', 4.5)
        else:
            return 'SHOULDER', rates.get('SHOULDER', 7.0)
            
    tariff_data = df['hour'].apply(get_tariff_info)
    df['tariff_period'] = [t[0] for t in tariff_data]
    df['tariff_rate'] = [t[1] for t in tariff_data]

    # 2. Occupancy Pattern (%)
    base_occ = []
    for idx, row in df.iterrows():
        h = row['hour']
        is_wknd = row['is_weekend']
        if is_wknd:
            occ = np.random.uniform(5, 25)
        else:
            if 8 <= h < 12 or 13 <= h < 17:
                occ = np.random.uniform(75, 95)
            elif 12 <= h < 13: # Lunch drop
                occ = np.random.uniform(15, 30)
            elif 17 <= h < 20:
                occ = np.random.uniform(20, 40)
            else:
                occ = np.random.uniform(2, 10)
        base_occ.append(round(occ, 1))
    df['occupancy'] = base_occ

    # 3. Solar Generation (kW)
    solar_kw = []
    for idx, row in df.iterrows():
        h = row['hour'] + row['minute'] / 60.0
        if 6.0 <= h <= 18.0:
            solar = 35.0 * np.sin(np.pi * (h - 6.0) / 12.0)
            noise = np.random.normal(1.0, 0.15)
            solar = max(0.0, solar * noise)
        else:
            solar = 0.0
        solar_kw.append(round(solar, 2))
    df['solar_gen_kw'] = solar_kw

    # 4. IT / Network Load (Critical, ~4.8 kW constant 24/7)
    df['it_network_kw'] = np.round(4.8 + np.random.normal(0, 0.2, total_records), 2)
    df['it_network_kw'] = df['it_network_kw'].clip(lower=4.0)

    # 5. Kitchen Load (Essential, meal peaks 7-9 AM, 12-2 PM, 7-9 PM)
    kitchen = []
    for idx, row in df.iterrows():
        h = row['hour']
        if 7 <= h < 9 or 12 <= h < 14 or 19 <= h < 21:
            val = np.random.uniform(7.0, 10.0)
        elif 6 <= h < 22:
            val = np.random.uniform(2.0, 4.0)
        else:
            val = np.random.uniform(0.8, 1.5)
        kitchen.append(round(val, 2))
    df['kitchen_kw'] = kitchen

    # 6. Lighting Load (Security lighting at night, classroom lighting during day)
    # ACTION 4 EMBEDDED: Classroom Lighting low occupancy dimming during verification phase
    lighting = []
    for idx, row in df.iterrows():
        day = row['day_index']
        h = row['hour']
        occ = row['occupancy']
        
        if h >= 18 or h < 6:
            val = 7.5 + np.random.uniform(0, 0.8) # Security corridor lighting
        else:
            base_light = 2.0 + (occ / 100.0) * 5.5
            if day > 60 and occ < 25.0:
                # Dim classroom lighting by 2.0 kW during low occupancy in Verification phase (TRUE ENERGY REDUCTION)
                val = max(1.5, base_light - 2.0)
            else:
                val = base_light + np.random.uniform(0, 0.4)
        lighting.append(round(val, 2))
    df['lighting_kw'] = lighting

    # 7. Operational Actions across 3 periods:
    # BASELINE (Day 1-30), INTERVENTION (Day 31-60), VERIFICATION (Day 61-90)
    water_pump = []
    hvac = []
    lab_equipment = []

    for idx, row in df.iterrows():
        day = row['day_index']
        h = row['hour']
        occ = row['occupancy']

        # --- WATER PUMP (LOAD SHIFTING / COST REDUCTION) ---
        # Baseline: Pump runs during PEAK tariff (17:00 - 19:00). 14.4 kWh/day total.
        # Verification: Pump shifted to OFF-PEAK (22:00 - 00:00). Same 14.4 kWh/day total!
        if day <= 30:
            wp = np.random.uniform(6.8, 7.5) if (17 <= h < 19) else np.random.uniform(0.0, 0.3)
        elif day <= 60:
            if day % 2 == 0:
                wp = np.random.uniform(6.8, 7.5) if (22 <= h < 24) else np.random.uniform(0.0, 0.3)
            else:
                wp = np.random.uniform(6.8, 7.5) if (17 <= h < 19) else np.random.uniform(0.0, 0.3)
        else:
            wp = np.random.uniform(6.8, 7.5) if (22 <= h < 24) else np.random.uniform(0.0, 0.3)

        # --- HVAC CHILLERS (TRUE ENERGY REDUCTION) ---
        # Baseline: HVAC runs 8 AM - 6 PM at full capacity (18-24 kW) regardless of occupancy.
        # Verification: Setback control lowers chiller draw to 7.0 kW when occupancy < 25%.
        if day <= 30:
            hvc = np.random.uniform(18.0, 24.0) if (8 <= h < 18) else np.random.uniform(0.0, 1.5)
        elif day <= 60:
            if 8 <= h < 18:
                hvc = np.random.uniform(6.0, 9.0) if occ < 25.0 else np.random.uniform(16.0, 22.0)
            else:
                hvc = np.random.uniform(0.0, 1.0)
        else:
            if 8 <= h < 18:
                hvc = np.random.uniform(5.5, 8.5) if occ < 25.0 else np.random.uniform(15.0, 21.0)
            else:
                hvc = np.random.uniform(0.0, 1.0)

        # --- LAB EQUIPMENT CNC (LOAD SHIFTING / COST REDUCTION) ---
        # Baseline: CNC runs during PEAK tariff (14:00 - 17:00).
        # Verification: CNC shifted to Morning SHOULDER tariff (9:00 - 12:00). Same energy!
        if day <= 30:
            if 14 <= h < 17:
                lab = np.random.uniform(11.0, 14.0)
            elif 10 <= h < 14:
                lab = np.random.uniform(3.0, 5.0)
            else:
                lab = np.random.uniform(0.2, 0.8)
        elif day <= 60:
            if 9 <= h < 12:
                lab = np.random.uniform(10.0, 13.5)
            else:
                lab = np.random.uniform(0.5, 2.0)
        else:
            if 9 <= h < 12:
                lab = np.random.uniform(9.5, 13.0)
            else:
                lab = np.random.uniform(0.2, 0.8)

        water_pump.append(round(wp, 2))
        hvac.append(round(hvc, 2))
        lab_equipment.append(round(lab, 2))

    df['water_pump_kw'] = water_pump
    df['hvac_kw'] = hvac
    df['lab_equipment_kw'] = lab_equipment

    # 8. Total Microgrid kW & Net Grid kW
    raw_total = (df['it_network_kw'] + df['kitchen_kw'] + df['lighting_kw'] + 
                 df['water_pump_kw'] + df['hvac_kw'] + df['lab_equipment_kw'])
    
    df['total_kw'] = np.round(raw_total + np.random.normal(0, 0.3, total_records), 2)
    df['total_kw'] = df['total_kw'].clip(lower=1.0)
    df['net_grid_kw'] = np.round((df['total_kw'] - df['solar_gen_kw']).clip(lower=0.0), 2)

    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    clean_df = df[[
        'timestamp', 'total_kw', 'lighting_kw', 'hvac_kw',
        'water_pump_kw', 'lab_equipment_kw', 'kitchen_kw',
        'it_network_kw', 'solar_gen_kw', 'occupancy',
        'tariff_period', 'tariff_rate', 'net_grid_kw', 'day_index'
    ]].copy()

    return clean_df
