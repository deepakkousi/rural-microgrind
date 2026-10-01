# Comprehensive Evaluation Report — Rural Microgrid Intelligence Platform

This document presents the complete technical and experimental evaluation of the Rural Microgrid Intelligence Platform prototype, populated exclusively with empirical numbers derived from actual execution across both the synthetic rural microgrid experiment and public benchmark validation.

---

### **1. Problem Analysis**
Rural microgrids balance critical, essential, and flexible loads under variable Time-of-Use (ToU) tariffs and fluctuating solar generation. Traditional dashboards display aggregate energy consumption (kWh) without disaggregating equipment loads or explaining *why* energy usage spikes occur during peak tariff windows. The Rural Microgrid Intelligence Platform addresses this gap by converting smart meter telemetry into actionable load disaggregation, non-technical root-cause explanations, and empirical energy-reduction verification.

---

### **2. User & Workflow Map**
```
Raw Smart Meter Data (15-min) + Equipment Schedules + Occupancy + Tariff Rates
                                      │
                                      ▼
                        Data Quality & Freshness Engine
                                      │
                                      ▼
                      Scenario Load Disaggregation Engine
                                      │
                                      ▼
                       Actionable Cause Detection Engine
                                      │
                                      ▼
                       Contextual Recommendation Engine
                                      │
                                      ▼
                    Role-Based Dashboard (4 Personas)
                                      │
                                      ▼
                Baseline vs. Verified Energy Reduction Experiment
```

---

### **3. Architecture**
- **Backend Framework**: Python 3.13 + FastAPI + Pandas + Pydantic + Pytest
- **Frontend Framework**: React 18 + Vite + TailwindCSS + Recharts + Lucide-react + TypeScript API Types
- **Service & Engine Registration**: Health check reporting 6 core engines (`engine_count: 6`) and 14 registered services/components (`service_count: 14`).
- **Contract & Type Safety**: Centralized Pydantic schemas in `backend/app/schemas/`, TypeScript API interfaces in `frontend/src/types/api.ts`, and full API specification in `docs/API_CONTRACT.md`.

---

### **4. Synthetic Dataset Specification**
- **Time Window**: 90 continuous days at 15-minute intervals (8,640 records).
- **Telemetry Channels**: `timestamp`, `total_kw`, `lighting_kw`, `hvac_kw`, `water_pump_kw`, `lab_equipment_kw`, `kitchen_kw`, `it_network_kw`, `solar_gen_kw`, `occupancy`, `tariff_period`, `tariff_rate`, `net_grid_kw`, `day_index`.
- **Phases**: Baseline (Days 1–30), Intervention Transition (Days 31–60), Verified Operational Policy (Days 61–90).

---

### **5. Synthetic Disaggregation Performance**
- **Disaggregation Methodology**: Scenario-based synthetic load disaggregation using component meter channels, equipment schedules, and contextual signals.
- **Empirical Evaluation Metrics against Synthetic Benchmark**:
  - **Mean Absolute Error (MAE)**: `0.243 kW`
  - **Root Mean Square Error (RMSE)**: `0.304 kW`
  - **Mean Absolute Percentage Error (MAPE)**: `1.17%`
  - **Weighted Absolute Percentage Error (WAPE)**: `0.98%`
- **Load Tiers**:
  - Critical (Server Rack, Network): ~4.8 kW (16.2%)
  - Essential (Lighting, Water Pump, Kitchen): ~12.5 kW (42.2%)
  - Flexible (HVAC, CNC Machine, 3D Printers): ~12.4 kW (41.6%)

---

### **6. Public Dataset Validation (REDD House 1 Benchmark)**

To rigorously validate the data cleaning, mathematical metrics, and tier-disaggregation pipeline against uncurated real-world telemetry, the platform includes automated validation against the **Reference Energy Disaggregation Dataset (REDD)**, published by Kolter & Johnson (MIT).

> [!IMPORTANT]
> **Strict Separation of Public vs. Synthetic Context**:
> REDD House 1 data represents a single-family residential home in Massachusetts, USA. It is strictly separated from the synthetic 90-day rural microgrid campus simulation. REDD data is used solely to validate algorithmic correctness on real non-synthetic data; it is NOT claimed to represent rural microgrid load profiles.

