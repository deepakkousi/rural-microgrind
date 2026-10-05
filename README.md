# Rural Microgrid Intelligence Platform

[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-sky.svg)](https://reactjs.org)
[![Build Status](https://img.shields.io/badge/Tests-69%2F69%20Passed-emerald.svg)]()
[![API Contract](https://img.shields.io/badge/API_Contract-Documented_%26_Tested-blue.svg)](docs/API_CONTRACT.md)
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
6. Public benchmark validation (REDD House 1) and end-to-end integration testing.

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
## Testing Architecture

The project employs a rigorous, multi-layered automated testing architecture verified via 69 automated tests.
- **Unit Testing**: Isolated verification of engines (physics, verification math, quality thresholds).
- **API/Contract Testing**: Ensures strict Pydantic JSON schema synchronization with frontend TypeScript interfaces.
- **Public Dataset Validation**: Evaluates the algorithmic pipeline robustness against the uncurated REDD House 1 dataset.
- **E2E Integration Testing**: Validates the chronological lifecycle (Telemetry Ingestion -> Validation -> Disaggregation -> Cause -> Recommendation).

For complete technical execution details, coverage, and module breakdowns, see [docs/TESTING.md](docs/TESTING.md).

---

## Error Boundaries and Error Handling

The platform handles exceptions gracefully across both the backend and frontend:
- **Backend**: Implements a standardized JSON error envelope for 400 (validation), 404 (not found), 422 (unprocessable entity), and 500 (internal server errors).
- **Frontend**: The React application leverages a root <ErrorBoundary> component to catch rendering exceptions safely and provide recovery paths without crashing the UI. Missing or stale telemetry automatically suppresses unsafe recommendations.

---

## API Documentation and Contracts

The system enforces strict typing across the full stack. The FastAPI backend utilizes strictly typed Pydantic models synchronized with the React frontend's TypeScript interfaces (rontend/src/types/api.ts).

### Core REST API Endpoints Overview
| Endpoint | Method | Purpose |
|---|---|---|
| /api/data/meter | GET | Ingests the latest 15-minute telemetry state |
| /api/disaggregation | GET | Disaggregates load into component usage tiers |
| /api/recommendations | GET | Generates actionable interventions with Evidence Scores |
| /api/verification/summary | GET | Calculates baseline vs. target vs. measured savings |
| /api/quality/freshness | GET | Evaluates telemetry age (LIVE, STALE, MISSING) |

For the exhaustive specification covering all endpoints, parameters, and standardized JSON error structures, see [docs/API_CONTRACT.md](docs/API_CONTRACT.md).

---

## Data Schema & Telemetry Model

The platform processes time-series telemetry data rather than maintaining a traditional relational SQL database. The data flow relies on 15-minute resolution metrics tracking aggregate load, component loads (HVAC, Lighting, Water Pump, CNC, etc.), contextual variables (occupancy, tariff rates), and solar generation.

For the exact field definitions and data-flow pipeline mapping, see [docs/DATA_SCHEMA.md](docs/DATA_SCHEMA.md).

---

## Code Organization

`	ext
rural-microgrind/
|-- README.md                           # Master project documentation
|-- docs/
|   |-- TESTING.md                      # Testing architecture and framework
|   |-- API_CONTRACT.md                 # Formal API specifications & schema contracts
|   |-- DATA_SCHEMA.md                  # Data model and pipeline flow
|   |-- demo_script.md                  # 3-minute video presentation script
|   \-- requirements.md                 # Traceability Matrix
|-- backend/
|   |-- app/
|   |   |-- api/                        # REST API routers
|   |   |-- schemas/                    # Modular Pydantic models
|   |   \-- engines/                    # Core algorithmic engines (Disagg, Cause, Verif)
|   |-- data/                           # REDD and Synthetic telemetry
|   \-- tests/                          # 69 Pytest automated test cases (Unit, E2E, Contract)
\-- frontend/
    \-- src/
        |-- App.jsx                     # Root application container & ErrorBoundary
        |-- components/                 # Reusable UI components
        |-- pages/                      # Page views (Dashboard, Recommendations, etc.)
        \-- types/                      # TypeScript definitions (api.ts)
`

---

## Limitations & Roadmap

- **Component Meter Disaggregation**: Current disaggregation utilizes synthetic sub-meter telemetry and contextual signals. Future iterations will integrate high-frequency Non-Intrusive Load Monitoring (NILM) harmonics (1-10 kHz).
- **Public Dataset Generalizability**: Validation against REDD House 1 provides external validation of the processing pipeline, but does not establish rural microgrid field performance.
- **Representative User Validation**: User testing protocol is formalized under eports/user_validation.md and labeled *"PENDING"* until field execution.

---

## License
This project is open-source and licensed under the [MIT License](LICENSE).
