# Rural Microgrid Intelligence Platform — API Contract & Specification

This document defines the formal API contracts, request/response schemas, validation rules, and standardized error responses for the Rural Microgrid Intelligence Platform REST API.

All endpoints are served under the `/api` prefix. The interactive OpenAPI documentation is accessible at `/api/v1/openapi.json` and `/docs` when the backend is running.

---

## 1. Standard Error Envelope

All error responses (HTTP 4xx and 5xx) conform to a strict, predictable JSON envelope. A legacy `detail` field is retained for backward compatibility with standard FastAPI/Starlette clients.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters or payload structure.",
    "details": {
      "validation_errors": [
        {
          "loc": ["query", "limit"],
          "msg": "ensure this value is greater than or equal to 1",
          "type": "value_error.number.not_ge"
        }
      ]
    },
    "timestamp": "2026-10-01T15:30:00.000000"
  },
  "detail": "ensure this value is greater than or equal to 1"
}
```

### Error Codes

| Error Code | HTTP Status | Description |
| :--- | :--- | :--- |
| `INVALID_REQUEST` | 400 | The request payload is malformed or contains invalid values (e.g. invalid status string). |
| `RESOURCE_NOT_FOUND` | 404 | The requested entity (equipment, drilldown channel, etc.) does not exist in the registry. |
| `METHOD_NOT_ALLOWED` | 405 | The HTTP method is not supported for this path. |
| `VALIDATION_ERROR` | 422 | Query parameters, path variables, or request body failed Pydantic schema validation. |
| `INTERNAL_SERVER_ERROR` | 500 | An unhandled server-side error occurred during calculation. |

---

## 2. API Endpoints Catalog

| Method | Endpoint | Description | Query / Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Service health and active calculation engine inventory | None |
| `GET` | `/api/data/meter` | Recent raw 15-minute telemetry intervals | `limit` (int, 1..8640, default: 96) |
| `GET` | `/api/data/context` | Contextual telemetry (occupancy, tariffs, solar) | `limit` (int, 1..8640, default: 96) |
| `GET` | `/api/data/summary` | Dataset metadata, total rows, date boundary | None |
| `GET` | `/api/disaggregation` | Disaggregated load components, baseline, confidence | None |
| `GET` | `/api/disaggregation/drilldown/{load_id}` | 15-min timeseries evidence for a specific load | Path: `load_id` (str, e.g. `EQ_WP_01`) |
| `GET` | `/api/recommendations` | Active root-cause recommendations with evidence | None |
| `POST` | `/api/recommendations/{rec_id}/status` | Update recommendation status (`PENDING`/`APPLIED`/`REJECTED`) | Body: `StatusUpdateRequest` |
| `PATCH` | `/api/recommendations/{rec_id}/status` | Update recommendation status (alias) | Body: `StatusUpdateRequest` |
| `GET` | `/api/verification/summary` | Measured vs baseline M&V results and savings | None |
| `GET` | `/api/verification/timeseries` | Measured vs baseline timeseries comparison points | None |
| `GET` | `/api/equipment` | Complete equipment registry with load tiers | None |
| `GET` | `/api/equipment/{equipment_id}` | Single equipment record by ID | Path: `equipment_id` (str) |
| `GET` | `/api/quality/freshness` | Telemetry freshness status (`LIVE`, `STALE`, `MISSING`) | None |
| `GET` | `/api/quality/anomalies` | Detected sensor anomalies (stuck, negative, spike) | None |
| `POST` | `/api/quality/simulate-failure` | Inject simulated edge failures for testing | Body: `FailureSimulationRequest` |
| `GET` | `/api/i18n/{lang}` | Localization dictionary for UI (`en`, `hi`) | Path: `lang` (str) |

---

## 3. Endpoint Specifications

### 3.1. System Health

#### `GET /api/health`
Returns the operational status of all core calculation engines and registered services.

- **Request**: None
- **Response (200 OK)**:
```json
{
  "status": "HEALTHY",
  "engine_count": 6,
  "service_count": 14,
  "engines": {
    "data_generator": "Active (90-day 15-min telemetry)",
    "quality_engine": "Active (Freshness & edge failure simulator)",
    "disaggregation_engine": "Active (Scenario disaggregation)",
    "cause_engine": "Active (Actionable root-cause detection)",
    "recommendation_manager": "Active (Stateful recommendation tracker)",
    "verification_engine": "Active (Historical baseline vs. Measured experiment)"
  },
  "services": { ... },
  "timestamp": "2026-10-01T15:30:00.000000"
}
```

---

### 3.2. Telemetry Ingestion & Data

#### `GET /api/data/meter`
Retrieves sliced raw telemetry records from the microgrid data store.

- **Query Parameters**:
  - `limit` (integer, optional): Number of intervals to return. Range: `1` to `8640`. Default: `96` (24 hours).
- **Validation**: If `limit < 1` or `limit > 8640`, returns `422 Unprocessable Entity` with standard error envelope.
- **Response (200 OK)**: Array of `TelemetryRecord`:
```json
[
  {
    "timestamp": "2026-06-01T00:00:00",
    "total_kw": 18.52,
    "it_network_kw": 4.82,
    "lighting_kw": 7.15,
    "water_pump_kw": 0.0,
    "kitchen_kw": 0.5,
    "hvac_kw": 0.0,
    "lab_equipment_kw": 0.0,
    "occupancy": 5.0,
    "tariff_period": "OFF_PEAK",
    "tariff_rate": 4.5,
    "solar_gen_kw": 0.0,
    "net_grid_kw": 18.52,
    "day_index": 1
  }
]
```

#### `GET /api/data/context`
Retrieves environmental and tariff context data.

- **Query Parameters**:
  - `limit` (integer, optional): Number of records. Range: `1` to `8640`. Default: `96`.
- **Response (200 OK)**: Array of `ContextRecord` (`timestamp`, `occupancy`, `tariff_period`, `tariff_rate`, `solar_gen_kw`).

#### `GET /api/data/summary`
Retrieves record count and temporal boundaries.

- **Response (200 OK)**:
```json
{
  "total_records": 8640,
  "latest_record": { ... },
  "date_range": {
    "start": "2026-06-01T00:00:00",
    "end": "2026-08-29T23:45:00"
  }
}
```

---

### 3.3. Load Disaggregation

#### `GET /api/disaggregation`
Calculates empirical load breakdown across registered equipment channels and evaluation metrics.

- **Response (200 OK)**: `DisaggregationSummary`:
```json
{
  "timestamp": "2026-08-29T23:45:00",
  "total_kw": 22.74,
  "tiers": {
    "critical": { "kw": 5.15, "pct": 22.9 },
    "essential": { "kw": 12.91, "pct": 57.4 },
    "flexible": { "kw": 4.45, "pct": 19.8 }
  },
  "evaluation_metrics": {
    "mae_kw": 0.243,
    "rmse_kw": 0.304,
    "mape_pct": 1.17,
    "wape_pct": 0.98
  },
  "components": {
    "lighting": 8.25,
    "hvac": 0.35,
    "water_pump": 7.12,
    "lab_equipment": 0.54,
    "kitchen": 1.15,
    "it_network": 4.88
  },
  "percentage_breakdown": {
    "critical": 22.9,
    "essential": 57.4,
    "flexible": 19.8
  },
  "detailed_loads": [ ... ]
}
```

#### `GET /api/disaggregation/drilldown/{load_id}`
Returns time series alignment and evidence points for a specific equipment load.

- **Path Parameters**:
  - `load_id` (string, required): Registered equipment ID, e.g. `EQ_WP_01`, `EQ_HVAC_01`, `EQ_LAB_01`.
- **Error (404 Not Found)**: If `load_id` is unrecognized:
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Equipment with ID nonexistent_id not found.",
    "details": {},
    "timestamp": "2026-10-01T15:30:00.000000"
  },
  "detail": "Equipment with ID nonexistent_id not found."
}
```

