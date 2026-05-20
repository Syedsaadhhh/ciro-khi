# CIRO — Submission Form Answer Drafts

> **Purpose:** Pre-drafted answers for AISeekho 2026 submission form fields
> **Note:** Copy-paste these into the submission form. Adjust as needed for exact field requirements.

---

## Project Name
```
CIRO — Crisis Intelligence & Response Orchestrator
```

## Team Name
```
Team Antigravity
```

## Challenge Selected
```
Challenge 3 — Crisis Management / Urban Resilience
```

## Team Members
```
1. Syed Muhammad Saad — Team Lead & Principal Cloud Architect
2. Farheen — Lead AI Core Engineer
3. Arisha — Lead UI/UX Designer
4. Areeba — Technical Communications & Media Lead
```

## Short Description (50-100 words)
```
CIRO is a production-oriented AI crisis command center for Karachi's monsoon flooding. It processes Roman Urdu social media signals, fuses them with weather and traffic telemetry via a 4-agent Gemini pipeline, and validates through a deterministic safety gate before generating emergency response recommendations. Built with Google Antigravity as the principal development orchestrator, CIRO catches false alarms, handles API failures gracefully, and operates at zero cost on Firebase Spark and Gemini free tier.
```

## Long Description (200-300 words)
```
CIRO (Crisis Intelligence & Response Orchestrator) is a production-oriented prototype designed to manage urban crises in Karachi, Pakistan. During monsoon season, Karachi's 16 million residents face catastrophic flooding while emergency responders struggle with information overload — thousands of social media reports in Roman Urdu, many contradictory or false.

CIRO addresses this through a 4-agent AI pipeline powered by Google Gemini 3 Flash-Preview:

1. SIFTER AGENT: Ingests raw social posts in Roman Urdu ("pani bhar gaya"), parses flood keywords, and fuses them with Meteosource weather and TomTom traffic telemetry.

2. STRATEGIST AGENT: Cross-validates incidents against fresh data, estimates affected population using Karachi-specific density maps, and generates traffic rerouting plans.

3. VALIDATOR GATE: A deterministic safety layer (intentionally not AI-powered) that catches false alarms by cross-referencing social sentiment against physical measurements. Social panic + zero rainfall = auto-flagged for operator review.

4. COMMANDER AGENT: Generates context-aware citizen alerts, simulates resource dispatch (suction pumps, rescue boats), and creates geographic geofence zones.

Every agent has both a Gemini-powered mode and a deterministic fallback, ensuring the system never crashes — even without API connectivity. The mobile-first dashboard features a live WebSocket trace terminal, Google Maps integration, offline demo mode with pre-built scenarios, and clear REAL/MOCK data labeling.

Built entirely with Google Antigravity as the principal development orchestrator. 110 out of 111 development tasks completed. Operating cost: $0.00 on Firebase Spark and Gemini free tier.
```

## Google AI Tools Used
```
- Google Antigravity (primary development orchestrator — architecture, code generation, debugging, documentation)
- Google Gemini 3 Flash-Preview (multi-agent AI reasoning for 3 agents: Sifter, Strategist, Commander)
- Google Firebase Firestore (real-time database with cirokhi database instance)
- Google Maps JavaScript API (dashboard map integration with dynamic markers)
```

## Technical Stack
```
- Backend: FastAPI (Python 3.11+), Uvicorn, structlog, Tenacity, Pydantic
- AI: Google Gemini 3 Flash-Preview via google-genai SDK
- Database: Firebase Firestore (production) / In-memory dict (demo fallback)
- Frontend: HTML5/CSS3/JavaScript SPA, Google Maps JS API
- Mobile: CapacitorJS → Android APK
- External APIs: Meteosource (weather), TomTom (traffic)
- Real-time: WebSocket (FastAPI native)
```

## GitHub Repository URL
```
[Insert GitHub URL here]
```

## Demo Video URL
```
[Insert YouTube/Drive URL here — CIRO-Demo-Video.mp4]
```

## Antigravity Usage Video URL
```
[Insert YouTube/Drive URL here — CIRO-Antigravity-Usage.mp4]
```

## Key Innovation (1-2 sentences)
```
CIRO's ValidatorGate is a deterministic safety layer that catches false alarms by cross-referencing AI-parsed social signals against physical telemetry — a deliberate design choice where the safety gate is rule-based (not AI-powered) because safety-critical decisions should not rely on probabilistic inference.
```

## How Antigravity Was Used (1-2 sentences)
```
Google Antigravity served as the principal development orchestrator for CIRO, designing the system architecture, generating the 4-agent pipeline codebase, implementing the ValidatorGate safety logic, building the 3,900-line mobile dashboard, and producing 20+ evidence files — completing 110 out of 111 development tasks. See the Antigravity Trace Pack (14 documents) for full evidence.
```

## Challenges Faced
```
1. Firestore database_id parameter: Initial code used database= (accepted silently) instead of database_id=, causing data to go to the wrong database. Antigravity identified and fixed this.
2. Gemini response parsing: Gemini occasionally wrapped JSON responses in markdown code fences despite system prompt instructions. Added stripping logic.
3. Offline resilience: Google Maps and Firebase both fail without network. Built SVG fallback map and in-memory storage to ensure demo never crashes.
```

## Future Improvements
```
1. Fine-tuned Urdu NLP model (replacing keyword matching with trained Gemini model)
2. Real-time Twitter/X API integration for live social signal ingestion
3. PDMA/NDMA integration for actual dispatch coordination
4. Multi-city expansion beyond Karachi
5. Historical incident learning for improved severity prediction
```
