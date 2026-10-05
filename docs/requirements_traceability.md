# Requirements Traceability

| Requirement | Evidence/File | Status |
|---|---|---|
| Problem analysis | `README.md`, `reports/evaluation_report.md` | COMPLETE |
| User/workflow map | `README.md` (System Architecture) | COMPLETE |
| Meter data | `backend/app/engines/data_generator.py` | COMPLETE |
| Equipment schedules | `backend/app/core/loader.py` | COMPLETE |
| Occupancy | `backend/app/engines/data_generator.py` | COMPLETE |
| Tariff periods | `backend/app/api/routes_data.py` | COMPLETE |
| Disaggregation | `backend/app/engines/disaggregation_engine.py` | COMPLETE |
| Actionable causes | `backend/app/engines/cause_engine.py` | COMPLETE |
| Non-technical explanation | `frontend/src/components/DrillDownModal.jsx` | COMPLETE |
| Role-based views | `backend/app/main.py`, `frontend/src/components/RoleViewWrapper.jsx` | COMPLETE |
| Drill-down evidence | `frontend/src/components/DrillDownModal.jsx` | COMPLETE |
| Freshness indicators | `backend/app/engines/quality_engine.py`, `frontend/src/components/FreshnessBanner.jsx` | COMPLETE |
| Missing/stale states | `backend/app/engines/quality_engine.py` | COMPLETE |
| Failure cases | `backend/tests/test_edge_cases.py` | COMPLETE |
| Accessibility | `frontend/src/index.css` (AA-oriented practices) | COMPLETE |
| Language | `frontend/src/i18n/translations.js`, `backend/app/i18n/` | COMPLETE |
| Explainability | `backend/app/engines/cause_engine.py` | COMPLETE |
| Public benchmark | `backend/tests/test_public_dataset.py`, `backend/data/public/` | COMPLETE |
| API contracts | `docs/API_CONTRACT.md`, `backend/app/schemas/` | COMPLETE |
| Pydantic validation | `backend/app/schemas/` | COMPLETE |
| E2E testing | `backend/tests/integration/test_e2e_pipeline.py` | COMPLETE |
| Baseline | `backend/app/engines/verification_engine.py` | COMPLETE |
| Target | `backend/app/engines/verification_engine.py` | COMPLETE |
| Measured result | `backend/app/engines/verification_engine.py` | COMPLETE |
| Error analysis | `backend/app/engines/verification_engine.py` | COMPLETE |
| Evaluation report | `reports/evaluation_report.md` | COMPLETE |
| Source code | GitHub Repository | COMPLETE |
| README | `README.md` | COMPLETE |
| 3-minute demo | `docs/demo_script.md` | MANUAL ACTION REQUIRED |
| User validation | `reports/user_validation.md` | MANUAL ACTION REQUIRED |
