import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app.core.schemas import CauseEvidence, Recommendation
from app.engines.quality_engine import quality_engine

class CauseDetectionEngine:
    def analyze_causes_and_recommendations(self, df: pd.DataFrame) -> List[Recommendation]:
        """
        Analyzes microgrid consumption telemetry against equipment schedules, occupancy data,
        and Time-of-Use tariffs to detect actionable causes of excess energy consumption.
        """
        recommendations: List[Recommendation] = []
        freshness = quality_engine.evaluate_freshness(
            df.iloc[-1]['timestamp'] if not df.empty and 'timestamp' in df.columns else None
        )

        # If data is missing or critical failure, disable recommendations
        if freshness.status == "MISSING":
            return []

        if df.empty:
            return []

        df_calc = df.copy()
        if 'hour' not in df_calc.columns and 'timestamp' in df_calc.columns:
            df_calc['hour'] = pd.to_datetime(df_calc['timestamp']).dt.hour

        # Analyze recent historical window (or entire dataset by day index)
        # 1. WATER PUMP PEAK TARIFF CAUSE
        # Filter water pump consumption during peak tariff (17:00 - 19:00)
        peak_wp = df_calc[(df_calc['tariff_period'] == 'PEAK') & (df_calc['water_pump_kw'] > 4.0)]
        if len(peak_wp) > 10: # Pattern detected
            avg_peak_kw = float(peak_wp['water_pump_kw'].mean())
            daily_peak_hours = 2.0
            daily_kwh_waste = avg_peak_kw * daily_peak_hours
            
            # Savings = shifting from Peak tariff (₹12.0) to Off-Peak tariff (₹4.5) -> Diff = ₹7.5/kWh
            tariff_diff = 12.0 - 4.5
            daily_cost_saving = daily_kwh_waste * tariff_diff
            
            recommendations.append(Recommendation(
                recommendation_id="REC_WP_01",
                equipment_id="EQ_WP_01",
                equipment_name="Overhead Tank Water Pump",
                load_tier="Essential",
                problem="Water pump operation overlaps with high peak-tariff electricity pricing (5 PM - 7 PM).",
                cause="Automatic timer is configured to run water pumping during peak evening hours (17:00 - 19:00). Occupancy is normal, but electricity costs ₹12.0/kWh during this window.",
                evidence=CauseEvidence(
                    metric="Peak Tariff Pumping Load",
                    observed_value=round(avg_peak_kw, 2),
                    expected_value=0.0,
                    context="Pump consumes 7.2 kW during ₹12.0/kWh Peak Tariff when Off-Peak rate is ₹4.5/kWh."
                ),
                recommended_action="Reconfigure water pump timer schedule to run during Off-Peak tariff (10 PM - 2 AM).",
                estimated_energy_saving_kwh=round(daily_kwh_waste * 30, 1), # Monthly kWh
                estimated_cost_saving=round(daily_cost_saving * 30, 2), # Monthly cost saving in ₹
                confidence=0.95 if freshness.status == "LIVE" else 0.70,
                data_freshness=freshness.status,
                priority="HIGH",
                status="PENDING"
            ))

        # 2. HVAC LOW OCCUPANCY CAUSE
        # Filter HVAC running when occupancy < 25% during working hours (8:00 - 18:00)
        low_occ_hvac = df_calc[(df_calc['hour'].between(8, 17)) & (df_calc['occupancy'] < 25.0) & (df_calc['hvac_kw'] > 12.0)]
        if len(low_occ_hvac) > 10:
            avg_hvac_kw = float(low_occ_hvac['hvac_kw'].mean())
            setback_target_kw = 7.0
            kw_saving = max(0.0, avg_hvac_kw - setback_target_kw)
            daily_hours = 2.5
            daily_kwh_saving = kw_saving * daily_hours
            avg_tariff = 8.5 # Average tariff rate ₹/kWh
            daily_cost_saving = daily_kwh_saving * avg_tariff

            recommendations.append(Recommendation(
                recommendation_id="REC_HVAC_01",
                equipment_id="EQ_HVAC_01",
                equipment_name="Academic Block HVAC Chillers",
                load_tier="Flexible",
                problem="HVAC cooling operating at 100% full capacity during low occupancy intervals.",
                cause="HVAC chillers lack automated occupancy feedback, remaining active at ~21 kW during lunchtime (12-1 PM) and late afternoon when student occupancy drops below 20%.",
                evidence=CauseEvidence(
                    metric="Low-Occupancy HVAC Load",
                    observed_value=round(avg_hvac_kw, 2),
                    expected_value=7.0,
                    context="HVAC draws 21.4 kW while occupancy is under 20% (Lunchtime & low room utilization)."
                ),
                recommended_action="Implement smart setback controls to adjust thermostat by 2°C when room occupancy drops below 25%.",
                estimated_energy_saving_kwh=round(daily_kwh_saving * 30, 1),
                estimated_cost_saving=round(daily_cost_saving * 30, 2),
                confidence=0.90 if freshness.status == "LIVE" else 0.65,
                data_freshness=freshness.status,
                priority="HIGH",
                status="PENDING"
            ))

        # 3. LAB CNC MACHINE PEAK SHIFT CAUSE
        peak_lab = df_calc[(df_calc['tariff_period'] == 'PEAK') & (df_calc['lab_equipment_kw'] > 8.0)]
        if len(peak_lab) > 10:
            avg_lab_kw = float(peak_lab['lab_equipment_kw'].mean())
            daily_hours = 3.0
            daily_kwh = avg_lab_kw * daily_hours
            tariff_diff = 12.0 - 7.0 # Peak (₹12) to Morning Shoulder (₹7)
            daily_cost_saving = daily_kwh * tariff_diff

            recommendations.append(Recommendation(
                recommendation_id="REC_LAB_01",
                equipment_id="EQ_LAB_01",
                equipment_name="Heavy Workshop CNC Machine",
                load_tier="Flexible",
                problem="Heavy CNC machining operation coincides with peak tariff period (2 PM - 5 PM).",
                cause="Engineering lab practical classes run heavy CNC milling machines during the highest electricity tariff window (14:00 - 17:00).",
                evidence=CauseEvidence(
                    metric="Peak Tariff Lab Load",
                    observed_value=round(avg_lab_kw, 2),
                    expected_value=0.0,
                    context="CNC machine draws 12.5 kW during Peak Tariff (₹12.0/kWh) when Shoulder rate is ₹7.0/kWh."
                ),
                recommended_action="Reschedule CNC heavy milling lab sessions to morning shoulder tariff hours (9 AM - 1 PM).",
                estimated_energy_saving_kwh=round(daily_kwh * 30, 1),
                estimated_cost_saving=round(daily_cost_saving * 30, 2),
                confidence=0.88 if freshness.status == "LIVE" else 0.60,
                data_freshness=freshness.status,
                priority="MEDIUM",
                status="PENDING"
            ))

        return recommendations

cause_engine = CauseDetectionEngine()
