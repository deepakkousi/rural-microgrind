# Rural Microgrid Intelligence Platform

[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-sky.svg)](https://reactjs.org)
[![Build Status](https://img.shields.io/badge/Tests-23%2F23%20Passed-emerald.svg)]()
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
5. Role-based views (Operations, Manager, Technician, Resident) with multi-language (English/Hindi) and WCAG accessibility checks.

---

## ⚡ Energy Reduction vs. Cost Reduction (Load Shifting)

The platform explicitly distinguishes between two operational outcomes:

- **ENERGY REDUCTION (kWh)**: Direct reduction in electricity consumed (e.g. HVAC low-occupancy setback, Classroom Lighting dimming).
- **COST REDUCTION (LOAD SHIFTING)**: Shifting heavy load runtime from Peak Tariff to Off-Peak/Shoulder Tariff. Reduces electricity bill (₹/$) without claiming false kWh reduction (e.g. Water Pump peak shift, CNC machine peak shift).

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
| `net_grid_kw` | Float | Net power imported from grid (`total_kw` - `solar_gen_kw`) |
| `day_index` | Integer | Experiment day index (1 to 90) |

---

## ⚙️ Load Categories & Disaggregation Methodology

### Load Categories
- **Critical (24/7)**: Server Rack (`EQ_IT_01`), WiFi Network Switches (`EQ_IT_02`)
- **Essential**: Main Security Lighting (`EQ_LT_01`), Water Pump (`EQ_WP_01`), Kitchen (`EQ_KT_01`)
- **Flexible**: HVAC Chillers (`EQ_HVAC_01`), Classroom Lighting (`EQ_LT_02`), CNC Machine (`EQ_LAB_01`), 3D Printers (`EQ_LAB_02`)

### Methodology
*"Scenario-based synthetic load disaggregation using known component meter channels, equipment schedules, and contextual signals."*

### Empirical Accuracy Metrics
- **Mean Absolute Error (MAE)**: `0.243 kW`
- **Root Mean Square Error (RMSE)**: `0.304 kW`
- **Mean Absolute Percentage Error (MAPE)**: `1.15%`

---

## 🎯 Actionable Cause Detection & Recommendation Engine

The system explains root causes with transparent Evidence Strength Scores (0–100):

- **WHAT Happened?**: Water pump running during 5 PM - 7 PM Peak Tariff.
- **WHY Did It Happen?**: Automatic timer scheduled pump during ₹12.0/kWh peak electricity pricing.
- **EVIDENCE**: 7.1 kW draw during Peak Tariff when Off-Peak rate is ₹4.5/kWh.
- **RECOMMENDED ACTION**: Shift water pumping schedule to late night Off-Peak tariff (10 PM - 2 AM).
- **ESTIMATED SAVING**: `0.0 kWh/day` energy reduction (Load Shift) → `₹3,156.90 / month` cost saving.
- **EVIDENCE STRENGTH SCORE**: `95 / 100` (Fresh Data: +30, Schedule Overlap: +30, Tariff Overlap: +20, Occupancy Correlation: +15).

---

## 📈 Baseline vs. Measured Energy Reduction Experiment

Three 30-day experimental phases calculated dynamically from raw telemetry:
- **BASELINE (Days 1–30)**: `658.9 kWh/day` average
- **TARGET (15% Goal Target)**: `560.1 kWh/day` (Target Reduction: `98.8 kWh/day`)
- **MEASURED (Days 61–90)**: `559.2 kWh/day`
- **VERIFIED REDUCTION**: `99.7 kWh/day` (`15.13%` reduction)
- **TARGET ACHIEVEMENT RATIO**: `100.9%`

### Measured Financial Savings & Error Analysis
- **Daily Financial Saving**: `₹1,123.73 / day` (`₹33,711.90` total over 30-day verification period)
- **Target Error**: `0.9 kWh/day` (`0.91%` absolute percentage error)
- **Sensor Uncertainty**: Assumed sensor uncertainty (±1.8%), lower bound: `97.9 kWh/day`, upper bound: `101.5 kWh/day`.

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
- **Accessibility Checks**: Keyboard focus indicators (`focus-visible:ring-2`), contrast ratio > 4.5:1, screen reader labels, non-color-only badges.

---

## 🧪 Automated Testing

Run Pytest suite:
```bash
cd backend
python -m pytest tests/ -v
```
**Test Results**: **23 / 23 Passed (100% Pass Rate)**.

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

## 📜 Interactive Demo Video Script

See [`docs/demo_script.md`](file:///c:/Users/M.DEEPAK%20KUMAR/Desktop/c28%20project/docs/demo_script.md) for the 3-minute video presentation transcript and timestamped walkthrough.

---

## 📑 Traceability Matrix

See [`docs/requirements.md`](file:///c:/Users/M.DEEPAK%20KUMAR/Desktop/c28%20project/docs/requirements.md) for the complete mapping from problem statement to implementation files, APIs, UI components, and test evidence.
