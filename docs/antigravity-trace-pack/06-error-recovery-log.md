# 06 — Error Recovery Log

> **Project:** CIRO — Crisis Intelligence & Response Orchestrator
> **Scope:** Errors encountered during development and their resolutions

---

## Error #1: Firestore `database=` vs `database_id=` Parameter

**When:** During initial Firestore integration
**Severity:** Critical — Data was silently going to wrong database
**Symptom:** Firestore client initialized without error, but data was written to the `(default)` database instead of the project-specific `cirokhi` database. No error was thrown because `database=` was accepted as a generic keyword argument.

**Root Cause:** The `firebase_admin.firestore.client()` function expects `database_id=` (not `database=`) when specifying a non-default database.

**Fix:**
```python
# Before
_db = firestore.client(database="cirokhi")

# After
database_id = os.getenv("FIREBASE_DATABASE_ID", "cirokhi")
_db = firestore.client(database_id=database_id)
```

**Prevention:** Added `database_id` to `Settings` model in `core/config.py` with default `"(default)"` and environment variable override.

**File:** `services/firestore_service.py`

---

## Error #2: IncidentModel Missing Import in Orchestrator

**When:** After adding the `run_validator_gate()` method
**Severity:** Medium — Caused `NameError` at runtime
**Symptom:** `NameError: name 'IncidentModel' is not defined` when `run_validator_gate()` was called, because the type hint `incident: IncidentModel` referenced a class that wasn't imported.

**Root Cause:** The `IncidentModel` import was present for the `SignalInput` usage but had been inadvertently removed during a refactor.

**Fix:**
```python
# Before
from models.incident import SignalInput

# After
from models.incident import SignalInput, IncidentModel
```

**File:** `core/orchestrator.py`

---

## Error #3: Google Maps Initialization Failure in Offline Mode

**When:** During offline demo testing
**Severity:** Medium — Map area showed blank/error
**Symptom:** When the dashboard loaded without internet connectivity, the Google Maps JavaScript API failed to load, causing `google is not defined` errors in the console. The map area remained blank.

**Root Cause:** The Google Maps `<script>` tag was loaded synchronously, and the `initMap()` callback was invoked before checking connectivity.

**Fix:**
- Added a connectivity check before initializing Google Maps
- Created an SVG-based fallback map of Karachi for offline mode
- The fallback map includes labeled zones (Orangi Town, University Road, Korangi, DHA/Clifton) with incident marker overlay capability
- Wrapped `initMap()` in try/catch to prevent console errors

**File:** `static/index.html`

---

## Error #4: Firebase Crash on Disconnected Devices

**When:** During mobile emulator testing without network
**Severity:** High — App crashed on startup
**Symptom:** When running the app on a device without network connectivity, the Firebase SDK attempted to connect and threw an unhandled exception that crashed the Firestore initialization.

**Root Cause:** `firebase_admin.initialize_app()` and subsequent `firestore.client()` calls attempted network operations during initialization. Without network, these threw connection errors.

**Fix:**
- Wrapped the entire `_get_db()` function in try/catch
- On connection failure, the function returns `None` (triggering in-memory fallback)
- Added logging: `logger.warning("firestore_init_failed", error=str(e))`
- The `simulation_mode` check was moved to the top of `_get_db()` to short-circuit before any network calls

```python
def _get_db():
    global _db
    if _db:
        return _db
    if settings.simulation_mode or not settings.firebase_project_id:
        return None  # Skip network calls entirely
    try:
        # ... Firebase initialization ...
    except Exception as e:
        logger.warning("firestore_init_failed", error=str(e))
        return None  # Graceful fallback
```

**File:** `services/firestore_service.py`

---

## Error #5: WebSocket Connection Handling

**When:** During concurrent client testing
**Severity:** Low — Caused log noise but no data loss
**Symptom:** When a WebSocket client disconnected during pipeline execution, the `ws_manager.broadcast_*` calls threw `ConnectionClosedError` exceptions that appeared in the server logs.

**Root Cause:** The `broadcast_trace()` method iterated over active connections and attempted to send to all of them, including recently disconnected ones that hadn't been cleaned up yet.

**Fix:**
- Added per-connection try/catch in broadcast methods
- Failed sends trigger automatic connection cleanup
- Disconnection is logged as `websocket_client_disconnected` (info level, not error)
- Pipeline execution continues regardless of WebSocket broadcast failures

**File:** `services/websocket_service.py`

---

## Error #6: Gemini API Response Parsing

**When:** During live Gemini integration testing
**Severity:** Medium — Caused pipeline to use fallback unnecessarily
**Symptom:** Gemini occasionally returned responses wrapped in markdown code fences (` ```json ... ``` `), which caused `json.loads()` to fail.

**Root Cause:** Despite the system prompt requesting "ONLY valid JSON. No markdown," Gemini 3 Flash-Preview sometimes wrapped responses in code fences.

**Fix:**
```python
text = response.text.strip()
if text.startswith("```"):
    text = text.split("```")[1]
    if text.startswith("json"):
        text = text[4:]
data = json.loads(text)
```

This stripping logic handles both ` ```json ` and bare ` ``` ` wrappers.

**File:** `agents/sifter_agent.py` (lines 129–133)

---

## Error #7: Congestion Level Type Mismatch

**When:** During edge case testing
**Severity:** Low — Caused incorrect routing decisions
**Symptom:** The Strategist's rerouting logic compared `congestion_level` against integer thresholds, but the traffic tool sometimes returned the value as a string (e.g., `"severe"` instead of `8`).

**Root Cause:** The mock traffic data used descriptive strings, while the comparison logic expected integers.

**Fix:** Added type coercion in the Strategist:
```python
congestion = traffic.get("congestion_level", 5)
if isinstance(congestion, str):
    congestion_map = {"severe": 9, "heavy": 7, "moderate": 5, "light": 3}
    congestion = congestion_map.get(congestion, 5)
```

**File:** `agents/strategist_agent.py`

---

## Summary

| # | Error | Severity | Category | Resolution Time |
|---|---|---|---|---|
| 1 | Firestore parameter name | Critical | Configuration | ~15 min |
| 2 | Missing import | Medium | Code structure | ~5 min |
| 3 | Google Maps offline | Medium | Frontend resilience | ~30 min |
| 4 | Firebase offline crash | High | Error handling | ~20 min |
| 5 | WebSocket disconnect | Low | Connection lifecycle | ~15 min |
| 6 | Gemini response format | Medium | API integration | ~10 min |
| 7 | Type mismatch | Low | Data validation | ~10 min |

All errors were identified and resolved during development. The system now handles all seven scenarios gracefully through explicit error handling and fallback mechanisms.
