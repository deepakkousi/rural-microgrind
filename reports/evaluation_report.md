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

To validate data cleaning, zero-threshold guarded metrics, and tier-disaggregation mechanics on uncurated physical readings, the platform includes automated validation against a publicly available real-world residential energy dataset: the **Reference Energy Disaggregation Dataset (REDD)**, House 1 (Kolter & Johnson, MIT).

> [!IMPORTANT]
> **Strict Separation of Public vs. Synthetic Context**:
> The REDD dataset reflects real-world residential smart meter telemetry from a single-family home in Massachusetts, USA. It is strictly separated from the synthetic 90-day rural microgrid campus simulation. REDD data is used solely to demonstrate algorithmic correctness and pipeline robustness on uncurated non-synthetic telemetry; it is NOT claimed to represent rural microgrid load profiles.

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

### **7. Actionable Cause Detection & Authoritative Savings**

All recommendations derive savings directly from the single authoritative intervention engine calculation. The platform enforces:

$$\text{Monthly Cost Saving (₹/mo)} = \text{Daily Cost Saving (₹/d)} \times 30$$
$$\text{Monthly Energy Saving (kWh/mo)} = \text{Daily Energy Saving (kWh/d)} \times 30$$

Every recommendation provides a structured 4-part explanation with a 4-factor **Evidence Strength Score (0–100)** (a transparent heuristic score, not a statistical confidence interval):

1. **Water Pump Peak Tariff Shift (`REC_WP_01` — Cost Reduction / Load Shift)**:
   - **WHAT**: Water pump operates during high peak-tariff pricing (₹12.0/kWh).
   - **WHY**: Water pumping scheduled between 5 PM and 7 PM during peak pricing.
   - **RECOMMENDED ACTION**: Shift water pumping schedule to off-peak tariff window (10 PM - 2 AM).
   - **DAILY SAVING**: **0.0 kWh/day** energy reduction (Load Shift), **₹105.82 / day** cost saving.
   - **MONTHLY SAVING (30 Days)**: **0.0 kWh/month**, **₹3,174.60 / month** cost saving.
   - **EVIDENCE STRENGTH SCORE**: `95 / 100` (Freshness: +30, Schedule Overlap: +30, Tariff Overlap: +20, Pattern: +15).

2. **HVAC Low-Occupancy Waste (`REC_HVAC_01` — True Energy Reduction)**:
   - **WHAT**: Air conditioning drawing excessive power while rooms are unoccupied.
   - **WHY**: HVAC chillers maintain full cooling output (~18.8 kW) during low occupancy (< 25%).
   - **RECOMMENDED ACTION**: Set back thermostat by 2°C or idle chiller capacity when room occupancy < 25%.
   - **DAILY SAVING**: **73.7 kWh/day** energy reduction, **₹644.71 / day** cost saving.
   - **MONTHLY SAVING (30 Days)**: **2,211.0 kWh/month** energy reduction, **₹19,341.30 / month** cost saving.
   - **EVIDENCE STRENGTH SCORE**: `95 / 100` (Fresh Data: +30, Occupancy: +30, Schedule: +20, Pattern: +15).

3. **Heavy Workshop Machining Shift (`REC_LAB_01` — Cost Reduction / Load Shift)**:
   - **WHAT**: Heavy workshop machining practical classes run during Peak Tariff (₹12.0/kWh).
   - **WHY**: High-power practical machining sessions scheduled from 2 PM to 5 PM.
   - **RECOMMENDED ACTION**: Reschedule CNC practicals to morning shoulder tariff window (9 AM - 12 PM).
   - **DAILY SAVING**: **0.0 kWh/day** energy reduction (Load Shift), **₹179.49 / day** cost saving.
   - **MONTHLY SAVING (30 Days)**: **0.0 kWh/month**, **₹5,384.70 / month** cost saving.
   - **EVIDENCE STRENGTH SCORE**: `95 / 100` (Fresh Data: +30, Schedule Overlap: +30, Tariff Overlap: +20, Pattern: +15).

