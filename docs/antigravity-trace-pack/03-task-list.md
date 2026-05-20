# 03 — Task List

> **Project:** CIRO — Crisis Intelligence & Response Orchestrator
> **Last Updated:** 2026-05-20T02:30:00+05:00

---

## Backend Setup

- [x] Initialize FastAPI project structure
- [x] Configure `main.py` with async lifespan
- [x] Set up CORS middleware
- [x] Implement structured logging (`structlog`)
- [x] Create `core/config.py` with `pydantic_settings`
- [x] Create `.env` and `.env.example`
- [x] Create `requirements.txt` with all dependencies
- [x] Harden `.gitignore` (credentials, logs, `__pycache__`)

## Data Models

- [x] Define `SignalInput` model
- [x] Define `IncidentModel` with severity, confidence, raw_signals
- [x] Define `PlanModel` with priority, population, routes
- [x] Define `ActionModel` with alert message, geofence, ticket
- [x] Define `SimulateRequest` for API input
- [x] Define `RouteModel` for alternative routing

## Agent Pipeline

- [x] Implement `SifterAgent` with Gemini + deterministic fallback
- [x] Implement `StrategistAgent` with cross-validation
- [x] Implement `CommanderAgent` with alert generation
- [x] Implement `FloodOrchestrator` with sequential pipeline
- [x] Add Tenacity retry logic in orchestrator
- [x] Add WebSocket broadcast at every pipeline stage
- [x] Add trace logging (`state.add_trace`) in every agent

## ValidatorGate Logic

- [x] Implement confirmed flood validation (social + rainfall match)
- [x] Implement contradiction detection (social high, rainfall zero)
- [x] Implement weak signal detection (low social + low rainfall)
- [x] Implement heatwave false alarm detection (temperature check)
- [x] Implement fallback mode detection (simulated telemetry)
- [x] Wire ValidatorGate into orchestrator pipeline

## Tool Modules

- [x] `weather_tool.py` — Meteosource API with fallback
- [x] `traffic_tool.py` — TomTom API with fallback
- [x] `social_signal_tool.py` — Roman Urdu parser + mock posts
- [x] `geofence_tool.py` — Impact zone calculator
- [x] `reroute_tool.py` — Alternative routes + delay estimation
- [x] `alert_tool.py` — Alert object + emergency ticket creation

## Storage Layer

- [x] Implement Firestore service with `database_id` parameter
- [x] Implement in-memory `_mem_store` fallback
- [x] Add `save_incident`, `save_plan`, `save_alert`, `save_trace`
- [x] Add `log_agent_event` for agent activity logging
- [x] Add `get_all_incidents`, `get_all_alerts`, `get_all_traces`
- [x] Fix `database=` → `database_id=` Firestore parameter

## WebSocket Service

- [x] Implement `WebSocketManager` class
- [x] Add broadcast methods (trace, incident, alert, status)
- [x] Handle connection lifecycle (connect/disconnect)
- [x] Wire WebSocket to `/ws/live-trace` endpoint

## Frontend Dashboard

- [x] Build 5-screen SPA (`static/index.html`)
- [x] Screen 1: Map with Google Maps integration
- [x] Screen 2: Agent Trace terminal with color-coded rows
- [x] Screen 3: Before/After comparison view
- [x] Screen 4: KPI dashboard cards
- [x] Screen 5: Alerts feed with filter chips
- [x] Bottom navigation with active state
- [x] Status bar with live time display
- [x] Dark ops theme with CSS custom properties

## Offline Demo Mode

- [x] Build offline simulation engine in JavaScript
- [x] Create scenario: Confirmed Flood
- [x] Create scenario: False Alarm
- [x] Create scenario: Missing Telemetry (Fallback Mode)
- [x] Add demo scenario trigger buttons
- [x] Add network status badge (ONLINE/OFFLINE)
- [x] Add source badges (REAL/MOCK)
- [x] Add result overlay with safety labels

## Mobile Packaging

- [x] Configure `capacitor.config.json`
- [x] Configure `package.json` with Capacitor dependencies
- [x] Write `MOBILE_INSTALL.md` build instructions
- [x] Configure emulator bridge (`10.0.2.2`)
- [ ] Build signed APK via Android Studio (pending build station)

## Evidence Pack

- [x] Generate `health-response.json`
- [x] Generate `simulate-response.json`
- [x] Generate `false-positive-response.json`
- [x] Generate `weak-signal-response.json`
- [x] Generate `contradiction-response.json`
- [x] Generate `missing-telemetry-fallback.json`
- [x] Generate `firestore-incident-sample.json`
- [x] Write `cost-latency-scaling.md`
- [x] Write `demo-script.md`
- [x] Write `mobile-app-proof.md`
- [x] Write `screenshot-checklist.md`
- [x] Generate `simulate-request.json`

## README Finalization

- [x] Write 21-section README.md
- [x] Add Mermaid architecture diagram
- [x] Add API surface table
- [x] Add testing matrix (6 scenarios)
- [x] Add judge Q&A reference
- [x] Add team contribution ledger
- [x] Document false positive/negative handling
- [x] Document cost, latency, and scalability

## Trace Pack

- [x] `01-main-orchestrator-proof.md`
- [x] `02-implementation-plan.md`
- [x] `03-task-list.md` (this file)
- [x] `04-walkthrough.md`
- [x] `05-agent-observations.md`
- [x] `06-error-recovery-log.md`
- [x] `07-final-outcomes.md`
- [x] `08-team-usage-notes.md`
- [x] `09-submission-readiness.md`
- [x] `ZIP_README.md`
- [x] Team task logs (4 files)

## Submission Docs

- [x] Demo video script
- [x] Antigravity usage video script
- [x] Demo shotlist
- [x] Antigravity video shotlist
- [x] Voiceover script
- [x] Judge Q&A reference (20 questions)
- [x] One-page project summary
- [x] Submission form answer drafts
- [x] File naming guide
- [x] Drive folder map
- [x] Final submission checklist
- [x] Final run checkpoint

---

## Summary

| Category | Tasks | Complete | Remaining |
|---|---|---|---|
| Backend | 8 | 8 | 0 |
| Data Models | 6 | 6 | 0 |
| Agent Pipeline | 7 | 7 | 0 |
| ValidatorGate | 6 | 6 | 0 |
| Tool Modules | 6 | 6 | 0 |
| Storage Layer | 6 | 6 | 0 |
| WebSocket | 4 | 4 | 0 |
| Frontend | 9 | 9 | 0 |
| Offline Demo | 8 | 8 | 0 |
| Mobile Packaging | 5 | 4 | 1 (APK build) |
| Evidence Pack | 12 | 12 | 0 |
| README | 8 | 8 | 0 |
| Trace Pack | 14 | 14 | 0 |
| Submission Docs | 12 | 12 | 0 |
| **Total** | **111** | **110** | **1** |

> **Note:** The one remaining task (APK build) requires Android Studio on a machine with the Android SDK. The web dashboard is fully functional standalone.