---

### 3.4. Root-Cause Analysis & Recommendations

#### `GET /api/recommendations`
Returns actionable operational recommendations with 4-part explanations and evidence scores.

- **Response (200 OK)**: Array of `Recommendation`:
```json
[
  {
    "recommendation_id": "REC_WP_01",
    "equipment_id": "EQ_WP_01",
    "equipment_name": "Overhead Tank Water Pump",
    "load_tier": "Essential",
    "action_type": "COST_REDUCTION",
    "problem": "Water pump operates during high peak-tariff pricing (₹12.0/kWh).",
    "cause": "Water pumping is scheduled between 5 PM and 7 PM during the expensive evening electricity tariff window.",
    "evidence": {
      "metric": "Peak Tariff Pumping Load",
      "observed_value": 7.15,
      "expected_value": 0.0,
      "context": "Pump draws an average of 7.15 kW during the ₹12.0/kWh peak period."
    },
    "recommended_action": "Shift water pumping schedule to the off-peak tariff window (10 PM - 2 AM).",
    "estimated_energy_saving_kwh": 0.0,
    "estimated_cost_saving": 3217.5,
    "evidence_score": 95,
    "evidence_breakdown": {
      "telemetry_freshness": 30,
      "schedule_correlation": 30,
      "tariff_overlap": 20,
      "pattern_consistency": 15
    },
    "confidence": 0.95,
    "data_freshness": "LIVE",
    "priority": "HIGH",
    "status": "PENDING"
  }
]
```

#### `POST /api/recommendations/{recommendation_id}/status`
Updates recommendation lifecycle state. Also supported via `PATCH`.

- **Path Parameters**:
  - `recommendation_id` (string, required): ID of target recommendation.
