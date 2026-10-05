# Data Schema & Telemetry Model

The Rural Microgrid Intelligence Platform does not rely on a traditional relational database (SQL) for real-time telemetry storage. Instead, it utilizes an in-memory Pandas dataframe generated from the synthetic telemetry engine (for the scenario) or loaded from CSV (for public benchmark validation). 

## Primary Telemetry Schema (15-Minute Resolution)

This structure represents the core time-series data ingested and processed by the disaggregation and verification engines.

| Field Name | Data Type | Units | Description |
|---|---|---|---|
| `timestamp` | `ISO-8601 string` | - | The exact 15-minute chronological timestamp of the reading. |
| `day_index` | `integer` | days | The index (1-90) of the current day in the scenario experiment. |
| `occupancy` | `float` | % (0.0-1.0) | The estimated percentage of total campus/building occupancy. |
| `tariff_period` | `string` | - | The ToU classification: `Off-Peak`, `Shoulder`, or `Peak`. |
| `tariff_rate` | `float` | ₹/kWh | The exact financial cost of electricity during this period. |
| `total_kw` | `float` | kW | The aggregate main feeder consumption (includes all circuits). |
| `hvac_kw` | `float` | kW | Sub-metered or disaggregated load for heating/cooling. |
| `lighting_kw` | `float` | kW | Sub-metered or disaggregated load for lighting. |
| `water_pump_kw` | `float` | kW | Sub-metered or disaggregated load for water pumping. |
| `lab_equipment_kw` | `float` | kW | Sub-metered or disaggregated load for heavy laboratory equipment. |
| `kitchen_kw` | `float` | kW | Sub-metered or disaggregated load for kitchen operations. |
| `it_network_kw` | `float` | kW | Sub-metered or disaggregated load for IT and networking infrastructure. |
| `solar_gen_kw` | `float` | kW | Local photovoltaic solar generation. |
| `net_grid_kw` | `float` | kW | Net power drawn from the main grid (`total_kw - solar_gen_kw`). |

## Data Flow Pipeline

Data flows chronologically through the system via the following stages:

1. **Telemetry Ingestion**: Data is pulled from the `data_generator.py` engine or external CSV into a Pandas DataFrame.
2. **Validation**: Pydantic schemas (e.g., `MeterData`) strictly validate API types, boundaries, and timestamps.
3. **Data Quality**: The `quality_engine.py` checks the latest timestamp against the server clock to assign a state (`LIVE`, `STALE`, `VERY_STALE`, `MISSING`) and runs variance checks to detect stuck sensors or negative readings.
4. **Disaggregation**: The `disaggregation_engine.py` calculates the proportional loads of flexible and essential components based on the aggregate signal and context.
5. **Cause Detection**: The `cause_engine.py` cross-references flexible usage against occupancy, schedules, and ToU tariffs to identify inefficiencies.
6. **Recommendation Generation**: The `recommendation_engine.py` constructs actionable advice, calculates Evidence Strength Scores, and identifies `ENERGY_REDUCTION` vs `COST_REDUCTION`.
7. **Verification**: The `verification_engine.py` calculates empirical baseline vs. measured reductions across the full dataframe.
8. **Frontend**: React components (via TypeScript interfaces) render the final payload.
