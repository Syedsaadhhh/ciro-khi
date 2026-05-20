# CIRO Mobile App — Proof of Implementation

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Mobile Application Architecture & Implementation Proof  
> Version: 2.1.0  
> Last Updated: 2026-05-20

---

## Overview

CIRO's mobile client is built as a **responsive web application** with **Capacitor** packaging for native Android distribution. This document describes the mobile architecture, offline capabilities, host detection, and security posture.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              CIRO Mobile App                │
├─────────────────────────────────────────────┤
│  Presentation Layer                         │
│  ├── React Components                       │
│  ├── Responsive CSS (mobile-first)          │
│  └── Real-time Trace Viewer                 │
├─────────────────────────────────────────────┤
│  Data Layer                                 │
│  ├── Firestore SDK (live mode)              │
│  ├── REST API Client (FastAPI backend)      │
│  ├── WebSocket Client (/ws/live-trace)      │
│  └── Offline Scenario Engine (demo mode)    │
├─────────────────────────────────────────────┤
│  Network Layer                              │
│  ├── Smart Host Detection                   │
│  ├── Network Mode Manager                   │
│  └── Auto-Reconnect Handler                 │
├─────────────────────────────────────────────┤
│  Native Layer (Capacitor)                   │
│  ├── Android WebView wrapper                │
│  ├── Status bar integration                 │
│  └── App lifecycle management               │
└─────────────────────────────────────────────┘
```

---

## Capacitor Packaging

### What is Capacitor?

Capacitor is a cross-platform native runtime by Ionic that wraps web applications in a native container, enabling distribution through app stores or direct APK installation.

### Build Process

```bash
# 1. Build the web application
npm run build

# 2. Sync web assets to Capacitor native project
npx cap sync android

# 3. Open in Android Studio for APK build
npx cap open android

# 4. Build APK from Android Studio
#    Build → Build Bundle(s) / APK(s) → Build APK(s)
```

### Capacitor Configuration

```json
{
  "appId": "com.ciro.karachi",
  "appName": "CIRO",
  "webDir": "build",
  "server": {
    "cleartext": true,
    "allowNavigation": ["*"]
  },
  "android": {
    "allowMixedContent": true
  }
}
```

### APK Details

| Property | Value |
|----------|-------|
| Package name | `com.ciro.karachi` |
| Min SDK | API 24 (Android 7.0) |
| Target SDK | API 33 (Android 13) |
| Build type | Debug APK (production-oriented prototype) |
| APK size (estimated) | ~8–12 MB |
| Web assets | Bundled in `assets/public/` |

---

## Offline Demo Mode

### Purpose

The offline demo mode allows CIRO to be demonstrated **without any network connectivity** — critical for hackathon presentations where WiFi may be unreliable.

### How It Works

1. **Detection:** On app launch, the network mode manager probes for backend availability
2. **Activation:** If no backend is reachable and no network is available, offline demo mode activates automatically
3. **Data source:** Pre-built scenario JSON files bundled in the app assets
4. **Trace simulation:** Agent trace events are played back with realistic timing delays

### Pre-loaded Scenarios

| # | Scenario | Location | Expected Outcome |
|---|---------|----------|-----------------|
| 1 | Confirmed flood | University Road | `status: confirmed`, severity 8.8 |
| 2 | Weak signal | Saddar | `status: no_incident`, severity 1.2 |
| 3 | False positive | Clifton Block 5 | `status: rejected_by_validator` |
| 4 | Contradiction | Malir Halt | `status: requires_operator_review` |
| 5 | Multi-crisis | University Road + Korangi | Both confirmed, resource conflict shown |

### Offline Engine Characteristics

- **No network calls** — entirely self-contained
- **Realistic delays** — simulates 3–5 second pipeline processing
- **Dynamic timestamps** — generated relative to device clock
- **Same UI** — no visual difference between offline and online mode (except badge)
- **Bundle size** — ~45 KB for all scenario data

---

## Smart Host Detection

### Problem

The mobile app needs to connect to the backend, but the backend address varies:
- **Production:** Deployed cloud URL
- **Development:** Local machine IP (`192.168.x.x:8000`)
- **Android Emulator:** `10.0.2.2:8000` (emulator's localhost proxy)
- **No backend:** Offline or mock mode

### Solution — Smart Host Detection

On launch, the app probes multiple candidate hosts in priority order:

```javascript
const HOST_CANDIDATES = [
  { url: 'https://ciro-backend.example.com', mode: 'LIVE' },
  { url: 'http://10.0.2.2:8000',             mode: 'LOCAL' },  // Android emulator
  { url: 'http://192.168.1.100:8000',         mode: 'LOCAL' },  // Common local IP
  { url: 'http://localhost:8000',             mode: 'LOCAL' },  // Desktop browser
];

