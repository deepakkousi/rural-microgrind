# 3-Minute Video Demo Script — Rural Microgrid Intelligence Platform

> [!NOTE]
> **Status: Demo script and screen walkthrough available; live video recording pending.**

This document provides a precise, timestamped narration and screen navigation guide for recording a 3-minute video demonstration of the working Rural Microgrid Intelligence Platform prototype.

---

### **Video Overview & Timing**

| Timestamp | Section | Visual Focus | Audio / Key Point Narration |
|---|---|---|---|
| **0:00 – 0:20** | **1. Problem Introduction** | Slide / Overview Dashboard | "Rural microgrids balance essential and flexible loads, but traditional dashboards only show total consumption without explaining *why* energy usage spikes or what operators should do. Here is our Rural Microgrid Intelligence Platform." |
| **0:20 – 0:50** | **2. Main Dashboard & Roles** | Role Selector & Main Dashboard | "We start on the Main Dashboard. Notice our 4 role views: Operations, Manager, Technician, and Resident. Switching to Manager shows overall cost and carbon savings. Switching to Resident simplifies energy into non-technical terms. We also support Hindi localization." |
| **0:50 – 1:20** | **3. Load Disaggregation** | Disaggregation Page | "Under Load Disaggregation, raw 15-minute smart meter telemetry is disaggregated into 9 equipment categories across Critical, Essential, and Flexible tiers. Evaluation metrics achieve an MAE of 0.243 kW and RMSE of 0.304 kW against component meters." |
| **0:20 – 1:50** | **4. Cause Detection & Drill-Down** | Drill-Down Evidence Modal | "Clicking on the Water Pump or HVAC reveals drill-down evidence. Rather than just reporting high energy, the platform explains *why*: Water Pumping was scheduled during Peak Tariff (5-7 PM) while occupancy was normal. It provides time-series alignment of schedule vs occupancy vs tariff." |
| **1:50 – 2:20** | **5. Recommendation & Action** | Recommendations Page | "In Recommendations, actionable interventions are generated with explicit estimated savings (kWh & ₹), evidence strength scores (0–100), and data freshness flags. The operator clicks 'Apply Action' to shift water pumping to off-peak hours (10 PM - 2 AM)." |
| **2:20 – 2:45** | **6. Baseline → Target → Measured Verification** | Verification Dashboard | "Our mandatory 90-day experiment shows: **Baseline (Days 1–30)**: 643.9 kWh/day average → **Target**: 547.3 kWh/day → **Measured (Days 61–90)**: 561.9 kWh/day. This validates an actual measured energy reduction of 12.73% (82.0 kWh/day feeder reduction, with 82.9 kWh/day direct submeter savings reconciled, ₹1,000.63/day saved) with an assumed prototype sensor uncertainty of ±1.8%." |
| **2:45 – 3:00** | **7. Data Quality & Failure Cases** | Data Quality / Edge Simulator | "Finally, in Data Quality, we demonstrate resilience. Simulating a missing meter signal or stuck sensor instantly updates the freshness badge to STALE/MISSING, flags sensor health, and safely disables unverified automated recommendations." |

---

### **Instructions for Recording**

1. **Environment Setup**:
   - Start the FastAPI backend: `python main.py` (running on `http://localhost:8000`).
   - Start the React Vite frontend: `npm run dev` (running on `http://localhost:5173`).
   - Open Chrome at standard 1080p (1920x1080) resolution.

2. **Screen Recording Tools**:
   - Use OBS Studio, Windows Game Bar (Win+G), or Loom.
   - Record system audio or add clear voiceover using the script above.

3. **Key Visual Interactions to Capture**:
   - Role dropdown changing between Manager, Operations, Technician, and Resident.
   - Language switch between English (EN) and Hindi (HI).
   - Clicking a load card to open the Drill-down Evidence modal.
   - Clicking "Apply Action" on a recommendation card.
   - Triggering a failure case (e.g. "Stuck Sensor") in the Data Quality page to show safety fallback.
