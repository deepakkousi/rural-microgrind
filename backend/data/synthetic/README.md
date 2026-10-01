# Synthetic Microgrid Scenario Dataset

- **Purpose**: Models a 90-day 15-minute resolution rural institutional microgrid (8,640 records).
- **Contextual Signals**: Includes Time-of-Use (tariff_rates off-peak ⊹4.5, shoulder ⋹7.0, peak ⊹12.0), campus occupancy percentage, and solar PV generation.
- **Experimental Phases**: historical Baseline (Days 1–30), Operational Intervention (Days 31–60), and Verified Policy (Days 61–90).
- **Generator Engine**: `backend/app/engines/data_generator.py`
~
