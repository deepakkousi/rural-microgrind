/**
 * Rural Microgrid Intelligence Platform — API TypeScript Definitions
 * Mirrors the backend Pydantic schemas in backend/app/schemas/
 */

// --- Error Envelope ---
export interface ApiErrorDetail {
  loc?: (string | number)[];
  msg?: string;
  type?: string;
  [key: string]: unknown;
}

export interface ApiError {
  code: 'INVALID_REQUEST' | 'RESOURCE_NOT_FOUND' | 'METHOD_NOT_ALLOWED' | 'VALIDATION_ERROR' | 'INTERNAL_SERVER_ERROR' | string;
  message: string;
  details?: Record<string, unknown> | ApiErrorDetail[];
  timestamp: string;
}

export interface ErrorResponse {
  error: ApiError;
  detail?: string | ApiErrorDetail[];
}

// --- System Health ---
export interface HealthStatus {
  status: 'HEALTHY' | 'DEGRADED' | 'DOWN';
  engine_count: number;
  service_count: number;
  engines: Record<string, string>;
  services: Record<string, string>;
  timestamp: string;
}

// --- Telemetry & Data ---
export interface TelemetryRecord {
  timestamp: string;
  total_kw: number;
  lighting_kw: number;
  hvac_kw: number;
  water_pump_kw: number;
  lab_equipment_kw: number;
  kitchen_kw: number;
  it_network_kw: number;
  solar_gen_kw: number;
  occupancy: number;
  tariff_period: 'OFF_PEAK' | 'SHOULDER' | 'PEAK' | string;
  tariff_rate: number;
  net_grid_kw: number;
  day_index?: number;
}

export interface ContextRecord {
  timestamp: string;
  occupancy: number;
  tariff_period: 'OFF_PEAK' | 'SHOULDER' | 'PEAK' | string;
  tariff_rate: number;
  solar_gen_kw: number;
}

export interface DateRange {
  start: string;
  end: string;
}

export interface TelemetrySummary {
  total_records: number;
  latest_record: Record<string, unknown>;
  date_range: DateRange;
}

// --- Equipment Registry ---
export interface EquipmentItem {
  equipment_id: string;
  equipment_name: string;
  load_tier: 'Critical' | 'Essential' | 'Flexible' | string;
  rated_power_kw: number;
  location: string;
  schedule_description: string;
  is_essential: boolean;
  channel_key: string;
}

// --- Load Disaggregation ---
export interface TierValue {
  kw: number;
  pct: number;
}

export interface DisaggregationTiers {
  critical: TierValue;
  essential: TierValue;
  flexible: TierValue;
}

export interface DisaggregationEvaluation {
  mae_kw: number;
  rmse_kw: number;
  mape_pct: number;
  wape_pct: number;
}

export interface DetailedLoadItem {
  equipment_id: string;
  equipment_name: string;
  load_tier: string;
  rated_power_kw: number;
  current_power_kw: number;
  percentage: number;
  location: string;
  is_essential: boolean;
  schedule: string;
}

export interface DisaggregationSummary {
  timestamp: string;
  total_kw: number;
  tiers: DisaggregationTiers;
  evaluation_metrics: DisaggregationEvaluation;
  detailed_loads: DetailedLoadItem[];
  components?: Record<string, number>;
  percentage_breakdown?: Record<string, number>;
}

export interface DrilldownPoint {
  timestamp: string;
  actual_kw: number;
  expected_kw: number;
  occupancy_pct: number;
  tariff_rate: number;
  tariff_period: string;
}

export interface DrilldownResponse {
  equipment_id: string;
  equipment_name: string;
  load_tier: string;
  impact_type: string;
  location: string;
  rated_power_kw: number;
  is_essential: boolean;
  schedule: string;
  cause_explanation: string;
  recommended_action: string;
  timeseries: DrilldownPoint[];
}

