# CIRO Mobile — Test Checklist

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Mobile Test Matrix  
> Version: 2.1.0  
> Last Updated: 2026-05-20

---

## Test Environment

| Property | Value |
|----------|-------|
| Backend | FastAPI on `http://localhost:8000` |
| Firestore | Database ID: `cirokhi` |
| Frontend | React / PWA served via development server |
| Test date | 2026-05-20 |

---

## Test Matrix

| # | Test | Environment | Expected Result | Status |
|---|------|------------|-----------------|--------|
| 1 | Dashboard loads with incident cards | Chrome Desktop (1920×1080) | Dashboard renders, incident cards populate from Firestore | ☐ Pending |
| 2 | POST /simulate returns confirmed flood | Chrome Desktop — Postman/fetch | JSON response with status=confirmed, severity 8.8 | ☐ Pending |
| 3 | Live trace WebSocket streams events | Chrome Desktop — ws://localhost:8000/ws/live-trace | 4-stage agent trace events stream in real time | ☐ Pending |
| 4 | Mobile responsive layout | Chrome DevTools — iPhone 14 Pro (393×852) | UI adapts to mobile viewport, no horizontal scroll, cards stack vertically | ☐ Pending |
| 5 | Mobile responsive layout | Chrome DevTools — Samsung Galaxy S21 (360×800) | Same as above, tested on Android viewport | ☐ Pending |
| 6 | Incognito mode — no cached state | Chrome Incognito (Desktop) | App loads fresh, fetches data from backend, no stale cache artifacts | ☐ Pending |
| 7 | Incognito mode — mobile viewport | Chrome Incognito — iPhone 14 Pro viewport | Same as #6 but in mobile layout | ☐ Pending |
| 8 | Airplane mode — offline demo activates | Chrome DevTools — Network: Offline | Network mode badge shows 🔴 OFFLINE DEMO, pre-loaded scenarios visible | ☐ Pending |
| 9 | Airplane mode → reconnect | Chrome DevTools — Offline → Online | Badge transitions from 🔴 OFFLINE DEMO → 🟢 LIVE within 30 seconds | ☐ Pending |
| 10 | Android Emulator — local backend | Android Emulator (API 33) — http://10.0.2.2:8000 | App connects via emulator localhost proxy, badge shows 🟡 LOCAL | ☐ Pending |
| 11 | Android Emulator — no backend | Android Emulator (API 33) — backend stopped | App falls back to OFFLINE DEMO or MOCK mode | ☐ Pending |
| 12 | Physical Android device — WiFi | Physical device on same WiFi as dev machine | App connects to local backend via IP, badge shows 🟡 LOCAL | ☐ Pending |
| 13 | Physical Android device — mobile data | Physical device on cellular data | App attempts deployed backend; if unavailable, shows MOCK or OFFLINE | ☐ Pending |
| 14 | Physical Android device — APK install | Install APK via `adb install` | APK installs cleanly, app launches, no crash on startup | ☐ Pending |
| 15 | Simulate confirmed flood — mobile | Physical device or emulator, mobile browser | Full pipeline executes, response displays correctly in mobile layout | ☐ Pending |
| 16 | Simulate weak signal — mobile | Physical device or emulator | Response shows no_incident status, no alert generated | ☐ Pending |
| 17 | Simulate false positive — mobile | Physical device or emulator | Response shows rejected_by_validator, ValidatorGate catches it | ☐ Pending |
| 18 | Trace viewer — mobile scroll | Physical device, trace viewer panel | Trace events scroll smoothly, timestamps readable, no layout overflow | ☐ Pending |
| 19 | Geofence map renders — mobile | Physical device, incident detail view | Map component renders with geofence circle overlay at correct coordinates | ☐ Pending |
| 20 | Error state — Gemini rate limit | Trigger rate limit (15+ requests/min) | Error response shown, fallback mode badge appears, operator notified | ☐ Pending |

---

## Device Test Coverage

| Device / Environment | Type | OS | Browser | Tested |
|---------------------|------|------|---------|--------|
| Chrome Desktop | Emulated | Windows 11 | Chrome 126 | ☐ |
| Chrome DevTools — iPhone 14 Pro | Emulated | iOS 17 | Chrome 126 (emulated) | ☐ |
| Chrome DevTools — Galaxy S21 | Emulated | Android 13 | Chrome 126 (emulated) | ☐ |
| Chrome Incognito | Emulated | Windows 11 | Chrome 126 | ☐ |
| Android Emulator | Emulated | Android 13 (API 33) | Chrome / WebView | ☐ |
| Physical Android Device | Physical | Android 12+ | Chrome Mobile | ☐ |
| Physical iPhone (if available) | Physical | iOS 16+ | Safari Mobile | ☐ |

---

## Known Limitations

- **iOS testing** requires a physical device or macOS with Xcode — not available in current setup
- **Capacitor native features** (camera, GPS) are not tested in browser emulation
- **WebSocket in emulator** may require explicit `10.0.2.2` proxy configuration
- **APK builds** require Android Studio with SDK 33+ installed locally

---

## How to Run Tests

1. **Start backend:** `uvicorn main:app --host 0.0.0.0 --port 8000`
2. **Start frontend:** `npm run dev` (or `ionic serve` for Capacitor builds)
3. **For emulator:** Launch Android Emulator from Android Studio
4. **For physical device:** Enable USB debugging, connect via USB, run `adb install app-debug.apk`
5. **For offline tests:** Use Chrome DevTools → Network tab → check "Offline"

---

*CIRO is a production-oriented prototype. This test matrix covers demonstration-critical scenarios.*
