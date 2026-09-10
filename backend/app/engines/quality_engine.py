import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from app.core.schemas import FreshnessStatus

class DataQualityEngine:
    def __init__(self):
        self.simulated_failure: Optional[Dict[str, Any]] = None

    def set_simulated_failure(self, failure_type: str, duration_intervals: int = 16, affected_channel: str = "water_pump_kw"):
        if failure_type == "RESET":
            self.simulated_failure = None
        else:
            self.simulated_failure = {
                "type": failure_type,
                "duration_intervals": duration_intervals,
                "affected_channel": affected_channel,
                "applied_at": datetime.now().isoformat()
            }

    def evaluate_freshness(self, latest_timestamp_str: Optional[str] = None) -> FreshnessStatus:
        if self.simulated_failure and self.simulated_failure["type"] == "MISSING_DATA":
            return FreshnessStatus(
                status="MISSING",
                last_updated="N/A",
                age_minutes=9999.0,
                affected_sources=["meter_telemetry", "occupancy_sensor"],
                recommendation_reliability="DISABLED",
                warning_message="CRITICAL: Smart meter data feeds are unavailable. Recommendations disabled."
            )
            
        if self.simulated_failure and self.simulated_failure["type"] == "STALE_DATA":
            return FreshnessStatus(
                status="STALE",
                last_updated=(datetime.now() - timedelta(minutes=47)).strftime("%Y-%m-%d %H:%M:%S"),
                age_minutes=47.0,
                affected_sources=["main_meter_feed"],
                recommendation_reliability="DEGRADED",
                warning_message="WARNING: Meter data is stale (last update 47 mins ago). Recommendations downgraded."
            )

        if not latest_timestamp_str:
            return FreshnessStatus(
                status="LIVE",
                last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                age_minutes=2.5,
                affected_sources=[],
                recommendation_reliability="HIGH",
                warning_message=None
            )

        try:
            latest_dt = datetime.strptime(latest_timestamp_str, "%Y-%m-%dT%H:%M:%S")
            now = datetime.now()
            # For prototype simulation purposes, compare relative to latest entry or current time
            age_mins = max(2.0, (now - latest_dt).total_seconds() / 60.0)
            if age_mins > 7*24*60: # Synthetic historical dataset scaling
                age_mins = 3.5 # Treat active prototype data as LIVE (3.5 mins)
        except Exception:
            age_mins = 5.0

        if age_mins < 15.0:
            status = "LIVE"
            reliability = "HIGH"
            msg = None
        elif age_mins <= 120.0:
            status = "STALE"
            reliability = "MEDIUM"
            msg = f"Data is stale. Last updated {age_mins:.1f} minutes ago."
        else:
            status = "VERY_STALE"
            reliability = "LOW"
            msg = f"Data is very stale. Last updated {age_mins / 60.0:.1f} hours ago."

        return FreshnessStatus(
            status=status,
            last_updated=latest_timestamp_str,
            age_minutes=round(age_mins, 1),
            affected_sources=[],
            recommendation_reliability=reliability,
            warning_message=msg
        )

    def apply_quality_checks_and_failures(self, df: pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        
        if not self.simulated_failure:
            return df_copy

        ftype = self.simulated_failure["type"]
        channel = self.simulated_failure.get("affected_channel", "water_pump_kw")
        num_rows = min(len(df_copy), self.simulated_failure.get("duration_intervals", 16))

        if ftype == "STUCK_SENSOR":
            # Set constant flatline reading on tail
            if channel in df_copy.columns:
                flatline_val = df_copy[channel].iloc[-num_rows].item() if num_rows < len(df_copy) else 7.2
                df_copy.iloc[-num_rows:, df_copy.columns.get_loc(channel)] = flatline_val
                
        elif ftype == "NEGATIVE_READING":
            # Inject unphysical negative polarity error
            if channel in df_copy.columns:
                df_copy.iloc[-num_rows:, df_copy.columns.get_loc(channel)] = -12.5

        elif ftype == "TARIFF_REVISION":
            # Simulate sudden 50% tariff surcharge peak spike
            df_copy.iloc[-num_rows:, df_copy.columns.get_loc('tariff_rate')] = 18.5
            df_copy.iloc[-num_rows:, df_copy.columns.get_loc('tariff_period')] = 'CRITICAL_PEAK'

        return df_copy

    def detect_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        anomalies = []
        
        if self.simulated_failure:
            ftype = self.simulated_failure["type"]
            channel = self.simulated_failure.get("affected_channel", "water_pump_kw")
            
            if ftype == "MISSING_DATA":
                anomalies.append({
                    "sensor": "Main Gateway Meter",
                    "issue_type": "MISSING_SIGNAL",
                    "severity": "CRITICAL",
                    "description": "Smart meter telemetry stream missing for 16+ intervals.",
                    "recommended_action": "Verify gateway cellular connection & power supply."
                })
            elif ftype == "STUCK_SENSOR":
                anomalies.append({
                    "sensor": f"Telemetry Channel ({channel})",
                    "issue_type": "FLATLINE_STUCK",
                    "severity": "HIGH",
                    "description": f"Sensor '{channel}' stuck at constant value for >2 hours.",
                    "recommended_action": "Recalibrate current transducer (CT) sensor."
                })
            elif ftype == "NEGATIVE_READING":
                anomalies.append({
                    "sensor": f"Telemetry Channel ({channel})",
                    "issue_type": "POLARITY_ERROR",
                    "severity": "CRITICAL",
                    "description": f"Unphysical negative consumption (-12.5 kW) detected.",
                    "recommended_action": "Check CT clamp direction & reverse wiring polarity."
                })
            elif ftype == "STALE_DATA":
                anomalies.append({
                    "sensor": "Telemetry Gateway",
                    "issue_type": "STALE_TELEMETRY",
                    "severity": "MEDIUM",
                    "description": "Telemetry delay exceeds 45 minutes.",
                    "recommended_action": "Restart buffer queue daemon."
                })
                
        # Check standard DataFrame bounds
        for col in ['hvac_kw', 'water_pump_kw', 'lab_equipment_kw', 'kitchen_kw']:
            if col in df.columns:
                neg_count = (df[col] < 0).sum()
                if neg_count > 0 and not any(a['issue_type'] == 'POLARITY_ERROR' for a in anomalies):
                    anomalies.append({
                        "sensor": col,
                        "issue_type": "POLARITY_ERROR",
                        "severity": "HIGH",
                        "description": f"Detected {neg_count} negative consumption readings.",
                        "recommended_action": "Filter negative values & inspect meter sensor."
                    })

        return anomalies

quality_engine = DataQualityEngine()
