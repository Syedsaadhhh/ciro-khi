# CIRO System Scale, Latency & Cost Evidence

## Latency Profiles
The CIRO Multi-Agent architecture completes its loop (Sifter → Strategist → Validator → Commander) synchronously but leverages highly optimal prompts and fast endpoints.

- **Agent Reasoning Generation:** ~1.2s per Agent
- **Data Extractor APIs (Weather/Traffic):** ~200ms
- **End-to-End Orchestration Loop:** ~5.5 seconds (measured via local `/simulate` endpoint trace)
- **UI Real-Time WebSocket Delivery:** <50ms (DOM manipulation via reactive JavaScript injections rather than full-page React re-renders)

## Infrastructure Footprint & Cost
We utilized serverless architectures specifically to keep operational costs mathematically close to **$0.00** during downtime.

- **Google Gemini API (Gemini 3 Flash-Preview):** 
  Utilized for structural parsing and intelligent dispatching. Because prompts are heavily compressed and output JSON strictly, usage during demo scaling falls completely under the **Free Tier**.
- **Firebase Firestore:**
  Live incident state management. Employs a NoSQL structure with document subscriptions (`onSnapshot`). At demo load (10-50 simultaneous reads), this costs **$0.00** against the Firebase Spark Plan.
- **Frontend / Cloud Hosting:**
  Fully decoupled static `index.html` frontend. We employ CDN-style static hosting. Zero backend EC2 server costs required for the UI.

## Fallback Modularity
In situations where an API Key (TomTom, Meteosource) hits rate limits or is redacted from `.env` prior to code submission, the `tools` pipeline will autonomously reroute to isolated static functions. This guarantees that **100% of the architecture remains judge-runnable without external dependencies**.
