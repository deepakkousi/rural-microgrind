with open('README.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = """## Error Boundaries and Error Handling

The platform handles exceptions gracefully across both the backend and frontend:
- **Backend**: Implements a standardized JSON error envelope for 400 (validation), 404 (not found), 422 (unprocessable entity), and 500 (internal server errors).
- **Frontend**: The React application leverages a root <ErrorBoundary> component to catch rendering exceptions safely and provide recovery paths without crashing the UI. Missing or stale telemetry automatically suppresses unsafe recommendations."""

replacement = """## Error Boundaries and Error Handling

The platform handles exceptions gracefully by clearly distinguishing between backend, network, and rendering failures:

1. **Backend / API Errors**:
   - Implements a standardized JSON error envelope: `{ "error": { "code", "message", "details", "timestamp" } }`.
   - Explicitly handles `400` (invalid parameters), `404` (missing resources), `422` (validation schemas), and `500` (internal server errors). Unsafe telemetry (missing/stale) returns specific operational data-unavailable statuses.

2. **Frontend Network Errors**:
   - The React API service handles timeout/network failures gracefully, avoiding infinite loading states by presenting clear "Backend Unavailable" fallback UI components.

3. **Frontend Rendering Errors**:
   - Implemented via a central React `<ErrorBoundary>` component (`frontend/src/components/ErrorBoundary.jsx`).
   - Catching React component crashes prevents the entire DOM from unmounting (white screen of death) and provides a user-friendly fallback UI with a localized "Reload Dashboard" action."""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(text.replace(target, replacement))