4. **Classroom Lighting Dimming (`REC_LT_01` — True Energy Reduction)**:
   - **WHAT**: Classroom and laboratory lighting energized during empty class periods.
   - **WHY**: Lights operate at ~4.2 kW during class breaks when student occupancy drops below 25%.
   - **RECOMMENDED ACTION**: Automate 50% lighting dimming via occupancy sensors when room occupancy < 25%.
   - **DAILY SAVING**: **9.2 kWh/day** energy reduction, **₹76.48 / day** cost saving.
   - **MONTHLY SAVING (30 Days)**: **276.0 kWh/month** energy reduction, **₹2,294.40 / month** cost saving.
   - **EVIDENCE STRENGTH SCORE**: `95 / 100` (Fresh Data: +30, Occupancy: +30, Schedule: +20, Pattern: +15).

---

### **8. Recommendation Engine Lifecycle**
- Tracks stateful status transitions (`PENDING` $\to$ `APPLIED` / `REJECTED`) persisted in memory across API calls.
- Both daily and monthly impacts are exposed directly via API endpoints (`GET /api/recommendations` and `GET /api/recommendations/causes`).

---

### **9. Role-Based Views**
Supports 4 distinct operational personas:
1. **Operations Staff**: Active alerts, current operational recommendations, real-time load status.
2. **Microgrid Manager**: Financial metrics, tariff distribution, baseline vs. verified energy savings ($ and ₹).
3. **Technician**: Sensor health, telemetry freshness, failure simulation controls, granular equipment logs.
4. **Resident / Non-Technical User**: Plain-language disaggregation summary, essential vs. flexible breakdown, simple recommendations.

---

### **10. Drill-Down Evidence**
Provides interactive 24-hour time series alignment overlaying Actual Load, Target Schedule, Occupancy %, and ToU Tariff Rates with non-technical root cause descriptions (`GET /api/disaggregation/drilldown/{load_id}`).

---

### **11. Data Quality & Edge Failure Analysis**
- **Freshness Categories**: `LIVE` (<15m), `STALE` (15m–2h), `VERY_STALE` (>2h), `MISSING`.
- **Tested Failure Cases**:
  1. *Missing Meter Data*: Triggers `MISSING` badge, disables recommendations, returns `DATA_UNAVAILABLE` status.
  2. *Stale Telemetry*: Downgrades freshness to `STALE`, updates age to 47 mins, reduces evidence strength score by 15 points.
  3. *Stuck Sensor*: Detects flatline transducer reading, logs `FLATLINE_STUCK` alert.
  4. *Negative Meter Reading*: Detects CT polarity reversal (-12.5 kW), logs `POLARITY_ERROR` alert.
  5. *Tariff Revision*: Dynamically recalculates cost savings under critical peak surcharge (₹18.5/kWh).

---

### **12. Explicit API Contracts & Schema Validation**
- Fully documented in `docs/API_CONTRACT.md` across all 22 registered REST endpoints.
- Validated via Pydantic models in `backend/app/schemas/` and TypeScript interfaces in `frontend/src/types/api.ts`.
- Standardized error envelope: `{ "error": { "code", "message", "details", "timestamp" }, "detail": "..." }`.
- Swagger docs at `/docs`, OpenAPI schemas at `/api/openapi.json` and `/api/v1/openapi.json`.

---

### **13. End-to-End Integration Testing**
6 multi-stage integration tests in `backend/tests/integration/test_e2e_pipeline.py` exercising:
1. Normal ingestion $\to$ verification pipeline flow
2. Missing telemetry suppression flow
3. Stale telemetry score degradation flow
4. Sensor flatline anomaly handling flow
5. Dynamic tariff sensitivity & energy separation
6. Recommendation lifecycle & drilldown flow

---

### **14. Verified Energy Reduction (Synthetic Prototype Experiment) & Error Analysis**
- **Baseline Period (Days 1–30)**: `643.9 kWh/day` average
- **Target Expectation**: `547.3 kWh/day` (15% reduction goal: Target Reduction `96.6 kWh/day`)
- **Measured Period (Days 61–90)**: `561.9 kWh/day`
- **Verified Feeder Energy Reduction**: `82.0 kWh/day` (`12.73%` energy reduction within synthetic experiment)
- **Target Achievement Ratio**: `84.9%` (`82.0 / 96.6 × 100`)
- **Verified Financial Saving**: `₹1,000.63 / day` (`₹30,018.90` total over 30-day verification period)
- **Target Error**: `14.6 kWh/day` (`15.11%` error against goal)
- **Sensor Uncertainty**: Assumed prototype sensor uncertainty (±1.8% based on typical smart meter transducer tolerance), lower bound: `80.5 kWh/day`, upper bound: `83.5 kWh/day`.

