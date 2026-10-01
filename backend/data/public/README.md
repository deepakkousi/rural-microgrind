#
+ Public Dataset Metadata: REDD (Reference Energy Disaggregation Data Set)

## 1. Dataset Overview
- Dataset Name: REDD (Reference Energy Disaggregation Data Set) â€“ House 1 Standardized Benchmark
- Source Citation: J. Zico Kolter and Matthew J. Johnson. "REDF­¶¸›º×º A public data set for energy disaggregation research." In Proceedings of the SustKDD Conference (ACM, 2011).
- Public URL: http://redd.csail.mit.edu/
- Dataset Type: Real-world residential high-resolution energy telemetry.

## 2. Technical Specifications
- Sampling Frequency: Standardized to 15-minute intervals (96 intervals/day).
- Duration & Record Count: 7 days (April 18 - 24, 2011), 672 records.
- Physical Unit: Kilowatts (kW) (converted from Watts: kW = Watts / 1000).
- Available Channels:
  1. mains_power_kw: Aggregate feeder power (House 1 Mains).
  2. hvac_kw: Air conditioning / cooling circuits.
  3. lighting_kw: Lighting branch circuits.
  4. kitchen_kw: Refrigerator and cooking appliances.
  5. electronics_kw: Consumer electronics and home IT.
  6. unmetered_other_kw: Residual sockets and parasitic draws.

## 3. Preprocessing Steps
1. Timestamp Normalization: Standardized to ISO-8601 strings (YYYY-MM-DDTHH:MM:SS).
2. Missing Value Handling: Linear interpolation for gaps < 30 divisions.
3. Unit Conversion: Converted Watts to kW, rounded to 3 decimal places.
4. Resampling: Downsampled to 15-minute average power intervals.

## 4. Clear Classification of Data Types
- REAL PUBLIC DATA:Â Metered electrical power readings (REDD house 1).
- SYNTHETIC CONTEXT DATA:p¨Rural microgrid Time-of-Use tariffs and student occupancy schedules are NOT in REDD and are NOT injected into public data metrics. Such context remains restricted to the synthetic microgrid experiment.
- DERIVED DATA:Â MAE, RMSE, MAPE, WAPE calculated by the validation pipeline.

## 5. Explicit Limitations
- Not a Rural Microgrid: REDD is residential building data from Cambridge, MA, USA, not a rural Indian microgrid, water pump, or solar generation.
- Validation Scope: Validates that our data ingestion, schema validation, cleaning, and disaggregation metrics pipeline runs reliably on external real-world energy telemetry.
