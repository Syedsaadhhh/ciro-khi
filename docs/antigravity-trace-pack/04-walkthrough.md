# 04 — Walkthrough of Changes Made

> **Project:** CIRO — Crisis Intelligence & Response Orchestrator
> **Scope:** Key changes, fixes, and improvements applied during development

---

## 1. Firestore `database_id` Fix

**Problem:** Initial Firestore client initialization used `database=` parameter, which is not recognized by `firebase_admin.firestore.client()`. This caused silent failures where the client defaulted to `(default)` database instead of the project-specific `cirokhi` database.

**Fix:** Changed parameter from `database=` to `database_id=` in `services/firestore_service.py`:

```python
# Before (broken)
_db = firestore.client(database="cirokhi")

# After (fixed)
database_id = os.getenv("FIREBASE_DATABASE_ID", "cirokhi")
_db = firestore.client(database_id=database_id)
```

**Impact:** Firestore now correctly connects to the `cirokhi` database. The fix also made the database ID configurable via environment variable.

**File:** `services/firestore_service.py` (line 42)

---

## 2. ValidatorGate Structured Validation

**Problem:** Early versions of the pipeline lacked a formal validation step between the Strategist and Commander. All incidents that passed the Strategist were automatically forwarded to the Commander, including potential false alarms that the Strategist's cross-validation might miss.

**Change:** Implemented `run_validator_gate()` as a dedicated method in the `FloodOrchestrator`:

- Extracts `social_score`, `rainfall_mm`, and `temperature` from incident raw signals
- Applies four distinct validation rules:
  - Confirmed: Strong social + strong telemetry → pass
  - Contradiction: Strong social + zero rainfall → operator review
  - Weak signal: Weak social + weak telemetry → operator review
  - Heatwave false alarm: Social crisis + low temperature → reject
- Detects fallback mode when telemetry sources return simulated data

**File:** `core/orchestrator.py` (lines 220–259)

---

## 3. Offline Simulation Engine

**Problem:** The dashboard needed to demonstrate full pipeline behavior during judging, even without backend connectivity or API keys.

**Change:** Built a JavaScript simulation engine directly into `static/index.html`:

- Three pre-built scenarios: Confirmed Flood, False Alarm, Missing Telemetry
- Each scenario generates a complete set of mock agent traces with realistic timing
- Traces are injected into the WebSocket trace terminal with appropriate color coding
- Map markers are placed at the simulated incident location
- Result overlay displays severity scorecard and safety labels
- Network detection: automatically activates offline mode when backend is unreachable

**File:** `static/index.html` (JavaScript section)

---

## 4. Network Badge System

**Problem:** Judges needed to understand whether the app was running against real APIs or simulated data.

**Change:** Added a real-time network status badge:

- Polls backend `/health` endpoint every 5 seconds
- Displays `🟢 ONLINE` (green) or `🔴 OFFLINE` (red) badge
- When offline, automatically enables demo mode buttons
- Badge appears in the header area of the dashboard

**File:** `static/index.html`

---

## 5. Demo Scenario Buttons

**Problem:** Judges needed quick, one-click access to demonstrate different system behaviors without manually crafting API requests.

**Change:** Added three scenario trigger buttons:

| Button | Scenario | Expected Output |
|---|---|---|
| ⚡ Confirmed Flood | University Road, 45mm rain, social score 0.93 | `validated: true`, full pipeline execution |
| 🚫 False Alarm | Clifton Block 5, 0mm rain, social score 0.85 | `requires_operator_review`, contradiction flag |
| ⚠️ Missing Telemetry | Korangi Industrial, fallback mode | `fallback_mode: true`, cached data validation |

**File:** `static/index.html`

---

## 6. Clock Fix for Karachi Timezone

**Problem:** The dashboard clock initially showed UTC time, which would be confusing during Pakistani judging.

**Change:** Updated the clock to display Pakistan Standard Time (PKT, UTC+5):

```javascript
const now = new Date().toLocaleTimeString('en-US', {
    timeZone: 'Asia/Karachi',
    hour12: false,
    hour: '2-digit',
    minute: '2-digit'
});
```

**File:** `static/index.html`

---

## 7. Source Badges (REAL/MOCK)

**Problem:** The system operates in multiple modes (live Gemini, deterministic fallback, simulation), and judges needed clarity on which data sources were active.

**Change:** Added visual badges on API responses:

- `REAL` badge (green) — Response came from live Gemini API or real telemetry
- `MOCK` badge (orange) — Response came from deterministic fallback or simulated data
- Badge logic checks for `fallback_mode`, `simulation_mode`, and Gemini availability flags

**File:** `static/index.html`

---

## 8. Result Overlay with Safety Labels

**Problem:** After pipeline execution, the raw JSON response was not user-friendly for judges.

**Change:** Added a result overlay that appears after each simulation run:

- **Severity scorecard:** Large numeric display of severity (1-10)
- **Safety labels:** Color-coded status — Confirmed (green), Requires Review (orange), Rejected (red)
- **Validation summary:** Shows which signals matched or mismatched
- **Actions list:** Displays all actions the Commander would execute
- **Alert message:** Shows the generated citizen alert text

**File:** `static/index.html`

---

## 9. IncidentModel Import Fix

**Problem:** The `FloodOrchestrator` referenced `IncidentModel` in the `run_validator_gate` type hint but the import was missing in an early version.

**Fix:** Added `IncidentModel` to the import statement in `core/orchestrator.py`:

```python
from models.incident import SignalInput, IncidentModel
```

**File:** `core/orchestrator.py` (line 12)

---

## 10. WebSocket Connection Resilience

**Problem:** WebSocket connections could fail silently if the client disconnected during pipeline execution, causing unhandled exceptions.

**Change:** Added try/catch wrappers around all `ws_manager.broadcast_*` calls in the orchestrator. Failed broadcasts are logged but do not interrupt pipeline execution.

**File:** `services/websocket_service.py`, `core/orchestrator.py`