#### **Intervention-by-Intervention Empirical Breakdown**

| ID | Intervention Name | Type | Daily Energy | Daily Cost | Monthly Energy (30d) | Monthly Cost (30d) |
|---|---|---|---|---|---|---|
| `INT_01` | Water Pump Peak Tariff Shift | `COST_REDUCTION` (Load Shift) | **0.0 kWh/d** | **₹105.82 / d** | **0.0 kWh/mo** | **₹3,174.60 / mo** |
| `INT_02` | HVAC Low-Occupancy Setback | `ENERGY_REDUCTION` | **73.7 kWh/d** | **₹644.71 / d** | **2,211.0 kWh/mo** | **₹19,341.30 / mo** |
| `INT_03` | Workshop CNC Machine Shift | `COST_REDUCTION` (Load Shift) | **0.0 kWh/d** | **₹179.49 / d** | **0.0 kWh/mo** | **₹5,384.70 / mo** |
| `INT_04` | Classroom Lighting Dimming | `ENERGY_REDUCTION` | **9.2 kWh/d** | **₹76.48 / d** | **276.0 kWh/mo** | **₹2,294.40 / mo** |

#### **Mathematical Reconciliation: Feeder Total vs. Submeter Interventions**

| Channel Scope | Daily Energy Saving | Daily Cost Saving | Monthly Energy (30d) | Monthly Cost (30d) | Physical / Mathematical Reconciliation Note |
|---|---|---|---|---|---|
| **Direct Interventions (Submeter Sum)** | **82.9 kWh/day** | **₹1,006.50 / day** | **2,487.0 kWh/mo** | **₹30,195.00 / mo** | Direct sum of sub-metered targeted loads: HVAC Setback (`73.7 kWh/d`, `₹644.71/d`) + Classroom Lighting (`9.2 kWh/d`, `₹76.48/d`) + Water Pump Shift (`₹105.82/d`) + CNC Shift (`₹179.49/d`). |
| **Main Microgrid Feeder Meter** | **82.0 kWh/day** (`12.73%`) | **₹1,000.63 / day** | **2,460.0 kWh/mo** | **₹30,018.90 / mo** | Net measurement across all circuits + solar gen + unmetered background load (`643.9 kWh/d` baseline vs `561.9 kWh/d` verification). |
| **Reconciliation Variance** | **-0.9 kWh/day** | **-₹5.87 / day** | **-27.0 kWh/mo** | **-₹176.10 / mo** | Reconciled by non-intervened campus circuits (kitchen load drift `+0.31 kWh/d`, CNC standby `+0.18 kWh/d`, water pump standby `+0.04 kWh/d`, IT standby `+0.01 kWh/d`) and unmetered parasitic microgrid draw (`~0.33 kWh/d`). |

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
- **Actual Total Tests**: **69**
  - **Core Unit Tests**: 31
  - **Public Dataset Validation Tests**: 6
  - **API Contract & Parity Tests**: 26
  - **E2E Integration Tests**: 6
- **Passed**: **69** (`100%` pass rate)
- **Failed**: **0**

---

### **18. User Validation Protocol**
- Structured pilot protocol defined across 4 user personas and 5 core tasks; explicitly labeled "Real-user validation pending field trial".

---

### **19. Limitations & Future Work**
- *Limitations*: Synthetic disaggregation relies on component meter channels; full physical NILM hardware decomposition requires high-frequency sampling (1-10 kHz). Public dataset validation (REDD) demonstrates algorithm mathematical soundness on real data, but cannot replace real-world in-situ field telemetry from rural developing-region microgrids.
- *Future Work*: Integrate solar battery storage optimization (BESS), demand response automation, and live IoT MQTT gateway ingestion.
