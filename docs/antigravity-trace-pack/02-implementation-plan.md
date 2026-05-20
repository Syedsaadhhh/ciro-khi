# 02 — Implementation Plan

> **Project:** CIRO — Crisis Intelligence & Response Orchestrator
> **Challenge:** AISeekho 2026, Challenge 3
> **Status:** Executed & Complete

---

## Overview

This document captures the implementation plan that guided CIRO's development from initial concept to submission-ready prototype. Each phase was executed sequentially with Antigravity orchestrating the work.

---

## Phase 1: Backend Foundation (FastAPI + Multi-Agent Pipeline)

### 1.1 Core Framework
- [x] Initialize FastAPI application with async lifecycle (`main.py`)
- [x] Configure CORS middleware for cross-origin mobile access
- [x] Set up structured logging via `structlog`
- [x] Implement `pydantic_settings.BaseSettings` for environment configuration (`core/config.py`)
- [x] Create `.env` / `.env.example` for secrets management
- [x] Add `.gitignore` to prevent credential leaks

### 1.2 Data Models (Pydantic)
- [x] `SignalInput` — Raw input from social/weather/traffic sources
- [x] `IncidentModel` — Detected crisis with severity, confidence, raw signals
- [x] `PlanModel` — Strategist output with priority, population, routes
- [x] `ActionModel` — Commander output with alert message, actions, geofence
- [x] `SimulateRequest` — API request body for `/simulate` endpoint

### 1.3 API Surface
- [x] `GET /` and `GET /health` — System health check
- [x] `GET /incidents` — Retrieve all detected incidents
- [x] `GET /alerts` — Retrieve all generated alerts
- [x] `GET /traces` — Retrieve agent reasoning traces
- [x] `POST /simulate` — Trigger full pipeline simulation
- [x] `GET /live-status` — Agent and system status polling
- [x] `WS /ws/live-trace` — Real-time reasoning stream

### 1.4 Multi-Agent Pipeline
- [x] `SifterAgent` — Signal ingestion, Roman Urdu parsing, severity scoring
- [x] `StrategistAgent` — Cross-validation, population estimation, rerouting
- [x] `ValidatorGate` — Structural safety gate (false alarm, contradiction, weak signal)
- [x] `CommanderAgent` — Alert generation, ticket dispatch, geofence creation
- [x] `FloodOrchestrator` — Sequential pipeline coordinator with retry logic

### 1.5 Tool Modules
- [x] `weather_tool.py` — Meteosource API with fallback JSON
- [x] `traffic_tool.py` — TomTom API with fallback congestion mapping
- [x] `social_signal_tool.py` — Roman Urdu NLP parsing with mock post generation
- [x] `geofence_tool.py` — Geographic impact zone calculation
- [x] `reroute_tool.py` — Alternative route generation and delay estimation
- [x] `alert_tool.py` — Alert object creation and emergency ticket generation

### 1.6 Storage Layer
- [x] Firebase Firestore integration (`services/firestore_service.py`)
- [x] In-memory `_mem_store` fallback for offline/simulation mode
- [x] Dual-write pattern: attempt Firestore, fallback silently to memory
- [x] Database ID configuration via `FIREBASE_DATABASE_ID` env var

### 1.7 WebSocket Service
- [x] `WebSocketManager` class for connection management
- [x] Broadcast methods: `broadcast_trace`, `broadcast_incident`, `broadcast_alert`, `broadcast_status`
- [x] Connection lifecycle handling (connect/disconnect)

---

## Phase 2: Frontend (Mobile-First Command Dashboard)

### 2.1 Dashboard Structure
- [x] Single-page application in `static/index.html`
- [x] 5-screen navigation: Map, Agent Trace, Before/After, KPI, Alerts
- [x] Mobile-optimized viewport (390×844 device frame)
- [x] Dark theme with military/ops aesthetic (CSS custom properties)

### 2.2 Real-Time Features
- [x] WebSocket client connecting to `/ws/live-trace`
- [x] Color-coded agent trace rows (Sifter=blue, Strategist=orange, Validator=purple, Commander=green)
- [x] Live status bar with blinking indicator
- [x] Google Maps integration with dynamic marker placement

