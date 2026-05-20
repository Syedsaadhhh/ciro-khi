# CIRO Mobile — Network Mode Detection & Offline Operation

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Mobile Network Mode Documentation  
> Version: 2.1.0  
> Last Updated: 2026-05-20

---

## Overview

The CIRO mobile client supports **four network modes** to ensure the application remains functional and demonstrable across all connectivity conditions — from full cloud connectivity to complete offline operation. The mode is auto-detected on launch and can transition dynamically during use.

---

## Network Modes

### 1. 🟢 LIVE Mode

**Badge:** Green  
**Label:** `LIVE`  
**Description:** Full connectivity to the deployed CIRO backend.

| Property | Value |
|----------|-------|
| Backend connection | ✅ Connected to FastAPI server on deployed URL |
| Firestore | ✅ Live reads via Firestore SDK |
| WebSocket | ✅ Real-time traces via `/ws/live-trace` |
| Gemini API | ✅ Live LLM-powered analysis |
| Data source | Production Firestore (`cirokhi` database) |

**When activated:** Device has internet access AND the deployed backend is reachable AND responds to `/health` with `status: "ok"`.

---

### 2. 🟡 LOCAL Mode

**Badge:** Yellow  
**Label:** `LOCAL`  
**Description:** Connected to a locally running development backend.

| Property | Value |
|----------|-------|
| Backend connection | ✅ Connected to `http://<local-ip>:8000` |
| Firestore | ✅ Live reads (if Firebase credentials configured) |
| WebSocket | ✅ Real-time traces on local network |
| Gemini API | ✅ If API key is configured on the local server |
| Data source | Local Firestore or emulator |

**When activated:** Device is on the same local network as the development machine. Smart host detection probes common local addresses (`localhost`, `10.0.2.2` for Android emulator, `192.168.x.x` for local network).

**Detection logic:**
```
1. Try deployed backend URL → if reachable, use LIVE mode
2. Try http://10.0.2.2:8000/health → (Android emulator localhost)
3. Try http://192.168.x.x:8000/health → (local network discovery)
4. If any local responds, use LOCAL mode
5. If none respond, fall through to OFFLINE DEMO or MOCK FALLBACK
```

---

### 3. 🔴 OFFLINE DEMO Mode

**Badge:** Red  
**Label:** `OFFLINE DEMO`  
**Description:** No network connectivity. Uses a fully self-contained offline simulation engine with pre-built scenarios.

| Property | Value |
|----------|-------|
| Backend connection | ❌ No backend required |
| Firestore | ❌ No Firestore access |
| WebSocket | ❌ Simulated trace playback |
| Gemini API | ❌ Not available |
| Data source | Bundled JSON scenario files |

**When activated:** Device has no internet AND no local backend is reachable. Also manually selectable via settings.

**Offline simulation engine:**
- Pre-loaded with 5 representative scenarios:
  1. Confirmed flood (University Road)
  2. Weak signal / no incident (Saddar)
  3. False positive caught by ValidatorGate (Clifton)
  4. Contradiction requiring operator review (Malir)
  5. Multi-crisis resource conflict (University Road + Korangi)
- Trace playback simulates real-time agent processing with realistic delays
- All data is read-only — no writes to any backend
- Timestamps are generated relative to the current device time

---

### 4. ⚪ MOCK FALLBACK Mode

**Badge:** Gray  
**Label:** `MOCK`  
**Description:** Network is available but the backend is unresponsive or returning errors. Uses mock API responses.

| Property | Value |
|----------|-------|
| Backend connection | ⚠️ Network available but backend unreachable or erroring |
| Firestore | ⚠️ May have partial access |
| WebSocket | ❌ Not available |
| Gemini API | ❌ Not available |
| Data source | Generated mock responses matching API schema |

**When activated:** Device has internet BUT the backend `/health` check fails (timeout, 5xx, DNS failure).

**Behavior:**
- POST `/simulate` calls return pre-generated mock responses
- Mock responses follow the exact same schema as real responses
- A warning banner is shown: "Backend unavailable — showing mock data"
- Automatically retries backend connection every 30 seconds
- Transitions to LIVE or LOCAL mode once backend becomes available

---

## Mode Detection Flow

```
┌─────────────────────────────┐
│     App Launch / Resume     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   Check network available?  │
└──────┬──────────┬───────────┘
       │ Yes      │ No
       ▼          ▼
┌──────────┐  ┌───────────────┐
│ Probe    │  │ OFFLINE DEMO  │
│ backends │  │ 🔴            │
└──┬───────┘  └───────────────┘
   │
   ▼
┌─────────────────────────────┐
│ Try deployed backend /health│
└──────┬──────────┬───────────┘
       │ 200 OK   │ Failed
       ▼          ▼
┌──────────┐  ┌───────────────────┐
│  LIVE    │  │ Try local backends│
│  🟢     │  └──┬────────┬───────┘
└──────────┘     │ Found  │ None
                 ▼        ▼
          ┌──────────┐ ┌───────────┐
          │  LOCAL   │ │ MOCK      │
          │  🟡     │ │ FALLBACK  │
          └──────────┘ │ ⚪       │
                       └───────────┘
```

---

## Badge Display

The network mode badge is displayed in the **top-right corner** of the mobile header bar, always visible to the user.

| Mode | Badge Color | Text | Background |
|------|------------|------|------------|
| LIVE | 🟢 Green | `LIVE` | `#22c55e` / `rgba(34, 197, 94, 0.15)` |
| LOCAL | 🟡 Yellow | `LOCAL` | `#eab308` / `rgba(234, 179, 8, 0.15)` |
| OFFLINE DEMO | 🔴 Red | `OFFLINE DEMO` | `#ef4444` / `rgba(239, 68, 68, 0.15)` |
| MOCK FALLBACK | ⚪ Gray | `MOCK` | `#6b7280` / `rgba(107, 114, 128, 0.15)` |

**Badge behavior:**
- Pulses briefly when mode transitions
- Tappable — shows a tooltip with mode details and connection info
- Updates automatically when connectivity changes

---

## Offline Simulation Engine — Technical Details

The offline simulation engine is a self-contained JavaScript module bundled with the mobile app:

1. **Scenario files** are stored as JSON in `assets/scenarios/`
2. **Trace playback** uses `setTimeout` chains to simulate agent processing delays
3. **Severity/confidence values** are pre-computed and stored in scenario files
4. **No network calls** are made in offline mode — all data is local
5. **Scenario selection** is driven by user input (location dropdown + signal type)
6. **Timestamps** are dynamically generated relative to device clock
7. **Total bundle size** for all offline scenarios: ~45 KB

---

*CIRO is a production-oriented prototype. Network mode detection is designed for demonstration and development use.*
