# CIRO — Screenshot Checklist for Hackathon Submission

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Last Updated: 2026-05-20

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

---

## Screenshot Guidelines

1. **Remove or blur** any API keys, tokens, or credentials visible in the UI
2. **Use consistent timestamps** — ideally `2026-05-20T02:30:00Z` range for cohesion
3. **Highlight key fields** with red boxes or arrows if submitting annotated versions
4. **Include the URL bar** in browser screenshots to show the endpoint
5. **Dark mode preferred** if the UI supports it — better contrast for presentation
6. **Mobile screenshots** should show the device frame if using DevTools emulation

---

## Capture Priority

If time is limited, prioritize in this order:

1. Screenshot 2 (Simulate Request) — proves the core flow works
2. Screenshot 4 (Live Trace) — shows real-time agent coordination
3. Screenshot 5 (Firestore) — proves data persistence
4. Screenshot 7 (Mobile Dashboard) — proves mobile support
5. Screenshot 6 (Validator Rejection) — proves safety layer works

---

*All screenshots should be saved to `docs/evidence/screenshots/` directory.*
