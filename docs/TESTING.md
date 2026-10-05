# Testing Architecture and Documentation

The Rural Microgrid Intelligence Platform utilizes a rigorous, multi-layered automated testing architecture. Tests are written in Python using the `pytest` framework and `httpx`/`TestClient` for FastAPI endpoint verification.

## Testing Layers

1. **Unit Testing**: Tests individual components, data generation physics, and isolated engines (e.g., verifying `verification_engine.py` calculations in isolation).
2. **API/Contract Testing**: Validates that FastAPI endpoints return the exact Pydantic-defined JSON schema expected by the React frontend TypeScript interfaces.
3. **Public Dataset Validation**: Evaluates the algorithmic robustness of the disaggregation pipeline against the public REDD House 1 dataset.
4. **End-to-End (E2E) Integration Testing**: Verifies the complete chronological lifecycle: Telemetry Ingestion → Validation → Quality Checks → Disaggregation → Cause Detection → Recommendation.

## Test Directory Structure

All tests reside in the `backend/tests/` directory:

*   **`test_api.py`**: Verifies core system API logic including `/api/health`, i18n translation fallbacks, and role-based view permissions.
*   **`test_api_contracts.py`**: Contains 26 exhaustive tests validating strict adherence to API contracts, OpenAPI specs, structured error envelopes (400, 404, 422), and exact Pydantic model serialization.
*   **`test_cause_recommendations.py`**: Validates the recommendation engine, ensuring accurate cause detection, appropriate intervention types (Energy vs. Cost), heuristic Evidence Strength Scoring, and status transitions.
*   **`test_disaggregation.py`**: Verifies the mathematical breakdown of component loads against the aggregate main feeder, alongside the accuracy of drill-down evidence endpoints.
*   **`test_edge_cases.py`**: Rigorously simulates physical sensor anomalies including missing data handling, stuck sensor flatlines, negative load readings (polarity inversion), and dynamic tariff revisions.
*   **`test_generator.py`**: Validates the synthetic data physics, ensuring continuous unique timestamps, logical tariff periods, occupancy correlation, and total energy sum conservation.
*   **`test_quality.py`**: Tests the `quality_engine.py` classification thresholds for `LIVE` (<15m), `STALE` (>15m), and `MISSING` data states.
*   **`test_public_dataset.py`**: Tests the public REDD pipeline (loading, cleaning, channel mapping) and verifies empirical metrics like MAE, RMSE, MAPE, WAPE, and EER against real-world uncurated telemetry.
*   **`test_verification.py`**: Tests the empirical verification math: baseline creation, target reduction calculations, reconciliation variance, and cost savings vs. energy savings logic.
*   **`integration/test_e2e_pipeline.py`**: Contains sequential E2E tests validating multiple continuous flows (e.g., normal pipeline, missing telemetry flow, stale data degradation).

## Executing the Test Suite

To run the complete test suite (all 69 tests):
```bash
python -m pytest backend/tests/ -v
```

To run a specific layer, point to the respective file. For example, to run just the API Contract tests:
```bash
python -m pytest backend/tests/test_api_contracts.py -v
```

## Coverage and Results

Based on the most recent execution, the repository maintains the following verifiable test counts:

*   **Collected**: 69
*   **Passed**: 69
*   **Failed**: 0
*   **Skipped**: 0
*   **Errors**: 0

*Total Tests by Category:*
*   Core Unit Tests: 31
*   Public Dataset Validation: 6
*   API Contract Tests: 26
*   E2E Integration Tests: 6