### 2.3 Demo Capabilities
- [x] Offline simulation engine with 3 pre-built scenarios
- [x] Demo scenario buttons: Confirmed Flood, False Alarm, Missing Telemetry
- [x] Network status badge (ONLINE/OFFLINE detection)
- [x] Source badges (REAL/MOCK) on every API response
- [x] Result overlay with safety labels and scorecard

### 2.4 UI Polish
- [x] Google Fonts: Orbitron (headings), Rajdhani (body), Share Tech Mono (terminal)
- [x] CSS animations for status transitions
- [x] Karachi timezone clock (PKT, UTC+5)
- [x] Bottom navigation with active state indicators

---

## Phase 3: Safety Layer (ValidatorGate)

### 3.1 Validation Rules
- [x] **Confirmed flood:** Social score > 0.5 AND rainfall ≥ 10mm → `validated: true`
- [x] **Contradiction:** Social score > 0.5 AND rainfall == 0mm → `requires_operator_review`
- [x] **Weak signal:** Social score ≤ 0.5 AND rainfall < 10mm → `requires_operator_review`
- [x] **Heatwave false alarm:** Social crisis + temperature < 35°C → `False Alarm`
- [x] **Fallback mode:** Simulated telemetry detected → `fallback_mode: true`

### 3.2 Safety Guarantees
- [x] No physical dispatch without dual-source confirmation
- [x] All actions labeled as "simulated" requiring operator approval
- [x] Gemini responses wrapped in try/catch with deterministic fallback
- [x] Pipeline retry with exponential backoff (up to 3 attempts)

---

## Phase 4: Mobile Packaging (Capacitor)

- [x] `capacitor.config.json` — App ID, web directory, cleartext config
- [x] `package.json` — Capacitor core + Android platform
- [x] `MOBILE_INSTALL.md` — Build instructions
- [x] Emulator bridge: `10.0.2.2` for local backend connectivity
- [ ] APK build — Requires Android Studio (pending team build station)

---

## Phase 5: Evidence Generation

- [x] 12+ JSON evidence files under `docs/evidence/`
- [x] Health check, simulate, false positive, weak signal, contradiction responses
- [x] Missing telemetry fallback evidence
- [x] Firestore schema sample
- [x] Cost/latency/scaling documentation
- [x] Screenshot checklist
- [x] Mobile app proof

---

## Phase 6: Documentation & Submission

- [x] `README.md` — 21-section judge-ready documentation
- [x] Antigravity Trace Pack (10 documents)
- [x] Team usage logs (4 documents)
- [x] Demo video script + shotlist
- [x] Antigravity usage video script + shotlist
- [x] Submission form answer drafts
- [x] Final submission checklist

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                    FastAPI Server                     │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ REST API │  │ WS API   │  │ Static Files      │  │
│  │ routes.py│  │websocket │  │ index.html (SPA)  │  │
│  └────┬─────┘  └────┬─────┘  └───────────────────┘  │
│       │              │                                │
│  ┌────▼──────────────▼──────────────────────────┐    │
│  │           FloodOrchestrator                   │    │
│  │  ┌────────┐ ┌───────────┐ ┌───────────────┐  │    │
│  │  │ Sifter │→│Strategist │→│ ValidatorGate │  │    │
│  │  └────────┘ └───────────┘ └───────┬───────┘  │    │
│  │                                    │          │    │
│  │                           ┌────────▼───────┐  │    │
│  │                           │   Commander    │  │    │
│  │                           └────────────────┘  │    │
│  └───────────────────────────────────────────────┘    │
│       │                                               │
│  ┌────▼───────────────────────────────────────┐      │
│  │     Firestore (prod) / _mem_store (demo)    │      │
│  └─────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

---

## Risk Mitigation

| Risk | Mitigation |
|---|---|
| Gemini API rate limits during demo | Deterministic fallback in every agent |
| Firestore connection failure | In-memory `_mem_store` with identical API |
| Weather/Traffic API unavailable | Hardcoded fallback JSON payloads in tool modules |
| Network unavailable during judging | Offline demo mode with pre-built scenarios |
| Mobile build failure | Web dashboard works standalone in any browser |
