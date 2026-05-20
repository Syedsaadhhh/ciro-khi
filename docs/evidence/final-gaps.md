# CIRO — Known Gaps & Honest Limitations

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Honest Assessment of Current Gaps  
> Version: 2.1.0  
> Last Updated: 2026-05-20

---

## Overview

CIRO is a **production-oriented prototype** built for the hackathon. This document transparently lists known gaps, limitations, and items that would need to be addressed before any real-world deployment. We believe transparency about limitations is more valuable than hiding them.

---

## Gap 1: APK Build Requires Android Studio (Manual Step)

**Category:** Build & Distribution  
**Severity:** Low — does not affect functionality  

**Current state:** The mobile APK cannot be built from the command line alone. The build process requires:
- Android Studio installed locally
- Android SDK API 33+
- JDK 17+
- Manual build via `Build → Build APK(s)` in Android Studio

**Impact:** Team members without Android Studio cannot build the APK. The web app runs fully in any browser without this step.

**Mitigation:** A pre-built debug APK can be shared via Google Drive or direct transfer. CI/CD with GitHub Actions + Gradle could automate this in a production pipeline.

---

## Gap 2: Public Backend Deployment Pending

**Category:** Infrastructure  
**Severity:** Medium — affects demo accessibility  

**Current state:** The FastAPI backend runs on `localhost:8000` during development. A publicly accessible deployment (e.g., on Google Cloud Run, Railway, or Render) has not been completed.

**Impact:** External judges or testers cannot access the live backend without being on the same local network. The mobile app falls back to OFFLINE DEMO or MOCK mode when the backend is unreachable.

**Mitigation:**
- Offline demo mode provides a fully functional demonstration without a backend
- Local network demos work via smart host detection
- Cloud deployment is a straightforward `docker build` + `gcloud run deploy` step

---

## Gap 3: Real Google Weather/Traffic API Keys Needed for Live Mode

**Category:** Data Sources  
**Severity:** Medium — affects data realism  

**Current state:** CIRO uses **simulated weather and traffic APIs** that return configurable test data. Real Google Weather API and Google Maps Traffic API integrations are architected but not connected with live API keys.

**Impact:** All weather and traffic data in the prototype is simulated. The system cannot detect actual real-world conditions without live API keys.

**What would be needed:**
- Google Maps Platform API key with Weather and Routes API enabled
- Billing account linked (Weather API and Routes API are paid services)
- Rate limit monitoring (Weather API: ~1,000 calls/day free tier)

**Mitigation:** The simulation layer accurately represents the data schema and behavior of real APIs. The agent pipeline processes simulated data identically to how it would process real data. Swapping to real APIs requires only changing the data source adapter — no agent logic changes.

---

## Gap 4: Demo Video Recording Pending

**Category:** Submission Deliverables  
**Severity:** Medium — required for many hackathon submissions  

**Current state:** A polished demo video showing the full CIRO workflow has not been recorded yet.

**Required video content:**
1. Walkthrough of the simulation interface
2. Submitting a confirmed flood scenario
3. Real-time agent trace playing in the WebSocket viewer
4. ValidatorGate catching a false positive
5. Firestore console showing persisted data
6. Mobile responsive view
7. Offline demo mode activation

**Estimated recording time:** 3–5 minutes  
**Estimated editing time:** 1–2 hours

**Mitigation:** Screen recording can be done with OBS Studio or Loom. The offline demo mode ensures a reliable, repeatable recording session without backend dependency.

---

## Gap 5: 3rd-Party API Rate Limits in Production

**Category:** Scalability & Reliability  
**Severity:** High — affects production viability  

**Current state:** CIRO depends on several external APIs that have rate limits:

| API | Current Limit | Impact if Exceeded |
|-----|--------------|-------------------|
| Gemini 2.0 Flash | 15 RPM (free tier) | Falls back to deterministic analysis |
| Google Weather API | ~1,000 calls/day (free tier) | Weather telemetry unavailable |
| Google Routes/Traffic API | ~1,000 calls/day (free tier) | Traffic telemetry unavailable |
| Firestore | 50K reads/day (free tier) | Dashboard reads may fail |

**Impact in production:** During a real crisis, request volume could spike well beyond free-tier limits. Multiple simultaneous incidents would multiply API calls.

**Mitigation in prototype:**
- Gemini fallback to deterministic rule engine (already implemented)
- Missing telemetry fallback mode (already implemented)
- Operator notification when APIs are degraded (already implemented)

