# Rural Microgrid Intelligence Platform — API Contract & Specification

This document defines the formal API contracts, request/response schemas, validation rules, and standardized error responses for the Rural Microgrid Intelligence Platform REST API.

All endpoints are served under the `/api` prefix. The interactive Swagger documentation is accessible at `/docs` and OpenAPI JSON schemas are accessible at `/api/openapi.json` and `/api/v1/openapi.json`.

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
| `GET` | `/api/data/tariff` | Active Time-of-Use tariff structure, rates, and schedule windows | None |
| `GET` | `/api/disaggregation` | Disaggregated load components, baseline, confidence | None |
| `GET` | `/api/disaggregation/drilldown/{load_id}` | 15-min timeseries evidence for a specific load | Path: `load_id` (str, e.g. `EQ_WP_01`) |
| `GET` | `/api/recommendations` | Active root-cause recommendations with evidence | None |
| `GET` | `/api/recommendations/causes` | Detected root-cause diagnostics | None |
| `POST` | `/api/recommendations/{rec_id}/status` | Update recommendation status (`PENDING`/`APPLIED`/`REJECTED`) | Body: `StatusUpdateRequest` |
| `PATCH` | `/api/recommendations/{rec_id}/status` | Update recommendation status (alias) | Body: `StatusUpdateRequest` |
| `GET` | `/api/verification/summary` | Measured vs baseline M&V results and savings | None |
| `GET` | `/api/verification/timeseries` | Measured vs baseline timeseries comparison points | None |
| `GET` | `/api/verification/baseline` | Baseline load modeling and 15% reduction target summary | None |
| `GET` | `/api/verification/experiment` | 4 operational policy changes and verified savings | None |
| `GET` | `/api/equipment` | Complete equipment registry with load tiers | None |
| `GET` | `/api/equipment/{equipment_id}` | Single equipment record by ID | Path: `equipment_id` (str) |
| `GET` | `/api/quality/freshness` | Telemetry freshness status (`LIVE`, `STALE`, `VERY_STALE`, `MISSING`) | None |
| `GET` | `/api/quality/anomalies` | Detected sensor anomalies (stuck, negative, spike) | None |
| `POST` | `/api/quality/simulate-failure` | Inject simulated edge failures for testing | Body: `FailureSimulationRequest` |
| `GET` | `/api/user/roles` | Available user personas (`operations`, `manager`, `technician`, `resident`) | None |
| `GET` | `/api/i18n/{lang}` | Localization dictionary for UI (`en`, `hi`) | Path: `lang` (str) |

---

## 3. Authoritative Calculations: Energy vs. Cost Savings

The platform strictly separates **energy reduction (kWh)** from **cost reduction (load shifting)**. Every recommendation and intervention provides both **daily** and **monthly** (30-day period) metrics:

$$\text{Monthly Cost Saving (₹/mo)} = \text{Daily Cost Saving (₹/d)} \times 30$$
$$\text{Monthly Energy Saving (kWh/mo)} = \text{Daily Energy Saving (kWh/d)} \times 30$$

