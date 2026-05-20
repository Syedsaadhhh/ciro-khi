# CIRO Firestore Schema — Database: `cirokhi`

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Firestore Database: `cirokhi`  
> Project: `ciro-karachi`  
> Version: 2.1.0  
> Last Updated: 2026-05-20

---

## Overview

CIRO uses Google Cloud Firestore (database ID: `cirokhi`) as its primary data store. All incident data, alerts, reasoning traces, simulation records, and agent logs are persisted here. The frontend reads from these collections in real time via Firestore listeners.

---

## Collection: `/incidents/{incident_id}`

**Purpose:** Stores every processed incident, whether confirmed, rejected, or pending review.  
**Document ID format:** `INC-YYYY-MMDD-NNNN` (auto-generated, sequential per day)

| Field | Type | Description |
|-------|------|-------------|
| `incident_id` | string | Unique incident identifier |
| `session_id` | string | Pipeline session identifier |
| `event_type` | string | `flood`, `heatwave`, `earthquake`, `infrastructure`, `uncertain` |
| `location` | string | Human-readable location name |
| `coordinates` | map | `{ lat: number, lng: number }` — Karachi coordinates |
| `severity` | number | 0.0–10.0 computed severity score |
| `priority` | string | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `validated` | boolean | `true` if ValidatorGate confirmed the incident |
| `confidence` | number | 0.0–1.0 final confidence score |
| `fallback_mode` | boolean | `true` if any telemetry was unavailable |
| `raw_signals` | map | Nested weather, traffic, social signal objects |
| `safety_validation` | map | Full ValidatorGate output (checks, status, confidence) |
| `command_package` | map | CommanderAgent output (alert, geofence, ticket, routes) |
| `estimated_affected_population` | number \| null | Estimated people affected |
| `estimated_delay_minutes` | number \| null | Estimated traffic delay |
| `timestamp` | timestamp | When the incident was processed |
| `created_at` | timestamp | Document creation time |
| `updated_at` | timestamp | Last update time |
| `pipeline_duration_ms` | number | Total pipeline processing time |
| `agent_versions` | map | Version of each agent that processed this incident |

### Example Document Path
```
projects/ciro-karachi/databases/cirokhi/documents/incidents/INC-2026-0520-0001
```

---

## Collection: `/alerts/{alert_id}`

**Purpose:** Stores all generated alerts, including suppressed ones.  
**Document ID format:** `ALT-YYYY-MMDD-NNNN`

