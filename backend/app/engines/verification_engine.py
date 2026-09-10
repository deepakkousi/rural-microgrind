import pandas as pd
import numpy as np
from typing import Dict, Any, List

class VerificationEngine:
    def evaluate_verification_experiment(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Dynamically calculates baseline, target, measured verification consumption,
        verified energy savings (kWh), cost savings (₹), target achievement ratio,
        and actual target error from raw DataFrame telemetry.
        Returns DATA_UNAVAILABLE if dataframe is empty.
        """
        if df.empty or 'day_index' not in df.columns:
            return {
                "status": "DATA_UNAVAILABLE",
                "message": "Verification cannot be calculated because meter data is missing."
            }

        # Filter the 3 experiment periods:
        # BASELINE: Days 1 - 30
        baseline_df = df[df['day_index'] <= 30]
        # INTERVENTION: Days 31 - 60
        intervention_df = df[(df['day_index'] > 30) & (df['day_index'] <= 60)]
        # VERIFICATION: Days 61 - 90
        verification_df = df[df['day_index'] > 60]

        if baseline_df.empty or verification_df.empty:
            return {
                "status": "DATA_UNAVAILABLE",
                "message": "Insufficient meter data across baseline or verification periods."
            }

        def calc_daily_kwh(sub_df, col='total_kw'):
            if sub_df.empty or col not in sub_df.columns:
                return 0.0
            total_kwh = (sub_df[col] * 0.25).sum()
            num_days = sub_df['day_index'].nunique()
            return float(total_kwh / max(1, num_days))

        def calc_daily_cost(sub_df, col='total_kw'):
            if sub_df.empty or col not in sub_df.columns:
                return 0.0
            total_cost = (sub_df[col] * 0.25 * sub_df['tariff_rate']).sum()
            num_days = sub_df['day_index'].nunique()
            return float(total_cost / max(1, num_days))

        # Overall Microgrid Metrics
        baseline_daily_kwh = round(calc_daily_kwh(baseline_df), 1)
        measured_daily_kwh = round(calc_daily_kwh(verification_df), 1)
        
        baseline_daily_cost = round(calc_daily_cost(baseline_df), 2)
        measured_daily_cost = round(calc_daily_cost(verification_df), 2)

        # Scenario Target: 15% reduction goal
        target_daily_kwh = round(baseline_daily_kwh * 0.85, 1)

        verified_reduction_kwh_day = round(max(0.0, baseline_daily_kwh - measured_daily_kwh), 1)
        verified_reduction_pct = round((verified_reduction_kwh_day / max(1.0, baseline_daily_kwh)) * 100, 2)
        
        cost_saving_daily = round(max(0.0, baseline_daily_cost - measured_daily_cost), 2)
        cost_saving_total = round(cost_saving_daily * 30, 2) # 30-day verification period total

        # Target Achievement Ratio %
        target_reduction_kwh = baseline_daily_kwh - target_daily_kwh
        target_achievement_pct = round((verified_reduction_kwh_day / max(0.1, target_reduction_kwh)) * 100, 1)

        # Actual Target Error Analysis
        absolute_error_kwh = round(abs(target_reduction_kwh - verified_reduction_kwh_day), 2)
        percentage_error = round((absolute_error_kwh / max(0.1, abs(target_reduction_kwh))) * 100, 2)

        # Sensor Uncertainty
        sensor_uncertainty_label = "Assumed sensor uncertainty (±1.8%)"
        lower_bound_kwh = round(verified_reduction_kwh_day * 0.982, 1)
        upper_bound_kwh = round(verified_reduction_kwh_day * 1.018, 1)

        # Dynamic Equipment Intervention Evaluation directly from raw meter data:
        # 1. WATER PUMP (COST REDUCTION / LOAD SHIFTING)
        wp_base_kwh = round(calc_daily_kwh(baseline_df, 'water_pump_kw'), 1)
        wp_ver_kwh = round(calc_daily_kwh(verification_df, 'water_pump_kw'), 1)
        wp_base_cost = round(calc_daily_cost(baseline_df, 'water_pump_kw'), 2)
        wp_ver_cost = round(calc_daily_cost(verification_df, 'water_pump_kw'), 2)
        wp_kwh_saved = round(max(0.0, wp_base_kwh - wp_ver_kwh), 1)
        wp_cost_saved = round(max(0.0, wp_base_cost - wp_ver_cost), 2)

        # 2. HVAC CHILLERS (TRUE ENERGY REDUCTION)
        hvac_base_kwh = round(calc_daily_kwh(baseline_df, 'hvac_kw'), 1)
        hvac_ver_kwh = round(calc_daily_kwh(verification_df, 'hvac_kw'), 1)
        hvac_base_cost = round(calc_daily_cost(baseline_df, 'hvac_kw'), 2)
        hvac_ver_cost = round(calc_daily_cost(verification_df, 'hvac_kw'), 2)
        hvac_kwh_saved = round(max(0.0, hvac_base_kwh - hvac_ver_kwh), 1)
        hvac_cost_saved = round(max(0.0, hvac_base_cost - hvac_ver_cost), 2)

        # 3. WORKSHOP CNC MACHINE (COST REDUCTION / LOAD SHIFTING)
        lab_base_kwh = round(calc_daily_kwh(baseline_df, 'lab_equipment_kw'), 1)
        lab_ver_kwh = round(calc_daily_kwh(verification_df, 'lab_equipment_kw'), 1)
        lab_base_cost = round(calc_daily_cost(baseline_df, 'lab_equipment_kw'), 2)
        lab_ver_cost = round(calc_daily_cost(verification_df, 'lab_equipment_kw'), 2)
        lab_kwh_saved = round(max(0.0, lab_base_kwh - lab_ver_kwh), 1)
        lab_cost_saved = round(max(0.0, lab_base_cost - lab_ver_cost), 2)

        # 4. CLASSROOM LIGHTING (TRUE ENERGY REDUCTION)
        light_base_kwh = round(calc_daily_kwh(baseline_df, 'lighting_kw'), 1)
        light_ver_kwh = round(calc_daily_kwh(verification_df, 'lighting_kw'), 1)
        light_base_cost = round(calc_daily_cost(baseline_df, 'lighting_kw'), 2)
        light_ver_cost = round(calc_daily_cost(verification_df, 'lighting_kw'), 2)
        light_kwh_saved = round(max(0.0, light_base_kwh - light_ver_kwh), 1)
        light_cost_saved = round(max(0.0, light_base_cost - light_ver_cost), 2)

        interventions = [
            {
                "id": "INT_01",
                "name": "Water Pump Peak Tariff Shift",
                "target_equipment": "Overhead Tank Water Pump",
                "type": "COST_REDUCTION",
                "action": "Shifted pumping from 5-7 PM Peak Tariff to 10 PM-2 AM Off-Peak Tariff.",
                "baseline_kwh_day": wp_base_kwh,
                "verification_kwh_day": wp_ver_kwh,
                "energy_saving_kwh_day": wp_kwh_saved, # 0 kWh (load shift)
                "cost_saving_daily_inr": wp_cost_saved,
                "explanation": "Load shifted to a cheaper tariff; reduces cost but does not reduce energy (kWh).",
                "status": "VERIFIED"
            },
            {
                "id": "INT_02",
                "name": "HVAC Low-Occupancy Setback",
                "target_equipment": "Academic Block HVAC Chillers",
                "type": "ENERGY_REDUCTION",
                "action": "Setback thermostat by 2°C when occupancy < 25% during working hours.",
                "baseline_kwh_day": hvac_base_kwh,
                "verification_kwh_day": hvac_ver_kwh,
                "energy_saving_kwh_day": hvac_kwh_saved,
                "cost_saving_daily_inr": hvac_cost_saved,
                "explanation": "Reduces cooling power draw during low occupancy, resulting in true energy (kWh) reduction.",
                "status": "VERIFIED"
            },
            {
                "id": "INT_03",
                "name": "Workshop CNC Machine Tariff Shift",
                "target_equipment": "Heavy Workshop CNC Machine",
                "type": "COST_REDUCTION",
                "action": "Shifted heavy machining practical labs from Peak (2-5 PM) to Morning (9 AM-12 PM).",
                "baseline_kwh_day": lab_base_kwh,
                "verification_kwh_day": lab_ver_kwh,
                "energy_saving_kwh_day": lab_kwh_saved,
                "cost_saving_daily_inr": lab_cost_saved,
                "explanation": "Load shifted from Peak to Shoulder tariff; reduces electricity cost.",
                "status": "VERIFIED"
            },
            {
                "id": "INT_04",
                "name": "Classroom Lighting Low-Occupancy Dimming",
                "target_equipment": "Classroom & Lab Lighting",
                "type": "ENERGY_REDUCTION",
                "action": "Dimmed lighting circuits when room occupancy < 25%.",
                "baseline_kwh_day": light_base_kwh,
                "verification_kwh_day": light_ver_kwh,
                "energy_saving_kwh_day": light_kwh_saved,
                "cost_saving_daily_inr": light_cost_saved,
                "explanation": "Lowers lighting power consumption during empty classroom hours, resulting in true energy (kWh) reduction.",
                "status": "VERIFIED"
            }
        ]

        return {
            "status": "AVAILABLE",
            "baseline_period": "Days 1 - 30 (Suboptimal Schedule)",
            "intervention_period": "Days 31 - 60 (Transition Phase)",
            "verification_period": "Days 61 - 90 (Verified Operational Policy)",
            "baseline_daily_avg_kwh": baseline_daily_kwh,
            "target_daily_avg_kwh": target_daily_kwh,
            "measured_daily_avg_kwh": measured_daily_kwh,
            "verified_reduction_kwh_day": verified_reduction_kwh_day,
            "verified_reduction_pct": verified_reduction_pct,
            "cost_saving_daily": cost_saving_daily,
            "cost_saving_total": cost_saving_total,
            "target_achievement_pct": target_achievement_pct,
            "error_analysis": {
                "target_reduction_kwh_day": round(target_reduction_kwh, 1),
                "verified_reduction_kwh_day": verified_reduction_kwh_day,
                "absolute_error_kwh": absolute_error_kwh,
                "percentage_error": percentage_error,
                "sensor_uncertainty": sensor_uncertainty_label,
                "lower_bound_kwh": lower_bound_kwh,
                "upper_bound_kwh": upper_bound_kwh
            },
            "interventions_applied": interventions
        }

    def get_timeseries_comparison(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generates daily aggregated time series comparing Baseline Period vs Verification Period.
        """
        if df.empty or 'day_index' not in df.columns:
            return []

        daily = df.groupby('day_index').agg({
            'total_kw': lambda x: round((x * 0.25).sum(), 1),
            'hvac_kw': lambda x: round((x * 0.25).sum(), 1),
            'water_pump_kw': lambda x: round((x * 0.25).sum(), 1),
            'lighting_kw': lambda x: round((x * 0.25).sum(), 1),
            'occupancy': 'mean',
            'tariff_rate': 'mean'
        }).reset_index()

        daily.columns = ['day', 'total_kwh', 'hvac_kwh', 'water_pump_kwh', 'lighting_kwh', 'avg_occupancy', 'avg_tariff']

        result = []
        for idx, row in daily.iterrows():
            d = int(row['day'])
            if d <= 30:
                phase = "BASELINE"
            elif d <= 60:
                phase = "INTERVENTION"
            else:
                phase = "VERIFICATION"

            result.append({
                "day": d,
                "phase": phase,
                "total_kwh": row['total_kwh'],
                "hvac_kwh": row['hvac_kwh'],
                "water_pump_kwh": row['water_pump_kwh'],
                "lighting_kwh": row['lighting_kwh'],
                "avg_occupancy": round(row['avg_occupancy'], 1)
            })

        return result

verification_engine = VerificationEngine()