**Production requirements:**
- Paid API tiers for all external services
- Request caching/deduplication to reduce API calls
- Queue-based processing to smooth request spikes
- Monitoring and alerting for API quota usage

---

## Gap 6: No User Authentication

**Category:** Security  
**Severity:** Medium — acceptable for prototype, critical for production  

**Current state:** CIRO has no user authentication or authorization. Any user who can reach the backend can submit simulations and view all incidents.

**Production requirements:**
- Firebase Authentication for operator login
- Role-based access control (Operator, Admin, Viewer)
- Audit logging for all operator actions
- Session management and timeout

---

## Gap 7: Single-Region Deployment

**Category:** Infrastructure  
**Severity:** Low — acceptable for Karachi-only scope  

**Current state:** The system is designed for a single deployment region (Karachi). There is no multi-region failover, load balancing, or geographic distribution.

**Production requirements for scale:**
- Multi-region Firestore replication
- Load-balanced API instances
- CDN for static assets
- Health monitoring and auto-scaling

---

## Gap 8: No Automated Testing Suite

**Category:** Quality Assurance  
**Severity:** Medium — affects maintainability  

**Current state:** Testing is manual, guided by the test checklist (`mobile-test-checklist.md`). There are no automated unit tests, integration tests, or end-to-end tests.

**Production requirements:**
- Unit tests for each agent's logic
- Integration tests for the full pipeline
- End-to-end tests for API endpoints
- Load testing for concurrent request handling

---

## Gap 9: Hardcoded Karachi Geography

**Category:** Generalizability  
**Severity:** Low — by design for this hackathon  

**Current state:** Location parsing, coordinate ranges, route suggestions, and population density models are all hardcoded for Karachi. The system cannot be used for other cities without significant modification.

**Future extensibility:**
- Location data could be parameterized via configuration
- Route suggestions could use Google Maps Directions API
- Population models could be loaded from census data APIs
- Agent prompts could be templated for different cities

---

## Gap 10: Roman Urdu NLP Accuracy

**Category:** AI/ML  
**Severity:** Medium — affects core detection quality  

**Current state:** Roman Urdu parsing relies on Gemini's multilingual capabilities and keyword matching. There is no fine-tuned NLP model specifically trained on Karachi crisis terminology.

**Known limitations:**
- Sarcasm and irony may be misclassified (e.g., "mashallah kitna pani hai" could be sarcastic)
- Regional dialect variations may not be recognized
- Code-switching between Urdu, English, and Sindhi in the same post
- Abbreviations and SMS shorthand (e.g., "uni rd" for "University Road")

**Production requirements:**
- Fine-tuned NLP model on labeled Karachi social media data
- Sarcasm/irony detection layer
- Continuous learning from operator corrections
- Multi-language support (Urdu script, Sindhi, English)

---

## Summary

| # | Gap | Severity | Effort to Fix | Blocking? |
|---|-----|----------|--------------|-----------|
| 1 | APK requires Android Studio | Low | 2 hours (CI/CD setup) | No |
| 2 | Public backend deployment | Medium | 1–2 hours | No (offline mode works) |
| 3 | Real Weather/Traffic API keys | Medium | 1 hour + billing setup | No (simulation works) |
| 4 | Demo video recording | Medium | 2–3 hours | No |
| 5 | API rate limits in production | High | Ongoing (paid tiers) | No (fallbacks exist) |
| 6 | No user authentication | Medium | 4–8 hours | No (prototype scope) |
| 7 | Single-region deployment | Low | Days (infrastructure) | No (Karachi scope) |
| 8 | No automated tests | Medium | 8–16 hours | No (manual testing works) |
| 9 | Hardcoded Karachi geography | Low | Days (parameterization) | No (by design) |
| 10 | Roman Urdu NLP accuracy | Medium | Weeks (ML training) | No (Gemini handles well) |

---

> **Our philosophy:** A production-oriented prototype should be honest about what it is and what it isn't. CIRO demonstrates the full architecture, agent coordination, safety validation, and graceful degradation patterns that a production system would need — while being transparent that several infrastructure, security, and ML components would need hardening before real-world deployment.

---

*CIRO is a production-oriented prototype built by Team CIRO: Syed Muhammad Saad (Lead), Farheen (AI Core), Arisha (UI/UX), Areeba (Communications).*
