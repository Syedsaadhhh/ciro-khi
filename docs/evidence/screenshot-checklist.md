# CIRO — Screenshot Checklist for Hackathon Submission

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Last Updated: 2026-05-20 (v2 — post UI polish pass)

---

## Required Screenshots

Capture each screenshot at **1920×1080** or higher resolution. Use **PNG** format. Name files with the prefix `screenshot-NN-` followed by a descriptive name.

---

| # | Screenshot | Description | Filename | Status |
|---|-----------|-------------|----------|--------|
| 1 | **Health Endpoint** | Browser or Postman showing `GET /health` returning 200 OK with full JSON response | `screenshot-01-health-endpoint.png` | ☐ Pending |
| 2 | **Simulate Request** | Postman or curl showing `POST /simulate` with University Road flood payload and successful response | `screenshot-02-simulate-request.png` | ☐ Pending |
| 3 | **Confirmed Flood Response** | Full JSON response body for a confirmed flood scenario showing severity 8.8, confidence 0.96 | `screenshot-03-confirmed-flood.png` | ☐ Pending |
| 4 | **Live Trace WebSocket** | Frontend or WebSocket client showing real-time agent trace messages flowing through all 4 stages | `screenshot-04-live-trace.png` | ☐ Pending |
| 5 | **Firestore Console** | Firebase Console showing the `cirokhi` database with incidents collection and a sample document | `screenshot-05-firestore-console.png` | ☐ Pending |
| 6 | **ValidatorGate Rejection** | Response showing a false positive caught by ValidatorGate with `rejected_by_validator` status | `screenshot-06-validator-rejection.png` | ☐ Pending |
| 7 | **Mobile Dashboard** | Mobile browser (Chrome DevTools device mode or physical device) showing the CIRO dashboard with incident cards | `screenshot-07-mobile-dashboard.png` | ☐ Pending |
| 8 | **Offline Demo Mode** | Mobile app or PWA showing the offline demo mode badge and simulated incident data without network | `screenshot-08-offline-demo.png` | ☐ Pending |
| 9 | **Multi-Crisis View** | Dashboard or API response showing two simultaneous incidents with resource allocation split | `screenshot-09-multi-crisis.png` | ☐ Pending |
| 10 | **Error Fallback** | Response showing Gemini API rate limit error with fallback mode activated and operator notification | `screenshot-10-error-fallback.png` | ☐ Pending |
| 11 | **Collapsible Tray Collapsed** | Screen 1 with tray in default collapsed state showing 🔴 2 ACTIVE / ✓ 1 RESOLVED pills | `screenshot-11-tray-collapsed.png` | ☐ Pending |
| 12 | **Collapsible Tray Expanded** | Tray expanded showing ALL / ACTIVE / REVIEW / RESOLVED tab row and all 3 incident rows | `screenshot-12-tray-expanded.png` | ☐ Pending |
| 13 | **Zoom In / Zoom Out** | Map zoomed in (ZOOM badge visible in corner) and custom +/– buttons highlighted | `screenshot-13-map-zoom.png` | ☐ Pending |
| 14 | **Satellite Toggle** | Map in satellite mode (🛰️ SATELLITE MODE toast) vs roadmap mode | `screenshot-14-satellite-toggle.png` | ☐ Pending |
| 15 | **Google Maps Attribution** | Confirm Google Maps attribution, Terms, and map data labels are visible and not covered by overlays | `screenshot-15-maps-attribution.png` | ☐ Pending |
| 16 | **Dispatch Progress Bar** | Progress bar showing staged agent steps (SIFTER → STRATEGIST → VALIDATOR → COMMANDER) illuminating in sequence during dispatch | `screenshot-16-dispatch-progress.png` | ☐ Pending |
| 17 | **Fallback Demo Label** | `⚠ LIVE API DELAY — FALLBACK DEMO MODE` label visible when backend times out after 8s | `screenshot-17-fallback-label.png` | ☐ Pending |

---

## Manual Verification Steps

Run these steps in order before final submission. Mark each ☑ when confirmed.

### Task 1 — Google Map Controls

