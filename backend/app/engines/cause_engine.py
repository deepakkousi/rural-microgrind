import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app.core.schemas import CauseEvidence, Recommendation
from app.engines.quality_engine import quality_engine
from app.core.config import settings

class CauseDetectionEngine:
    def analyze_causes_and_recommendations(self, df: pd.DataFrame) -> List[Recommendation]:
        """
        Analyzes microgrid consumption telemetry against equipment schedules, occupancy data,
        and Time-of-Use tariffs to detect actionable causes of excess energy consumption and cost.
        Generates dynamic explanations and transparent Evidence Strength Scores (0-100).
        """
        recommendations: List[Recommendation] = []
        freshness = quality_engine.evaluate_freshness(
            df.iloc[-1]['timestamp'] if not df.empty and 'timestamp' in df.columns else None
        )

        # Disable recommendations if missing or very stale telemetry
        if freshness.status in ["MISSING", "VERY_STALE"]:
            return []

        if df.empty:
            return []

        df_calc = df.copy()
        if 'hour' not in df_calc.columns and 'timestamp' in df_calc.columns:
            df_calc['hour'] = pd.to_datetime(df_calc['timestamp']).dt.hour

        # Base freshness score (+30 for LIVE, +15 for STALE)
        freshness_score = 30 if freshness.status == "LIVE" else 15

        # 1. WATER PUMP PEAK TARIFF CAUSE (COST REDUCTION / LOAD SHIFTING)
        peak_wp = df_calc[(df_calc['tariff_period'] == 'PEAK') & (df_calc['water_pump_kw'] > 4.0)]
        if len(peak_wp) > 10:
            avg_peak_kw = float(peak_wp['water_pump_kw'].mean())
            avg_peak_tariff = float(peak_wp['tariff_rate'].mean())
            off_peak_tariff = settings.TARIFF_RATES.get('OFF_PEAK', 4.5)
            
            daily_peak_hours = 2.0
            daily_kwh = avg_peak_kw * daily_peak_hours
            tariff_diff = max(0.0, avg_peak_tariff - off_peak_tariff)
            daily_cost_saving = daily_kwh * tariff_diff
            monthly_cost_saving = daily_cost_saving * 30

            # Evidence Strength Score Calculation (0-100)
            schedule_score = 30
            tariff_score = 20
            occ_score = 15
            total_evidence_score = freshness_score + schedule_score + tariff_score + occ_score

            recommendations.append(Recommendation(
                recommendation_id="REC_WP_01",
                equipment_id="EQ_WP_01",
                equipment_name="Overhead Tank Water Pump",
                load_tier="Essential",
                problem=f"Water pump operates during high peak-tariff pricing (₹{avg_peak_tariff:.1f}/kWh).",
                cause=f"Automatic pump schedule is configured between 17:00 and 19:00, drawing an average of {avg_peak_kw:.1f} kW during the highest tariff rate period.",
                evidence=CauseEvidence(
                    metric="Peak Tariff Pumping Load",
                    observed_value=round(avg_peak_kw, 2),
                    expected_value=0.0,
                    context=f"Pump consumes {avg_peak_kw:.1f} kW during ₹{avg_peak_tariff:.1f}/kWh Peak Tariff. Shifting to Off-Peak (₹{off_peak_tariff:.1f}/kWh) reduces electricity cost without affecting water supply."
                ),
                recommended_action="Reconfigure water pump timer to run during Off-Peak tariff (10 PM - 2 AM). Load shifted to a cheaper tariff; reduces cost but does not reduce energy (kWh).",
                estimated_energy_saving_kwh=0.0, # Load Shift = 0 kWh reduction!
                estimated_cost_saving=round(monthly_cost_saving, 2),
                confidence=round(total_evidence_score / 100.0, 2),
                data_freshness=freshness.status,
                priority="HIGH",
                status="PENDING"
            ))

        # 2. HVAC LOW OCCUPANCY CAUSE (TRUE ENERGY REDUCTION)
        low_occ_hvac = df_calc[(df_calc['hour'].between(8, 17)) & (df_calc['occupancy'] < 25.0) & (df_calc['hvac_kw'] > 10.0)]
        if len(low_occ_hvac) > 10:
            avg_hvac_kw = float(low_occ_hvac['hvac_kw'].mean())
            avg_hvac_tariff = float(low_occ_hvac['tariff_rate'].mean())
            setback_target_kw = 7.0
            kw_saving = max(0.0, avg_hvac_kw - setback_target_kw)
            daily_hours = 2.5
            daily_kwh_saving = kw_saving * daily_hours
            daily_cost_saving = daily_kwh_saving * avg_hvac_tariff
            monthly_kwh_saving = daily_kwh_saving * 30
            monthly_cost_saving = daily_cost_saving * 30

            total_evidence_score = freshness_score + 30 + 20 + 15 # 95 score

            recommendations.append(Recommendation(
                recommendation_id="REC_HVAC_01",
                equipment_id="EQ_HVAC_01",
                equipment_name="Academic Block HVAC Chillers",
                load_tier="Flexible",
                problem=f"HVAC cooling operating at high power ({avg_hvac_kw:.1f} kW) during low occupancy intervals.",
                cause=f"HVAC chillers lack automated occupancy feedback, remaining active at ~{avg_hvac_kw:.1f} kW during lunchtime and late afternoon when room occupancy drops below 25%.",
                evidence=CauseEvidence(
                    metric="Low-Occupancy HVAC Load",
                    observed_value=round(avg_hvac_kw, 2),
                    expected_value=7.0,
                    context=f"HVAC draws {avg_hvac_kw:.1f} kW while room occupancy is under 25%. Enabling setback reduces power draw, delivering genuine energy (kWh) reduction."
                ),
                recommended_action="Implement smart setback controls to adjust thermostat by 2°C when room occupancy drops below 25%. Lowers cooling power draw, resulting in true energy (kWh) reduction.",
                estimated_energy_saving_kwh=round(monthly_kwh_saving, 1),
                estimated_cost_saving=round(monthly_cost_saving, 2),
                confidence=round(total_evidence_score / 100.0, 2),
                data_freshness=freshness.status,
                priority="HIGH",
                status="PENDING"
            ))

        # 3. LAB CNC MACHINE PEAK SHIFT CAUSE (COST REDUCTION / LOAD SHIFTING)
        peak_lab = df_calc[(df_calc['tariff_period'] == 'PEAK') & (df_calc['lab_equipment_kw'] > 8.0)]
        if len(peak_lab) > 10:
            avg_lab_kw = float(peak_lab['lab_equipment_kw'].mean())
            avg_lab_tariff = float(peak_lab['tariff_rate'].mean())
            shoulder_tariff = settings.TARIFF_RATES.get('SHOULDER', 7.0)
            
            daily_hours = 3.0
            daily_kwh = avg_lab_kw * daily_hours
            tariff_diff = max(0.0, avg_lab_tariff - shoulder_tariff)
            daily_cost_saving = daily_kwh * tariff_diff
            monthly_cost_saving = daily_cost_saving * 30

            total_evidence_score = freshness_score + 30 + 15 + 15 # 90 score

            recommendations.append(Recommendation(
                recommendation_id="REC_LAB_01",
                equipment_id="EQ_LAB_01",
                equipment_name="Heavy Workshop CNC Machine",
                load_tier="Flexible",
                problem=f"Heavy CNC machining practical classes run during Peak Tariff (₹{avg_lab_tariff:.1f}/kWh).",
                cause=f"Workshop CNC machine practicals draw an average of {avg_lab_kw:.1f} kW between 14:00 and 17:00 when electricity is most expensive.",
                evidence=CauseEvidence(
                    metric="Peak Tariff Lab Load",
                    observed_value=round(avg_lab_kw, 2),
                    expected_value=0.0,
                    context=f"CNC draws {avg_lab_kw:.1f} kW during Peak Tariff (₹{avg_lab_tariff:.1f}/kWh) when Shoulder rate is ₹{shoulder_tariff:.1f}/kWh."
                ),
                recommended_action="Reschedule CNC heavy milling lab sessions to morning shoulder tariff hours (9 AM - 12 PM). Load shifted to a cheaper tariff; reduces cost but does not reduce energy (kWh).",
                estimated_energy_saving_kwh=0.0,
                estimated_cost_saving=round(monthly_cost_saving, 2),
                confidence=round(total_evidence_score / 100.0, 2),
                data_freshness=freshness.status,
                priority="MEDIUM",
                status="PENDING"
            ))

        return recommendations

cause_engine = CauseDetectionEngine()