| ID | Load / Intervention | Type | Daily Energy | Daily Cost | Monthly Energy (30d) | Monthly Cost (30d) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `REC_WP_01` / `INT_01` | Water Pump Peak Tariff Shift | `COST_REDUCTION` (Load Shift) | **0.0 kWh/d** | **₹105.82 / d** | **0.0 kWh/mo** | **₹3,174.60 / mo** |
| `REC_HVAC_01` / `INT_02` | HVAC Low-Occupancy Setback | `ENERGY_REDUCTION` | **73.7 kWh/d** | **₹644.71 / d** | **2,211.0 kWh/mo** | **₹19,341.30 / mo** |
| `REC_LAB_01` / `INT_03` | Workshop CNC Machine Shift | `COST_REDUCTION` (Load Shift) | **0.0 kWh/d** | **₹179.49 / d** | **0.0 kWh/mo** | **₹5,384.70 / mo** |
| `REC_LT_01` / `INT_04` | Classroom Lighting Dimming | `ENERGY_REDUCTION` | **9.2 kWh/d** | **₹76.48 / d** | **276.0 kWh/mo** | **₹2,294.40 / mo** |
| **Sum of Submeter Interventions** | Targeted Circuits | — | **82.9 kWh/d** | **₹1,006.50 / d** | **2,487.0 kWh/mo** | **₹30,195.00 / mo** |
| **Main Feeder Net Measurement** | Net Microgrid Feeder | — | **82.0 kWh/d** | **₹1,000.63 / d** | **2,460.0 kWh/mo** | **₹30,018.90 / mo** |
| **Reconciliation Variance** | Non-Intervened & Parasitic | — | **-0.9 kWh/d** | **-₹5.87 / d** | **-27.0 kWh/mo** | **-₹176.10 / mo** |

---

## 4. Endpoint Specifications

### 4.1. System Health & User Roles

#### `GET /api/health`
Returns the operational status of all core calculation engines and registered services.

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

#### `GET /api/user/roles` (and `GET /api/user/role`)
Returns supported operational personas.

- **Response (200 OK)**:
```json
{
  "roles": [
    { "id": "operations", "name": "Operations Staff", "description": "Active alerts and operational recommendations" },
    { "id": "manager", "name": "Microgrid Manager", "description": "Financial metrics and verified savings" },
    { "id": "technician", "name": "Technician", "description": "Sensor health and failure simulation" },
    { "id": "resident", "name": "Resident / Non-Technical User", "description": "Plain-language disaggregation summary" }
  ]
}
```

---

### 4.2. Telemetry Ingestion & Tariffs

#### `GET /api/data/meter`
Retrieves sliced raw telemetry records from the microgrid data store.
- **Query Parameters**: `limit` (integer, 1..8640, default: 96).

#### `GET /api/data/tariff`
Retrieves active Time-of-Use tariff structure and schedule windows.

- **Response (200 OK)**:
```json
{
  "currency": "INR",
  "currency_symbol": "₹",
  "rates": {
    "OFF_PEAK": 4.5,
    "SHOULDER": 7.0,
    "PEAK": 12.0
  },
  "periods": [
    { "period": "OFF_PEAK", "rate": 4.5, "hours": "22:00 - 06:00", "description": "Late night / early morning off-peak window" },
    { "period": "SHOULDER", "rate": 7.0, "hours": "06:00 - 14:00, 19:00 - 22:00", "description": "Daytime standard operation window" },
    { "period": "PEAK", "rate": 12.0, "hours": "14:00 - 19:00", "description": "Afternoon peak demand surcharge window" }
  ]
}
```

---

### 4.3. Recommendations & Causes

#### `GET /api/recommendations` (and `GET /api/recommendations/causes`)
Returns actionable operational recommendations with 4-part explanations, daily and monthly savings, and Evidence Strength Scores.

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
      "context": "Pump draws an average of 7.15 kW during the ₹12.0/kWh peak period. Shifting this 2-hour window saves ₹105.82/day (₹3,174.60/month, 30 days) with 0.0 kWh/day energy reduction (pure load shifting)."
    },
    "recommended_action": "Shift water pumping schedule to the off-peak tariff window (10 PM - 2 AM).",
    "daily_energy_saving_kwh": 0.0,
    "daily_cost_saving": 105.82,
    "estimated_energy_saving_kwh": 0.0,
    "estimated_cost_saving": 3174.6,
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

---

### 4.4. Verification Engine & Baseline

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
    "absolute_error_kwh": 14.6,
    "percentage_error": 15.11,
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

#### `GET /api/verification/baseline`
Returns the 30-day baseline average and 15% scenario reduction target.

#### `GET /api/verification/experiment`
Returns the 4 operational policy changes and verified savings list.
