import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
from app.core.loader import get_all_equipment, get_equipment_by_id

class DisaggregationEngine:
    def disaggregate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Disaggregates 15-minute telemetry into tier breakdowns (Critical, Essential, Flexible)
        and evaluates synthetic scenario disaggregation metrics (MAE, RMSE, MAPE).
        """
        if df.empty:
            return {}

        latest = df.iloc[-1]
        
        # Calculate components (in kW)
        lighting = float(max(0, latest.get('lighting_kw', 0.0)))
        hvac = float(max(0, latest.get('hvac_kw', 0.0)))
        water_pump = float(max(0, latest.get('water_pump_kw', 0.0)))
        lab_equipment = float(max(0, latest.get('lab_equipment_kw', 0.0)))
        kitchen = float(max(0, latest.get('kitchen_kw', 0.0)))
        it_network = float(max(0, latest.get('it_network_kw', 0.0)))
        
        total = float(latest.get('total_kw', 0.0))
        if total <= 0.0:
            total = lighting + hvac + water_pump + lab_equipment + kitchen + it_network

        # Tier breakdown
        critical_kw = round(it_network, 2)
        essential_kw = round(lighting * 0.6 + water_pump + kitchen, 2)
        flexible_kw = round(hvac + lab_equipment + lighting * 0.4, 2)

        # Percentage contribution
        denom = max(0.1, critical_kw + essential_kw + flexible_kw)
        pct_critical = round((critical_kw / denom) * 100, 1)
        pct_essential = round((essential_kw / denom) * 100, 1)
        pct_flexible = round((flexible_kw / denom) * 100, 1)

        # Disaggregation accuracy evaluation metrics against synthetic benchmark
        # Compare actual component sum vs unaggregated estimate
        component_sum = df['it_network_kw'] + df['kitchen_kw'] + df['lighting_kw'] + df['water_pump_kw'] + df['hvac_kw'] + df['lab_equipment_kw']
        total_series = df['total_kw']
        
        mae = float(np.mean(np.abs(total_series - component_sum)))
        rmse = float(np.sqrt(np.mean((total_series - component_sum) ** 2)))
        mape = float(np.mean(np.abs((total_series - component_sum) / np.maximum(0.1, total_series))) * 100)

        # Equipment detail breakdown
        equipment_list = get_all_equipment()
        detailed_loads = []
        
        for eq in equipment_list:
            ch_val = float(max(0, latest.get(eq.channel_key, 0.0)))
            # Split shared channels proportionally
            if eq.equipment_id == "EQ_IT_01":
                load_val = round(ch_val * 0.7, 2) # Server rack ~70% of IT
            elif eq.equipment_id == "EQ_IT_02":
                load_val = round(ch_val * 0.3, 2) # WiFi/Network ~30% of IT
            elif eq.equipment_id == "EQ_LT_01":
                load_val = round(ch_val * 0.6, 2) # Main security lighting
            elif eq.equipment_id == "EQ_LT_02":
                load_val = round(ch_val * 0.4, 2) # Classroom lighting
            elif eq.equipment_id == "EQ_LAB_01":
                load_val = round(ch_val * 0.75, 2) # CNC Machine
            elif eq.equipment_id == "EQ_LAB_02":
                load_val = round(ch_val * 0.25, 2) # 3D Printers
            else:
                load_val = round(ch_val, 2)

            pct = round((load_val / max(0.1, total)) * 100, 1)
            
            detailed_loads.append({
                "equipment_id": eq.equipment_id,
                "equipment_name": eq.equipment_name,
                "load_tier": eq.load_tier,
                "rated_power_kw": eq.rated_power_kw,
                "current_power_kw": load_val,
                "percentage": pct,
                "location": eq.location,
                "is_essential": eq.is_essential,
                "schedule": eq.schedule_description
            })

        return {
            "timestamp": latest.get('timestamp', datetime.now().isoformat()),
            "total_kw": round(total, 2),
            "tiers": {
                "critical": {"kw": critical_kw, "pct": pct_critical},
                "essential": {"kw": essential_kw, "pct": pct_essential},
                "flexible": {"kw": flexible_kw, "pct": pct_flexible}
            },
            "evaluation_metrics": {
                "mae_kw": round(mae, 3),
                "rmse_kw": round(rmse, 3),
                "mape_pct": round(mape, 2)
            },
            "detailed_loads": detailed_loads
        }

    def get_drilldown_evidence(self, df: pd.DataFrame, load_id: str) -> Dict[str, Any]:
        """
        Generates detailed time series evidence for a specific load tier / equipment channel.
        Includes Actual Load, Occupancy, Tariff, Schedule Alignment, and Non-Technical Cause.
        """
        if df.empty:
            return {}

        eq = get_equipment_by_id(load_id)
        ch_key = eq.channel_key
        
        # Take recent 24-hour window (96 intervals)
        sample = df.tail(96).copy()
        
        timeseries = []
        for idx, row in sample.iterrows():
            ch_val = float(max(0, row.get(ch_key, 0.0)))
            occ = float(row.get('occupancy', 0.0))
            tariff_r = float(row.get('tariff_rate', 0.0))
            tariff_p = str(row.get('tariff_period', 'OFF_PEAK'))
            h = int(pd.to_datetime(row['timestamp']).hour)
            
            # Expected schedule baseline estimation
            if eq.equipment_id == "EQ_WP_01":
                # Baseline expected pump off during peak tariff (17-19)
                expected_kw = 7.0 if (22 <= h or h < 2) else 0.0
            elif eq.equipment_id == "EQ_HVAC_01":
                # Expected HVAC proportional to occupancy
                expected_kw = (occ / 100.0) * 22.0 if (8 <= h < 18) else 0.0
            elif eq.equipment_id == "EQ_LAB_01":
                expected_kw = 12.0 if (9 <= h < 13) else 0.0
            else:
                expected_kw = ch_val * 0.9

            timeseries.append({
                "timestamp": row['timestamp'],
                "actual_kw": round(ch_val, 2),
                "expected_kw": round(expected_kw, 2),
                "occupancy_pct": round(occ, 1),
                "tariff_rate": tariff_r,
                "tariff_period": tariff_p
            })

        # Non-technical explanation synthesis
        if eq.equipment_id == "EQ_WP_01":
            cause = "Water pump operates during high-tariff evening hours (5 PM - 7 PM), incurring maximum electricity rate charges."
            recommendation = "Shift water pumping schedule to late night off-peak tariff (10 PM - 2 AM)."
        elif eq.equipment_id == "EQ_HVAC_01":
            cause = "HVAC cooling remains at 100% full power during low-occupancy periods (lunchtime & late afternoon), wasting power in empty spaces."
            recommendation = "Enable automated setback control to reduce cooling when occupancy drops below 25%."
        elif eq.equipment_id == "EQ_LAB_01":
            cause = "Heavy workshop CNC machinery is scheduled during peak tariff hours (2 PM - 5 PM)."
            recommendation = "Shift non-urgent workshop machining to morning shoulder tariff (9 AM - 1 PM)."
        else:
            cause = "Normal operational consumption within expected load parameters."
            recommendation = "Maintain current operational schedule."

        return {
            "equipment_id": eq.equipment_id,
            "equipment_name": eq.equipment_name,
            "load_tier": eq.load_tier,
            "location": eq.location,
            "rated_power_kw": eq.rated_power_kw,
            "is_essential": eq.is_essential,
            "schedule": eq.schedule_description,
            "cause_explanation": cause,
            "recommended_action": recommendation,
            "timeseries": timeseries
        }

disaggregation_engine = DisaggregationEngine()