#### **Public Dataset Characteristics**
- **Source**: REDD (Reference Energy Disaggregation Dataset), House 1.
- **Duration**: 7 continuous days (672 records at 15-minute resampling).
- **Mains Power**: Channel 1 + Channel 2 aggregate feeder power (kW).
- **Sub-metered Channels**: Refrigerator (ch5), Lighting (ch9), Outlets/Electronics (ch3), Lighting 2 (ch10).
- **Dataset Location**: `backend/data/public/redd_house1_sample.csv` (Metadata in `backend/data/public/README.md`).

#### **Tier Mapping for Benchmark Validation**
| Microgrid Tier | REDD Channel | Appliance Description | Benchmark Operational Role |
| :--- | :--- | :--- | :--- |
| **Critical** | `refrigerator_kw` (ch5) | Domestic Refrigerator | 24/7 continuous baseline load |
| **Essential** | `lighting_kw` + `lighting2_kw` (ch9, ch10) | Kitchen & Corridor Lighting | Essential task and evening illumination |
| **Flexible** | `electronics_kw` (ch3) | Living Room Outlets / Electronics | Discretionary daytime load |

#### **Empirical Validation Results on Real REDD Telemetry**
- **Mean Absolute Error (MAE)**: `0.0801 kW`
- **Root Mean Square Error (RMSE)**: `0.0856 kW`
- **Mean Absolute Percentage Error (MAPE)**: `8.59%` (zero-threshold guarded)
- **Weighted Absolute Percentage Error (WAPE)**: `8.36%`
- **Energy Explained Ratio (EER)**: `91.64%`
- **Unmetered Residual**: `8.36%` (unmonitored residential circuits: HVAC, washer/dryer, oven)

#### **Dataset Limitations & Boundary Conditions**
1. *Geographic & Climatic*: High-income suburban US residence with 120V split-phase mains, differing fundamentally from 3-phase rural microgrids.
2. *Equipment Differences*: Residential appliances do not feature agricultural water pumps, academic chillers, or heavy machine-tool equipment.
3. *Absence of Generation*: REDD House 1 does not include distributed solar PV or battery storage.

---

### **7. Actionable Cause Detection**
Detects primary operational causes with transparent Evidence Strength Scores (0–100):
1. **Water Pump Peak Tariff Shift** (COST REDUCTION): Pump running 5 PM–7 PM during ₹12.0/kWh peak tariff.
2. **HVAC Low-Occupancy Waste** (ENERGY REDUCTION): HVAC running at ~21.4 kW while room occupancy < 25%.
3. **Heavy Workshop Machining Shift** (COST REDUCTION): CNC machine operating during ₹12.0/kWh peak tariff.
4. **Classroom Lighting Dimming** (ENERGY REDUCTION): Lighting active during low classroom utilization.

---

### **8. Recommendation Engine Performance**
- Generates structured recommendations with Evidence Strength Scores (0–100), priority tags, and stateful status tracking (`PENDING`, `APPLIED`, `REJECTED`).
- Complete explainability structure for every recommendation:
  - **WHAT**: Concrete description of the detected inefficiency.
  - **WHY**: Equipment scheduling and ToU tariff overlap cause.
  - **ACTION**: Recommended operational policy adjustment.
  - **IMPACT**: Explicit separation of expected kWh/day energy reduction from ₹/day cost reduction.

---

### **9. Role-Based Views**
Supports 4 distinct user roles:
1. **Operations Staff**: Active alerts, current operational recommendations, real-time load status.
2. **Microgrid Manager**: Financial metrics, tariff distribution, baseline vs. verified energy savings ($ and ₹).
3. **Technician**: Sensor health, telemetry freshness, failure simulation controls, granular equipment logs.
4. **Resident / Non-Technical User**: Plain-language disaggregation summary, essential vs. flexible breakdown, simple recommendations.

---

