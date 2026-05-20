# CIRO — One-Page Project Summary

> **Challenge:** AISeekho 2026, Challenge 3 — Crisis Management
> **Team:** Syed Muhammad Saad (Lead), Farheen, Arisha, Areeba
> **Built With:** Google Antigravity + Google Gemini

---

## What Is CIRO?

**CIRO (Crisis Intelligence & Response Orchestrator)** is a production-oriented prototype that manages urban flood crises in Karachi, Pakistan. It processes Roman Urdu social media signals, fuses them with real-time weather and traffic telemetry, validates through a safety gate, and generates coordinated emergency response recommendations — all in under 6 seconds.

---

## How It Works

```
Social Post (Roman Urdu) + Weather API + Traffic API
        ↓
   [SIFTER AGENT] — Parses signals, detects crisis, scores severity
        ↓
   [STRATEGIST AGENT] — Cross-validates, estimates population, generates routes
        ↓
   [VALIDATOR GATE] — Catches false alarms, contradictions, weak signals
        ↓
   [COMMANDER AGENT] — Generates alerts, dispatches resources, creates geofence
        ↓
   Dashboard + WebSocket → Real-time mobile command center
```

---

## Key Differentiators

| Feature | What It Does |
|---|---|
| **Roman Urdu NLP** | Parses social media posts in Pakistan's dominant informal language |
| **Multi-Signal Fusion** | Combines social, weather, and traffic data — never trusts a single source |
| **ValidatorGate** | Deterministic safety layer that catches false alarms before dispatch |
| **Dual-Mode Agents** | Every agent works with Gemini AI or deterministic fallback |
| **Offline Demo Mode** | Pre-built scenarios work without network — demo never fails |
| **$0 Operating Cost** | Runs entirely on free tiers (Firebase Spark + Gemini) |

---

## Technical Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) with async lifecycle |
| AI Engine | Google Gemini 3 Flash-Preview (4 agents) |
| Database | Firebase Firestore (production) / In-memory dict (demo) |
| Real-time | WebSocket live trace streaming |
| Frontend | HTML/CSS/JS SPA with military ops aesthetic |
| Mobile | CapacitorJS → Android APK |
| APIs | Meteosource (weather), TomTom (traffic) |
| Orchestrator | Google Antigravity |

---

## Safety Features

- **False alarm rejection** — Social panic + no rain = auto-flagged
- **Contradiction detection** — Social vs telemetry mismatch = operator review
- **Weak signal handling** — Ambiguous data = requires human review
- **No autonomous dispatch** — All physical actions require operator approval
- **Fallback mode** — API failures trigger cached data with MOCK labels

---

## Numbers

| Metric | Value |
|---|---|
| Pipeline latency | ~200ms (deterministic) / ~5.5s (Gemini) |
| Agents | 4 (3 Gemini-capable + 1 deterministic gate) |
| API endpoints | 7 REST + 1 WebSocket |
| Source files | 18 Python + 1 HTML (3,900 lines) |
| Evidence files | 20+ JSON/Markdown |
| Development tasks | 110/111 complete |
| Operating cost | $0.00 |

---

## Antigravity Role

Google Antigravity served as the **principal development orchestrator** — designing architecture, generating code, implementing safety logic, building the dashboard, creating evidence, and authoring documentation. See the Antigravity Trace Pack (14 files) for complete evidence.

---

## Team

| Member | Role | Primary Contribution |
|---|---|---|
| **Syed Muhammad Saad** | Team Lead & Cloud Architect | Backend, Firestore, deployment |
| **Farheen** | Lead AI Core Engineer | Agent pipeline, Gemini integration |
| **Arisha** | Lead UI/UX Designer | Dashboard, mobile, animations |
| **Areeba** | Technical Communications Lead | README, evidence pack, documentation |