- **Request Body**:
```json
{
  "status": "APPLIED"
}
```
- **Validation Rules**:
  - `status` MUST be one of: `PENDING`, `APPLIED`, `REJECTED`.
  - Empty body or missing status returns `400 Bad Request`.
  - Unrecognized status returns `400 Bad Request` with error message.
- **Response (200 OK)**:
```json
{
  "recommendation_id": "REC_WP_01",
  "status": "APPLIED",
  "success": true
}
```

---

### 3.5. Measurement & Verification (M&V)

#### `GET /api/verification/summary`
Calculates empirical pre- vs. post-intervention savings, separating energy reduction from load shifting.

- **Response (200 OK)**: `VerificationSummary`:
```json
{
  "status": "AVAILABLE",
  "baseline_period": "Days 1 - 30 (Suboptimal Schedule)",
  "intervention_period": "Days 31 - 60 (Transition Phase)",
  "verification_period": "Days 61 - 90 (Verified Operational Policy)",
  "baseline_daily_avg_kwh": 643.9,
  "target_daily_avg_kwh": 547.3,
  "measured_daily_avg_kwh": 561.9,
  "verified_reduction_kwh_day": 82.0,
  "verified_reduction_pct": 12.73,
  "cost_saving_daily": 1000.63,
  "cost_saving_total": 30018.9,
  "target_achievement_pct": 84.9,
  "error_analysis": {
    "target_reduction_kwh_day": 96.6,
    "verified_reduction_kwh_day": 82.0,
    "absolute_error_kwh": 14.59,
    "percentage_error": 15.1,
    "sensor_uncertainty": "Assumed prototype sensor uncertainty (±1.8%)",
    "lower_bound_kwh": 80.5,
    "upper_bound_kwh": 83.5
  },
  "interventions_applied": [ ... ],
  "reconciliation": {
    "main_meter_reduction_kwh_day": 82.0,
    "main_meter_reduction_pct": 12.73,
    "sum_submeter_reductions_kwh_day": 82.9,
    "background_unmetered_variance_kwh_day": -0.9,
    "main_meter_daily_cost_saving_inr": 1000.63,
    "sum_submeter_daily_cost_savings_inr": 1006.5,
    "background_cost_variance_inr": -5.87,
    "explanation": "Direct submetered interventions account for 82.9 kWh/day of energy reduction..."
  }
}
```

---

### 3.6. Equipment Registry

#### `GET /api/equipment`
Returns all registered campus microgrid loads and their operating tiers.

- **Response (200 OK)**: Array of `EquipmentItem`:
```json
[
  {
    "equipment_id": "EQ_IT_01",
    "equipment_name": "Server Rack",
    "load_tier": "Critical",
    "rated_power_kw": 3.5,
    "location": "IT Data Room",
    "schedule_description": "24/7 Continuous Operation",
    "is_essential": true,
    "channel_key": "it_network_kw"
  }
]
```

#### `GET /api/equipment/{equipment_id}`
Returns details for a single equipment entity.

- **Path Parameters**:
  - `equipment_id` (string, required): e.g., `EQ_WP_01`.
- **Error (404 Not Found)**: If ID is not in registry:
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Equipment with ID EQ_UNKNOWN not found.",
    "details": {},
    "timestamp": "2026-10-01T15:30:00.000000"
  },
  "detail": "Equipment with ID EQ_UNKNOWN not found."
}
```

---

### 3.7. Data Quality & Edge Failure Simulation

#### `GET /api/quality/freshness`
Evaluates telemetry freshness relative to the latest timestamp.

- **Response (200 OK)**: `FreshnessStatus`:
```json
{
  "status": "LIVE",
  "last_updated": "2026-10-01 15:30:00",
  "age_minutes": 2.5,
  "affected_sources": [],
  "recommendation_reliability": "HIGH",
  "warning_message": null
}
```

#### `GET /api/quality/anomalies`
Identifies abnormal sensor signals (negative values, stuck values, variance dropouts).

- **Response (200 OK)**: Array of `AnomalyItem`.

#### `POST /api/quality/simulate-failure`
Configures simulated edge failures for testing platform resilience.

- **Request Body**: `FailureSimulationRequest`:
```json
{
  "failure_type": "MISSING_DATA",
  "duration_intervals": 16,
  "affected_channel": "water_pump_kw"
}
```
Supported `failure_type` values: `MISSING_DATA`, `STALE_DATA`, `STUCK_SENSOR`, `NEGATIVE_READING`, `RESET`.

---

### 3.8. Internationalization (i18n)

#### `GET /api/i18n/{lang}`
Retrieves localized UI text dictionaries.

- **Path Parameters**:
  - `lang` (string): `en` (English) or `hi` (Hindi). Fallback is `en`.
- **Response (200 OK)**: Key-value dictionary of UI strings.