### **10. Drill-Down Evidence**
Provides interactive 24-hour time series alignment overlaying Actual Load, Target Schedule, Occupancy %, and ToU Tariff Rates with non-technical root cause descriptions.

---

### **11. Data Quality & Edge Failure Analysis**
- **Freshness Categories**: `LIVE` (<15m), `STALE` (15m–2h), `VERY_STALE` (>2h), `MISSING`.
- **Tested Failure Cases**:
  1. *Missing Meter Data*: Triggers `MISSING` badge, disables recommendations, returns `DATA_UNAVAILABLE` status.
  2. *Stale Telemetry*: Downgrades freshness to `STALE`, updates age to 47 mins, reduces evidence strength score.
  3. *Stuck Sensor*: Detects flatline transducer reading, logs `FLATLINE_STUCK` alert.
  4. *Negative Meter Reading*: Detects CT polarity reversal (-12.5 kW), logs `POLARITY_ERROR` alert.
  5. *Tariff Revision*: Dynamically recalculates cost savings under critical peak surcharge (₹18.5/kWh).

---

### **12. Explicit API Contracts & Schema Validation**
- **Contract Specification**: Fully documented in `docs/API_CONTRACT.md` across 17 endpoints.
- **Pydantic Validation**: All incoming requests and outgoing payloads validated via typed models in `backend/app/schemas/`.
- **Standardized Error Envelope**:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR" | "RESOURCE_NOT_FOUND" | "INVALID_REQUEST" | "INTERNAL_SERVER_ERROR",
      "message": "Human-readable description",
      "details": { ... },
      "timestamp": "ISO-8601"
    },
    "detail": "Backward-compatible string or list"
  }
  ```
- **Frontend TypeScript Synchronization**: Complete TypeScript interfaces in `frontend/src/types/api.ts` mirroring backend schemas.
- **Automated Contract Tests**: 19 automated tests in `backend/tests/test_api_contracts.py` covering valid responses, out-of-range bounds, 404 resource lookups, and 400 bad requests.

---

### **13. End-to-End Integration Testing**
The test suite includes 6 multi-stage integration tests in `backend/tests/integration/test_e2e_pipeline.py`:
1. `test_e2e_normal_pipeline`: End-to-end telemetry ingestion $\to$ freshness validation $\to$ load disaggregation $\to$ cause detection $\to$ recommendation generation $\to$ verification calculation $\to$ mathematical reconciliation.
2. `test_e2e_missing_telemetry_flow`: Validates safe behavior during data dropouts; verifies recommendations are suppressed and verification returns `DATA_UNAVAILABLE`.
3. `test_e2e_stale_telemetry_flow`: Validates graceful degradation under network latency; confirms evidence strength scores drop by 15 points.
4. `test_e2e_sensor_anomaly_handling`: Injects transducer flatline (`STUCK_SENSOR`) and verifies anomaly detection flags the channel without crashing the platform.
5. `test_e2e_tariff_dynamics_and_separation`: Verifies mathematical separation of energy savings (kWh) from financial savings (₹) under tariff modifications.
6. `test_e2e_recommendation_lifecycle_and_drilldown`: Exercises recommendation inspection $\to$ drilldown evidence extraction $\to$ status application (`APPLIED`) $\to$ state persistence across calls.

---

### **14. Verified Energy Reduction (Synthetic Prototype Experiment) & Error Analysis**
- **Baseline Period (Days 1–30)**: `643.9 kWh/day` average
- **Target Expectation**: `547.3 kWh/day` (Target Reduction: `96.6 kWh/day`)
- **Measured Period (Days 61–90)**: `561.9 kWh/day`
- **Verified Feeder Energy Reduction**: `82.0 kWh/day` (`12.73%` energy reduction within synthetic experiment)
- **Target Achievement Ratio**: `84.9%`
- **Verified Financial Saving**: `₹1,000.63 / day` (`₹30,018.90` total over 30-day verification period)
- **Target Error**: `14.6 kWh/day` (`15.11%` error against goal)
- **Sensor Uncertainty**: Assumed prototype sensor uncertainty (±1.8% based on typical smart meter transducer tolerance), lower bound: `80.5 kWh/day`, upper bound: `83.5 kWh/day`.

#### **Intervention-by-Intervention Empirical Breakdown**

| ID | Intervention Name | Type | Baseline (kWh/d) | Verified (kWh/d) | Energy Saved | Cost Saved |
|---|---|---|---|---|---|---|
| `INT_01` | Water Pump Peak Tariff Shift | `COST_REDUCTION` | 16.5 | 16.5 | **0.0 kWh/d** | **₹105.82 / d** |
| `INT_02` | HVAC Low-Occupancy Setback | `ENERGY_REDUCTION` | 220.5 | 146.8 | **73.7 kWh/d** | **₹644.71 / d** |
| `INT_03` | Workshop CNC Machine Shift | `COST_REDUCTION` | 47.9 | 48.1 | **0.0 kWh/d** | **₹179.49 / d** |
| `INT_04` | Classroom Lighting Dimming | `ENERGY_REDUCTION` | 153.9 | 144.7 | **9.2 kWh/d** | **₹76.48 / d** |

#### **Mathematical Reconciliation: Feeder Total vs. Submeter Interventions**

| Channel Scope | Daily Energy Saving | Daily Cost Saving | Physical / Mathematical Reconciliation Note |
|---|---|---|---|
| **Direct Interventions (Submeter Sum)** | **82.9 kWh/day** | **₹1,006.50 / day** | Direct sum of sub-metered targeted loads: HVAC Setback (`73.7 kWh/d`, `₹644.71/d`) + Classroom Lighting (`9.2 kWh/d`, `₹76.48/d`) + Water Pump Shift (`₹105.82/d`) + CNC Shift (`₹179.49/d`). |
| **Main Microgrid Feeder Meter** | **82.0 kWh/day** (`12.73%`) | **₹1,000.63 / day** | Net measurement across all circuits + solar gen + unmetered background load (`643.9 kWh/d` baseline vs `561.9 kWh/d` verification). |
| **Reconciliation Variance** | **-0.9 kWh/day** | **-₹5.87 / day** | Reconciled by non-intervened campus circuits (kitchen load drift `+0.31 kWh/d`, CNC standby `+0.18 kWh/d`, water pump standby `+0.04 kWh/d`, IT standby `+0.01 kWh/d`) and unmetered parasitic microgrid draw (`~0.33 kWh/d`). |

$$\text{Verified Reduction \%} = \frac{\text{Baseline} - \text{Measured}}{\text{Baseline}} \times 100 = \frac{643.9 - 561.9}{643.9} \times 100 = \frac{82.0}{643.9} \times 100 = 12.7349\% \approx 12.73\%$$

---

### **15. Accessibility Implementation**
- Accessibility features implemented with WCAG 2.1 AA-oriented practices: Keyboard focus indicators (`focus-visible:ring-2`), contrast ratio > 4.5:1, screen reader ARIA labels, non-color-only indicators; formal compliance audit not performed.

---

### **16. Language Support**
- Full English (EN) and Hindi (HI) localization across UI and backend API responses.

---

### **17. Automated Testing Results**
- **Executed Test Suite**: Pytest
- **Actual Total Tests**: **62**
  - **Core Unit Tests**: 31
  - **Public Dataset Validation Tests**: 6
  - **API Contract Tests**: 19
  - **E2E Integration Tests**: 6
- **Passed**: **62** (`100%` pass rate)
- **Failed**: **0**

---

### **18. User Validation Protocol**
- Structured pilot protocol defined across 4 user personas and 5 core tasks; explicitly labeled "Real-user validation pending field trial".

---

### **19. Limitations & Future Work**
- *Limitations*: Synthetic disaggregation relies on component meter channels; full physical NILM hardware decomposition requires high-frequency sampling (1-10 kHz). Public dataset validation (REDD) demonstrates algorithm mathematical soundness on real data, but cannot replace real-world in-situ field telemetry from rural developing-region microgrids.
- *Future Work*: Integrate solar battery storage optimization (BESS), demand response automation, and live IoT MQTT gateway ingestion.