| Field | Type | Description |
|-------|------|-------------|
| `alert_id` | string | Unique alert identifier |
| `incident_id` | string | Reference to parent incident |
| `session_id` | string | Pipeline session identifier |
| `level` | string | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO` |
| `message` | string | Human-readable alert message |
| `channels` | array | List of delivery channels: `sms`, `app_push`, `dashboard`, `public_pa` |
| `geofence` | map \| null | `{ center: { lat, lng }, radius_km, restriction }` |
| `dispatched` | boolean | `true` if alert was sent (always simulated in prototype) |
| `suppressed` | boolean | `true` if ValidatorGate suppressed this alert |
| `suppressed_reason` | string \| null | Why the alert was suppressed |
| `operator_approved` | boolean \| null | `true` if operator approved dispatch |
| `timestamp` | timestamp | Alert creation time |

### Example Document Path
```
projects/ciro-karachi/databases/cirokhi/documents/alerts/ALT-2026-0520-0001
```

---

## Collection: `/reasoning_traces/{session_id}`

**Purpose:** Stores the full reasoning trace for each pipeline execution — used for debugging, auditing, and the live trace viewer.  
**Document ID format:** `sess-YYYYMMDD-HHMMSS-location`

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Unique session identifier |
| `incident_id` | string | Reference to the resulting incident |
| `location` | string | Input location |
| `started_at` | timestamp | Pipeline start time |
| `completed_at` | timestamp | Pipeline completion time |
| `duration_ms` | number | Total processing time |
| `status` | string | Final pipeline status |
| `stages` | array | Ordered list of stage trace objects |
| `stages[].agent` | string | Agent name |
| `stages[].stage_number` | number | 1–4 |
| `stages[].started_at` | timestamp | Stage start time |
| `stages[].completed_at` | timestamp | Stage end time |
| `stages[].duration_ms` | number | Stage processing time |
| `stages[].input_summary` | string | Brief description of stage input |
| `stages[].output_summary` | string | Brief description of stage output |
| `stages[].decisions` | array | List of decision point descriptions |
| `stages[].trace_events` | array | Ordered list of trace event objects |
| `error` | string \| null | Error message if pipeline failed |
| `fallback_activated` | boolean | Whether fallback mode was used |

### Example Document Path
```
projects/ciro-karachi/databases/cirokhi/documents/reasoning_traces/sess-20260520-023000-univ-road
```

---

## Collection: `/simulations/{incident_id}`

**Purpose:** Stores metadata for each simulation run, linking input to output for reproducibility.  
**Document ID format:** Same as incident_id (`INC-YYYY-MMDD-NNNN`)

| Field | Type | Description |
|-------|------|-------------|
| `incident_id` | string | Reference to the resulting incident |
| `session_id` | string | Pipeline session identifier |
| `input` | map | Original SignalInput payload |
| `input.location` | string | Input location |
| `input.social_posts` | array | Input social posts |
| `input.rainfall_mm` | number | Input rainfall |
| `input.congestion_level` | number | Input congestion |
| `output_status` | string | Final pipeline status |
| `output_severity` | number | Computed severity |
| `output_confidence` | number | Final confidence |
| `output_validated` | boolean | Whether ValidatorGate confirmed |
| `duration_ms` | number | Pipeline duration |
| `timestamp` | timestamp | Simulation run time |
| `triggered_by` | string | `operator`, `automated_test`, `demo` |

### Example Document Path
```
projects/ciro-karachi/databases/cirokhi/documents/simulations/INC-2026-0520-0001
```

---

## Collection: `/agent_logs/{auto_id}`

**Purpose:** Stores individual agent-level log entries for monitoring and debugging. Auto-ID documents for append-only logging.  
**Document ID format:** Firestore auto-generated ID

| Field | Type | Description |
|-------|------|-------------|
| `agent` | string | Agent name: `SifterAgent`, `StrategistAgent`, `ValidatorGate`, `CommanderAgent`, `Orchestrator` |
| `session_id` | string | Pipeline session identifier |
| `incident_id` | string \| null | Associated incident, if applicable |
| `level` | string | `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `message` | string | Log message |
| `data` | map \| null | Optional structured data |
| `timestamp` | timestamp | Log entry time |
| `agent_version` | string | Version of the agent |

### Example Document Path
```
projects/ciro-karachi/databases/cirokhi/documents/agent_logs/abc123def456
```

---

## Firestore Security Rules (Summary)

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/cirokhi/documents {
    // Incidents: read by authenticated users, write by backend service account only
    match /incidents/{incidentId} {
      allow read: if request.auth != null;
      allow write: if false; // Server-side only
    }
    
    // Alerts: same as incidents
    match /alerts/{alertId} {
      allow read: if request.auth != null;
      allow write: if false;
    }
    
    // Reasoning traces: read by authenticated users
    match /reasoning_traces/{sessionId} {
      allow read: if request.auth != null;
      allow write: if false;
    }
    
    // Simulations: read by authenticated users
    match /simulations/{incidentId} {
      allow read: if request.auth != null;
      allow write: if false;
    }
    
    // Agent logs: read by admin only
    match /agent_logs/{logId} {
      allow read: if request.auth.token.admin == true;
      allow write: if false;
    }
  }
}
```

> **Note:** In the production-oriented prototype, Firestore rules are permissive for demo purposes. The rules above represent the intended production configuration.

---

## Data Flow Diagram

```
POST /simulate
    │
    ▼
┌─────────────┐    ┌──────────────────────┐
│ SifterAgent  │───▶│ /agent_logs/{auto_id}│
└─────┬───────┘    └──────────────────────┘
      │
      ▼
┌───────────────┐  ┌──────────────────────┐
│StrategistAgent│─▶│ /agent_logs/{auto_id}│
└─────┬─────────┘  └──────────────────────┘
      │
      ▼
┌───────────────┐  ┌──────────────────────┐
│ ValidatorGate │─▶│ /agent_logs/{auto_id}│
└─────┬─────────┘  └──────────────────────┘
      │
      ▼
┌────────────────┐ ┌──────────────────────┐
│ CommanderAgent │─▶│ /agent_logs/{auto_id}│
└─────┬──────────┘ └──────────────────────┘
      │
      ▼
┌────────────────────────────────────────────┐
│ Firestore Writes (parallel):               │
│  • /incidents/{incident_id}                │
│  • /alerts/{alert_id}                      │
│  • /reasoning_traces/{session_id}          │
│  • /simulations/{incident_id}              │
└────────────────────────────────────────────┘
```

---

*CIRO is a production-oriented prototype. Schema may evolve based on deployment requirements.*