1. **Open** `http://localhost:8000` with Chrome DevTools in iPhone 12 Pro mode
2. **Confirm** Google Maps renders (Karachi visible with dark theme)
3. **Confirm** Google attribution / Terms / Map data text is visible at bottom of map
4. [ ] Click **+** zoom button → map zooms in one step, ZOOM badge appears briefly
5. [ ] Click **−** zoom button → map zooms out one step, ZOOM badge appears briefly
6. [ ] Click **🛰️** satellite button → map switches to satellite imagery, `🛰️ SATELLITE MODE` toast appears
7. [ ] Click **🛰️** again → returns to roadmap, `🗺️ STANDARD MODE` toast appears
8. [ ] Confirm zoom/satellite buttons have `pointer-events: auto` (visible and clickable, not blocked by overlays)
9. [ ] Confirm Google attribution remains visible in both roadmap and satellite mode

### Task 2 — Collapsible Incident Tray

1. **Open** Screen 1 (MAP tab)
2. [ ] Confirm tray handle is visible at bottom showing pills: `🔴 2 ACTIVE` and `✓ 1 RESOLVED`
3. [ ] Confirm **map is fully visible above the tray** — no incident rows blocking the map by default
4. [ ] Tap the tray handle → tray expands with smooth slide animation
5. [ ] Confirm tray shows ALL/ACTIVE/REVIEW/RESOLVED tabs and 3 incident rows
6. [ ] Confirm tray height does **not** exceed ~45% of the phone viewport
7. [ ] Click **ACTIVE** tab → only IIC + UNIV rows shown, DHA hidden
8. [ ] Click **RESOLVED** tab → only DHA shown
9. [ ] Click **ALL** → all 3 rows visible
10. [ ] Click tray handle again → tray collapses back
11. [ ] Open modal for IIC, click **MARK AS RESOLVED** → tray pill updates to `🔴 1 ACTIVE / ✓ 2 RESOLVED`

### Task 3 — Dispatch Perceived Speed

1. **Click** `🌊 CONFIRMED FLOOD` demo button
2. **Click** `⚡ LAUNCH DISPATCH`
3. [ ] Confirm progress bar appears **immediately** below the button
4. [ ] Confirm `SIFTER` lights green first (within 0.5s)
5. [ ] Confirm `STRATEGIST` lights at ~1.2s, `VALIDATOR` at ~2.8s, `COMMANDER` at ~4.5s
6. [ ] Confirm result overlay or offline sim completes by ~5–6s total
7. [ ] Confirm progress bar disappears after result loads
8. [ ] **With backend running**: dispatch completes with real response before 8s timeout
9. [ ] **To test timeout**: temporarily point to wrong port → after 8s see `⚠ LIVE API DELAY — FALLBACK DEMO MODE` label + offline sim fires

### Task 4 — Demo Scenarios (no regression)

| Scenario | Button | Expected Result | Status |
|---|---|---|---|
| Confirmed Flood | 🌊 CONFIRMED FLOOD | `● CONFIRMED FLOOD` green chip, severity 8.8+, resource panel shows pumps | ☐ |
| False Alarm | ⊘ FALSE ALARM | `✕ FALSE ALARM` red chip, no dispatch action | ☐ |
| Missing Telemetry | 📡 MISSING TELEMETRY | `◐ MOCK FALLBACK` purple chip, fallback mode badge | ☐ |
| Multi-Crisis | ⚠ MULTI-CRISIS | `⚠ OPERATOR REVIEW` orange chip, review panel | ☐ |

---

## Screenshot Guidelines

1. **Remove or blur** any API keys, tokens, or credentials visible in the UI
2. **Use consistent timestamps** — Karachi time (`Asia/Karachi`) auto-synced by the clock
3. **Highlight key fields** with red boxes or arrows if submitting annotated versions
4. **Include the URL bar** in browser screenshots to show the endpoint
5. **Dark mode only** — CIRO uses a fixed dark cyberpunk theme
6. **Mobile screenshots** should show the device frame if using DevTools emulation

---

## Capture Priority

If time is limited, prioritize in this order:

1. Screenshot 2 (Simulate Request) — proves the core flow works
2. Screenshot 4 (Live Trace) — shows real-time agent coordination
3. Screenshot 5 (Firestore) — proves data persistence
4. Screenshot 7 (Mobile Dashboard) — proves mobile support
5. Screenshot 11+12 (Tray) — shows judge-facing UI improvement
6. Screenshot 16 (Dispatch Progress) — shows immediate perceived response
7. Screenshot 6 (Validator Rejection) — proves safety layer works
8. Screenshot 15 (Maps Attribution) — Google compliance proof

---

*All screenshots should be saved to `docs/evidence/screenshots/` directory.*
