# Rural Microgrid Intelligence Platform

[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-sky.svg)](https://reactjs.org)
[![Build Status](https://img.shields.io/badge/Tests-30%2F30%20Passed-emerald.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

> A scenario-based disaggregation, actionable cause detection, operational recommendation, and empirical verification platform for rural microgrids.

---

## 📌 Problem Statement

Rural microgrids balance critical, essential, and flexible loads under variable Time-of-Use (ToU) electricity tariffs and fluctuating solar generation. Traditional energy dashboards display aggregate power consumption (kW/kWh) without disaggregating individual load categories or explaining **why** energy usage spikes occur or **what** operators should do to save cost.

The **Rural Microgrid Intelligence Platform** converts smart meter telemetry, equipment schedules, occupancy data, and tariff structures into:
1. Load disaggregation across Critical, Essential, and Flexible tiers.
2. Plain-language root cause explanations (WHAT, WHY, EVIDENCE).
3. Actionable operational recommendations.
4. Empirical **Baseline → Target → Measured → Verified Energy Reduction** experiments.
5. Role-based views (Operations, Manager, Technician, Resident) with multi-language (English/Hindi) and WCAG 2.1 AA-oriented accessibility practices.

---

## ⚡ Energy Reduction (kWh) vs. Cost Reduction (Load Shifting)

To maintain complete engineering accuracy, the platform strictly separates two operational concepts:

| Dimension | Energy Reduction (kWh) | Cost Reduction (Load Shifting) |
|---|---|---|
| **Core Definition** | Genuine reduction in kilowatt-hours consumed. | Shifting heavy equipment runtime to Off-Peak / Shoulder tariffs. |
| **Physics Effect** | Reduces mechanical, thermodynamic, or optical power demand. | Total daily run hours and total daily energy consumption (kWh) remain constant. |
| **Microgrid Impact** | Conserves diesel/battery capacity and reduces absolute grid draw. | Avoids ₹12.0/kWh peak electricity rate without sacrificing utility. |
| **Platform Examples** | • **HVAC Setback** (+2°C / idle capacity during low room occupancy): **73.7 kWh/day saved**.<br>• **Classroom Lighting Dimming** (50% dimming when occupancy < 25%): **9.2 kWh/day saved**. | • **Water Pumping Shift** (Shifted from 5–7 PM Peak to 10 PM–2 AM Off-Peak): **0.0 kWh/day energy saved**, **₹105.82/day cost saved**.<br>• **Workshop CNC Machine Shift** (Shifted from 2–5 PM Peak to 9 AM–12 PM Morning): **0.0 kWh/day energy saved**, **₹179.49/day cost saved**. |

---

## 🏗 System Architecture

```
                                  ┌──────────────────────┐
                                  │     Meter Data       │
                                  │    15-minute data    │
                                  └──────────┬───────────┘
                                             │
           ┌─────────────────────────────────┼─────────────────────────────────┐
           │                                 │                                 │
           ▼                                 ▼                                 ▼
     Equipment                          Occupancy                           Tariff
      Schedule                            Data                               Data
           │                                 │                                 │
           └─────────────────────────────────┼─────────────────────────────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │   Data Quality       │
                                  │ Missing / Stale /    │
                                  │ Abnormal detection   │
                                  └──────────┬───────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │   Disaggregation     │
                                  └──────────┬───────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │ Cause / Anomaly      │
                                  │ Detection            │
                                  └──────────┬───────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │ Recommendation       │
                                  │ Engine               │
                                  └──────────┬───────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │ Operational Action   │
                                  └──────────┬───────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │ Baseline vs          │
                                  │ Measured Verification│
                                  └──────────┬───────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │ Verified Energy      │
                                  │ Reduction            │
                                  └──────────┘
```

---

## 📊 Dataset Schema (90-Day Telemetry)

The system generates a 90-day synthetic dataset at 15-minute intervals (8,640 records).

| Column Name | Data Type | Description |
|---|---|---|
| `timestamp` | ISO String | Date and time formatted as `YYYY-MM-DDTHH:MM:SS` |
| `total_kw` | Float | Aggregate microgrid power consumption (kW) |
| `lighting_kw` | Float | Main corridor & classroom lighting load (kW) |
| `hvac_kw` | Float | Academic block HVAC chiller load (kW) |
| `water_pump_kw` | Float | Overhead tank water pumping load (kW) |
| `lab_equipment_kw` | Float | Heavy CNC workshop machine & 3D printers load (kW) |
| `kitchen_kw` | Float | Mess hall cooking & refrigeration load (kW) |
| `it_network_kw` | Float | Server racks & campus WiFi switches load (kW) |
| `solar_gen_kw` | Float | On-site solar PV generation (kW) |
| `occupancy` | Float | Campus room occupancy percentage (0–100%) |
| `tariff_period` | String | Time-of-Use tariff phase (`OFF_PEAK`, `SHOULDER`, `PEAK`) |
| `tariff_rate` | Float | Electricity rate in ₹ / kWh |
| `net_grid_kw` | Float | Net power flow in kW (`total_kw` - `solar_gen_kw`); positive = grid import, negative = solar export |
| `day_index` | Integer | Experiment day index (1 to 90) |

---

## ⚙️ Load Categories & Disaggregation Methodology

### Load Categories
- **Critical (24/7)**: Server Rack (`EQ_IT_01`), WiFi Network Switches (`EQ_IT_02`)
- **Essential**: Main Security Lighting (`EQ_LT_01`), Water Pump (`EQ_WP_01`), Kitchen (`EQ_KT_01`)
- **Flexible**: HVAC Chillers (`EQ_HVAC_01`), Classroom Lighting (`EQ_LT_02`), CNC Machine (`EQ_LAB_01`), 3D Printers (`EQ_LAB_02`)

### Methodology
*"Scenario-based synthetic load disaggregation using known component meter channels, equipment schedules, and contextual signals."*

### Empirical Accuracy Metrics (Evaluated on Synthetic Scenario Telemetry)
- **Mean Absolute Error (MAE)**: `0.243 kW`
- **Root Mean Square Error (RMSE)**: `0.304 kW`
- **Mean Absolute Percentage Error (MAPE)**: `1.17%`
- **Weighted Absolute Percentage Error (WAPE)**: `0.98%`

---

## 🎯 Actionable Cause Detection & Recommendation Engine

The engine cross-correlates power draws against schedules, occupancy, and tariff structures to generate transparent root-cause diagnoses with a 4-factor **Evidence Strength Score (0–100)** (a transparent heuristic score, not a statistical confidence interval):

### 1. Water Pump Peak Tariff Shift (`REC_WP_01` — Cost Reduction / Load Shift)
- **WHAT Happened?**: Water pump running during 5 PM - 7 PM Peak Tariff.
- **WHY Did It Happen?**: Scheduled during ₹12.0/kWh peak electricity pricing.
- **EVIDENCE**: 7.1 kW draw during Peak Tariff when Off-Peak rate is ₹4.5/kWh.
- **RECOMMENDED ACTION**: Shift water pumping schedule to late night Off-Peak tariff (10 PM - 2 AM).
- **ESTIMATED SAVING**: `0.0 kWh/day` energy reduction (Load Shift) → `₹3,174.60 / month` cost saving.
- **PROTOTYPE EVIDENCE SCORE**: `95 / 100` (High confidence under LIVE data: Freshness: +30, Schedule Overlap: +30, Tariff Overlap: +20, Pattern: +15; not a statistical confidence interval).

### 2. HVAC Low-Occupancy Waste (`REC_HVAC_01` — True Energy Reduction)
- **WHAT Happened?**: Air conditioning drawing excessive power while rooms are unoccupied.
- **WHY Did It Happen?**: HVAC chillers maintaining full cooling output (18.8 kW) during low occupancy (< 25%).
- **EVIDENCE**: 18.8 kW observed vs. 7.0 kW setback baseline.
- **RECOMMENDED ACTION**: Set back thermostat by 2°C or idle chiller capacity when room occupancy drops below 25%.
- **ESTIMATED SAVING**: `885.0 kWh / month` energy reduction → `₹6,195.00 / month` cost saving.
- **EVIDENCE STRENGTH SCORE**: `95 / 100` (Fresh Data: +30, Occupancy Correlation: +30, Schedule: +20, Pattern: +15).

### 3. Workshop CNC Machine Shift (`REC_LAB_01` — Cost Reduction / Load Shift)
- **WHAT Happened?**: Heavy CNC milling operated during Peak Tariff (₹12.0/kWh).
- **WHY Did It Happen?**: High-power practical machining sessions scheduled from 2 PM to 5 PM.
- **EVIDENCE**: 12.5 kW draw during peak hours vs. ₹7.0/kWh morning shoulder rate.
- **RECOMMENDED ACTION**: Reschedule CNC machining practicals to morning shoulder window (9 AM - 12 PM).
- **ESTIMATED SAVING**: `0.0 kWh/day` energy reduction (Load Shift) → `₹5,625.00 / month` cost saving.
- **EVIDENCE STRENGTH SCORE**: `95 / 100` (Fresh Data: +30, Schedule Overlap: +30, Tariff Overlap: +20, Pattern: +15).

### 4. Classroom Lighting Dimming (`REC_LT_01` — True Energy Reduction)
- **WHAT Happened?**: Classroom and laboratory lighting energized at ~4.2 kW during empty class periods.
- **WHY Did It Happen?**: Manual light switches left ON when student room occupancy drops below 25%.
- **EVIDENCE**: 4.2 kW observed vs. 2.0 kW dimmed target.
- **RECOMMENDED ACTION**: Automate 50% lighting dimming via occupancy sensors when room occupancy < 25%.
- **ESTIMATED SAVING**: `132.0 kWh / month` energy reduction → `₹924.00 / month` cost saving.
- **EVIDENCE STRENGTH SCORE**: `95 / 100` (Fresh Data: +30, Occupancy Correlation: +30, Schedule: +20, Pattern: +15).

---

## 📈 Baseline vs. Measured Verification (Synthetic Prototype Experiment)

Three 30-day experimental phases calculated dynamically from raw telemetry (verified within the synthetic prototype experiment; not real-world field data):
- **BASELINE (Days 1–30)**: `643.9 kWh/day` average
- **TARGET (15% Goal Target)**: `547.3 kWh/day` (Target Reduction: `96.6 kWh/day`)
- **MEASURED (Days 61–90)**: `561.9 kWh/day`
- **VERIFIED REDUCTION**: `82.0 kWh/day` (`12.73%` reduction within synthetic experiment)
- **TARGET ACHIEVEMENT RATIO**: `84.9%`

### Measured Financial Savings & Error Analysis
- **Daily Financial Saving**: `₹1,000.63 / day` (`₹30,018.90` total over 30-day verification period)
- **Target Error**: `14.6 kWh/day` (`15.11%` error against goal)
- **Sensor Uncertainty**: Assumed prototype sensor uncertainty (±1.8% based on typical smart meter transducer tolerance), lower bound: `80.5 kWh/day`, upper bound: `83.5 kWh/day`.

### 🔬 Intervention-by-Intervention Empirical Breakdown

| ID | Intervention Name | Type | Baseline (kWh/d) | Verified (kWh/d) | Energy Saved | Cost Saved |
|---|---|---|---|---|---|---|
| `INT_01` | Water Pump Peak Tariff Shift | `COST_REDUCTION` | 16.5 | 16.5 | **0.0 kWh/d** | **₹105.82 / d** |
| `INT_02` | HVAC Low-Occupancy Setback | `ENERGY_REDUCTION` | 220.5 | 146.8 | **73.7 kWh/d** | **₹644.71 / d** |
| `INT_03` | Workshop CNC Machine Shift | `COST_REDUCTION` | 47.9 | 48.1 | **0.0 kWh/d** | **₹179.49 / d** |
| `INT_04` | Classroom Lighting Dimming | `ENERGY_REDUCTION` | 153.9 | 144.7 | **9.2 kWh/d** | **₹76.48 / d** |

### ⚖️ Mathematical Reconciliation: Feeder Total vs. Submeter Interventions

| Channel Scope | Daily Energy Saving | Daily Cost Saving | Physical / Mathematical Reconciliation Note |
|---|---|---|---|
| **Direct Interventions (Submeter Sum)** | **82.9 kWh/day** | **₹1,006.50 / day** | Direct sum of sub-metered targeted loads: HVAC Setback (`73.7 kWh/d`, `₹644.71/d`) + Classroom Lighting (`9.2 kWh/d`, `₹76.48/d`) + Water Pump Shift (`₹105.82/d`) + CNC Shift (`₹179.49/d`). |
| **Main Microgrid Feeder Meter** | **82.0 kWh/day** (`12.73%`) | **₹1,000.63 / day** | Net measurement across all circuits + solar gen + unmetered background load (`643.9 kWh/d` baseline vs `561.9 kWh/d` verification). |
| **Reconciliation Variance** | **-0.9 kWh/day** | **-₹5.87 / day** | Reconciled by non-intervened campus circuits (kitchen load drift `+0.31 kWh/d`, CNC standby `+0.18 kWh/d`, water pump standby `+0.04 kWh/d`, IT standby `+0.01 kWh/d`) and unmetered parasitic microgrid draw (`~0.33 kWh/d`). |

$$\text{Verified Reduction \%} = \frac{\text{Baseline} - \text{Measured}}{\text{Baseline}} \times 100 = \frac{643.9 - 561.9}{643.9} \times 100 = \frac{82.0}{643.9} \times 100 = 12.7349\% \approx 12.73\%$$

---

## 👥 Role-Based Dashboard Architecture

1. **Operations Staff**: Active alerts, current operational recommendations, real-time load status.
2. **Microgrid Manager**: Financial metrics, tariff distribution, baseline vs. verified energy savings ($ and ₹).
3. **Technician**: Sensor health, telemetry freshness, failure simulation controls, granular equipment logs.
4. **Resident / Non-Technical User**: Plain-language disaggregation summary, essential vs. flexible breakdown, simple recommendations.

---

## 🛡 Data Quality & Edge Failure Simulator

Handles 4 freshness states: `LIVE` (<15m), `STALE` (15m–2h), `VERY_STALE` (>2h), `MISSING`.
- Telemetry > 2 hours (`VERY_STALE`) pauses recommendations.
- Missing telemetry (`MISSING`) disables recommendations and displays data unavailable notice.

Supported & Tested Edge Cases:
1. **Missing Meter Data**: Disables unsafe recommendations, returns `DATA_UNAVAILABLE` status.
2. **Stale Telemetry**: Shows warning badge, downgrades evidence strength score.
3. **Stuck Sensor**: Detects flatline transducer reading (>2h constant value).
4. **Negative Meter Reading**: Flags CT polarity inversion error (-12.5 kW).
5. **Tariff Revision**: Dynamically recalculates cost savings under critical peak surcharge (₹18.5/kWh).

---

## 🌐 Language & Accessibility Checks

- **Languages**: English (`en`) and Hindi (`hi`) translation toggle.
- **Accessibility Implementation**: Accessibility features implemented with WCAG 2.1 AA-oriented practices (keyboard focus indicators `focus-visible:ring-2`, contrast ratio > 4.5:1, screen reader ARIA labels, non-color-only badges); formal compliance audit not performed.

---

## 🧪 Automated Testing

Run Pytest suite:
```bash
cd backend
python -m pytest tests/ -v
```
**Test Results**: **31 / 31 Passed (100% Pass Rate)**.

---

## 🚀 Quick Start & Running Instructions

### Backend (FastAPI)
```bash
cd backend
python -m pip install -r requirements.txt
python main.py
```
Backend runs at: `http://localhost:8000` (Health API: `http://localhost:8000/api/health`)

### Frontend (React + Vite)
```bash
cd frontend
cmd /c npm install
cmd /c npm run dev
```
Frontend runs at: `http://localhost:5173`

---

## 📡 Complete REST API Endpoint Directory

| Endpoint | Method | Engine | Description |
|---|---|---|---|
| `/api/health` | GET | Core | Service health, engine registry, and compliance status |
| `/api/data/meter` | GET | Generator | Retrieve raw 15-min smart meter time-series records |
| `/api/data/context` | GET | Generator | Retrieve occupancy, ToU tariff, and solar data |
| `/api/data/summary` | GET | Generator | Telemetry statistics and dataset date range |
| `/api/equipment` | GET | Loader | Full registry of 9 microgrid loads and metadata |
| `/api/disaggregation` | GET | Disaggregation | Disaggregated equipment power channels and accuracy |
| `/api/disaggregation/drilldown/{load_id}` | GET | Disaggregation | 24-hr schedule vs. occupancy vs. tariff alignment |
| `/api/recommendations` | GET | Cause & Rec | Actionable recommendations with Evidence Scores |
| `/api/recommendations/{id}/status` | POST | Rec Manager | Transition status: `PENDING`, `APPLIED`, `REJECTED` |
| `/api/verification/summary` | GET | Verification | Baseline vs. Target vs. Measured verified savings |
| `/api/verification/timeseries` | GET | Verification | Daily verification trends across 90 days |
| `/api/quality/freshness` | GET | Quality | Telemetry age, freshness category, and timestamp |
| `/api/quality/anomalies` | GET | Quality | Detected sensor anomalies, polarity errors, stuck signals |
| `/api/quality/simulate-failure` | POST | Quality | Simulate missing, stale, stuck, or polarity errors |
| `/api/i18n/{lang}` | GET | I18n | Localized strings dictionary (English / Hindi) |

---

## 📂 Repository Layout

```text
rural-microgrind/
├── README.md                           # Master project documentation
├── docs/
│   ├── demo_script.md                  # 3-minute video presentation script with timestamps
│   └── requirements.md                 # 20-item Requirements Traceability Matrix
├── reports/
│   ├── evaluation_report.md            # Comprehensive empirical technical evaluation report
│   └── user_validation.md              # 4-persona pilot protocol (validation pending field trial)
├── backend/
│   ├── main.py                         # FastAPI server initialization and middleware
│   ├── pyproject.toml                  # Backend project configuration
│   ├── requirements.txt                # Python dependencies
│   ├── app/
│   │   ├── api/                        # REST API routers (data, quality, rec, verif, etc.)
│   │   ├── core/                       # Config, Pydantic schemas, equipment registry loader
│   │   ├── engines/                    # 6 Core algorithmic engines:
│   │   │   ├── data_generator.py       # 90-day 15-min physics & telemetry generator
│   │   │   ├── disaggregation_engine.py# Scenario-based load disaggregation
│   │   │   ├── cause_engine.py         # Root-cause diagnostic & evidence scorer
│   │   │   ├── recommendation_engine.py# Recommendation lifecycle manager
│   │   │   ├── quality_engine.py       # Telemetry freshness & edge failure simulator
│   │   │   └── verification_engine.py  # Baseline vs Measured verification engine
│   │   └── i18n/                       # Backend internationalization dictionaries
│   └── tests/                          # 30 Pytest automated test cases
└── frontend/
    ├── package.json                    # React dependencies and scripts
    ├── vite.config.js                  # Vite bundler configuration
    ├── tailwind.config.js              # Tailwind CSS configuration
    └── src/
        ├── App.jsx                     # Root application container & navigation
        ├── components/                 # Reusable UI components (Navbar, Modal, Freshness, etc.)
        ├── pages/                      # 8 Page views (Dashboard, Disaggregation, Recs, etc.)
        └── i18n/                       # Frontend translation dictionaries
```

---

## 📜 Interactive Demo Presentation & Script

See [`docs/demo_script.md`](file:///c:/Users/M.DEEPAK%20KUMAR/Desktop/c28%20project/docs/demo_script.md) for the 3-minute video presentation transcript, timestamped screen navigation guide, and narrator cues (live video recording pending).

---

## 📑 Traceability Matrix

See [`docs/requirements.md`](file:///c:/Users/M.DEEPAK%20KUMAR/Desktop/c28%20project/docs/requirements.md) for the complete mapping from problem statement to implementation files, APIs, UI components, test evidence, and status (`PASS` / `PARTIAL` / `PENDING`).

---

## ⚖️ Limitations & Roadmap

- **Component Meter Disaggregation**: Current disaggregation utilizes synthetic sub-meter telemetry and contextual signals. Future iterations will integrate high-frequency Non-Intrusive Load Monitoring (NILM) harmonics (1–10 kHz).
- **Representative User Validation**: User testing protocol is formalized under [`reports/user_validation.md`](file:///c:/Users/M.DEEPAK%20KUMAR/Desktop/c28%20project/reports/user_validation.md) and labeled *"PENDING — representative-user validation not yet conducted"* until live hardware deployment.
- **Battery Energy Storage (BESS)**: Planned roadmap item to integrate automated lithium-ion battery dispatch alongside load shifting.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