// --- Cause Analysis & Recommendations ---
export interface CauseEvidence {
  metric: string;
  observed_value: number;
  expected_value: number;
  context: string;
}

export interface Recommendation {
  recommendation_id: string;
  equipment_id: string;
  equipment_name: string;
  load_tier: string;
  action_type: 'COST_REDUCTION' | 'ENERGY_REDUCTION' | string;
  problem: string;
  cause: string;
  evidence: CauseEvidence;
  recommended_action: string;
  estimated_energy_saving_kwh: number;
  estimated_cost_saving: number;
  evidence_score: number;
  evidence_breakdown: Record<string, number>;
  confidence: number;
  data_freshness: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW' | string;
  status: 'PENDING' | 'APPLIED' | 'REJECTED';
}

export interface StatusUpdateRequest {
  status: 'PENDING' | 'APPLIED' | 'REJECTED';
}

export interface StatusUpdateResponse {
  recommendation_id: string;
  status: string;
  success: boolean;
}

// --- Measurement & Verification ---
export interface ErrorAnalysisDetail {
  target_reduction_kwh_day: number;
  verified_reduction_kwh_day: number;
  absolute_error_kwh: number;
  percentage_error: number;
  sensor_uncertainty: string;
  lower_bound_kwh: number;
  upper_bound_kwh: number;
}

export interface InterventionItem {
  id: string;
  name: string;
  target_equipment: string;
  type: 'COST_REDUCTION' | 'ENERGY_REDUCTION' | string;
  action: string;
  baseline_kwh_day: number;
  verification_kwh_day: number;
  energy_saving_kwh_day: number;
  cost_saving_daily_inr: number;
  explanation: string;
  status: string;
}

export interface ReconciliationDetail {
  main_meter_reduction_kwh_day: number;
  main_meter_reduction_pct: number;
  sum_submeter_reductions_kwh_day: number;
  background_unmetered_variance_kwh_day: number;
  main_meter_daily_cost_saving_inr: number;
  sum_submeter_daily_cost_savings_inr: number;
  background_cost_variance_inr: number;
  explanation: string;
}

export interface VerificationSummary {
  status: 'AVAILABLE' | 'DATA_UNAVAILABLE' | string;
  message?: string;
  baseline_period?: string;
  intervention_period?: string;
  verification_period?: string;
  baseline_daily_avg_kwh?: number;
  target_daily_avg_kwh?: number;
  measured_daily_avg_kwh?: number;
  verified_reduction_kwh_day?: number;
  verified_reduction_pct?: number;
  cost_saving_daily?: number;
  cost_saving_total?: number;
  target_achievement_pct?: number;
  error_analysis?: ErrorAnalysisDetail;
  interventions_applied?: InterventionItem[];
  reconciliation?: ReconciliationDetail;
}

export interface VerificationTimeseriesPoint {
  day: number;
  phase: string;
  total_kwh: number;
  hvac_kwh: number;
  water_pump_kwh: number;
  lighting_kwh: number;
}

// --- Data Quality & Freshness ---
export interface FreshnessStatus {
  status: 'LIVE' | 'STALE' | 'VERY_STALE' | 'MISSING' | string;
  last_updated: string;
  age_minutes: number;
  affected_sources: string[];
  recommendation_reliability: 'HIGH' | 'MEDIUM' | 'LOW' | 'DISABLED' | string;
  warning_message?: string | null;
}

export interface AnomalyItem {
  sensor: string;
  issue_type: string;
  severity: string;
  description: string;
  recommended_action: string;
}

export interface FailureSimulationRequest {
  failure_type?: 'MISSING_DATA' | 'STALE_DATA' | 'STUCK_SENSOR' | 'NEGATIVE_READING' | 'RESET' | string;
  duration_intervals?: number;
  affected_channel?: string;
}

export interface FailureSimulationResponse {
  status: string;
  failure_type: string;
  affected_channel?: string;
}