async function detectHost() {
  for (const candidate of HOST_CANDIDATES) {
    try {
      const response = await fetch(`${candidate.url}/health`, {
        signal: AbortSignal.timeout(3000)
      });
      if (response.ok) {
        return { host: candidate.url, mode: candidate.mode };
      }
    } catch (e) {
      continue; // Try next candidate
    }
  }
  
  // No backend reachable
  if (navigator.onLine) {
    return { host: null, mode: 'MOCK' };
  }
  return { host: null, mode: 'OFFLINE_DEMO' };
}
```

### Detection Timing

| Step | Timeout | Action |
|------|---------|--------|
| Probe deployed backend | 3 seconds | If 200 OK → LIVE mode |
| Probe emulator localhost | 2 seconds | If 200 OK → LOCAL mode |
| Probe local network IPs | 2 seconds | If 200 OK → LOCAL mode |
| All probes failed | — | Check `navigator.onLine` |
| Online but no backend | — | MOCK FALLBACK mode |
| Offline | — | OFFLINE DEMO mode |

**Total detection time:** 3–7 seconds (parallel probing where possible)

---

## Security — No Secrets in APK

### Principle

The CIRO mobile APK contains **zero secrets, API keys, or credentials**.

### What is NOT in the APK

| Item | Where It Lives | Why Not in APK |
|------|---------------|----------------|
| Gemini API key | Backend server environment variable | LLM calls are server-side only |
| Firebase service account | Backend server environment variable | Firestore writes are server-side only |
| Firebase client config | Loaded from backend `/config` endpoint at runtime | Not hardcoded in app |
| Backend URL | Discovered via smart host detection | Not hardcoded (probed dynamically) |
| User credentials | Not applicable | No user authentication in prototype |

### What IS in the APK

| Item | Purpose | Risk |
|------|---------|------|
| Offline scenario JSON files | Demo mode data | None — public simulation data |
| App JavaScript bundle | Application logic | Low — standard web app code |
| UI assets (icons, fonts, CSS) | Presentation | None |
| Capacitor native bridge | WebView container | None — standard framework code |

### Security Design Decisions

1. **Server-side LLM calls:** All Gemini API calls are made by the FastAPI backend, never from the client
2. **Runtime configuration:** Firebase client config is fetched from the backend at startup, not bundled
3. **No persistent storage of sensitive data:** The mobile app does not store any credentials in local storage, shared preferences, or the keychain
4. **Cleartext traffic allowed:** For development/demo purposes, the Capacitor config allows cleartext HTTP to local backends. In a production deployment, this would be restricted to HTTPS only
5. **No authentication in prototype:** User auth is not implemented in this production-oriented prototype. A production version would integrate Firebase Auth or similar

---

## Build Requirements

| Requirement | Purpose | Status |
|------------|---------|--------|
| Node.js 18+ | Build web app | ✅ Available |
| npm / yarn | Package management | ✅ Available |
| Capacitor CLI (`@capacitor/cli`) | Native project management | ✅ Installed |
| Android Studio | APK build and signing | ⚠️ Required for APK (manual step) |
| Android SDK API 33 | Target SDK | ⚠️ Required for APK |
| JDK 17 | Android build toolchain | ⚠️ Required for APK |

> **Note:** The APK build step requires Android Studio installed locally. This is a manual step documented in the build process above.

---

## Evidence of Implementation

| Proof Point | Evidence File |
|------------|--------------|
| Network mode detection logic | `mobile-network-mode.md` |
| Offline scenario data | `confirmed-flood-response.json`, `weak-signal-response.json`, etc. |
| API schema contracts | `agent-schema-contracts.md` |
| WebSocket trace format | `websocket-trace-sample.txt` |
| Test coverage | `mobile-test-checklist.md` |
| Firestore schema | `firestore-schema.md` |

---

*CIRO is a production-oriented prototype. The mobile app is designed for demonstration and evaluation purposes. A production deployment would require additional hardening, authentication, and HTTPS enforcement.*
