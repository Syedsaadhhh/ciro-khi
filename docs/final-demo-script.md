# CIRO — Demo Video Script (3-5 Minutes)

> **Target Length:** 3:30 – 4:00
> **Format:** Screen recording with voiceover
> **Resolution:** 1080p minimum

---

## HOOK — What Is CIRO? (0:00 – 0:15)

**[SCREEN: Title card — "CIRO: Crisis Intelligence & Response Orchestrator"]**

**VOICEOVER:**
"Karachi. 16 million people. Every monsoon season, the city faces catastrophic urban flooding. Social media explodes with cries for help — in Roman Urdu. Emergency responders are overwhelmed. What if AI could cut through the noise in real time?"

---

## SEGMENT 1 — Mobile App Overview (0:15 – 1:00)

**[SCREEN: Open CIRO mobile app / web dashboard]**

**VOICEOVER:**
"This is CIRO — a production-oriented crisis command center built for Karachi. Let me show you the app."

**ACTIONS:**
1. Show the map screen with Karachi zones
2. Point out the live clock (PKT timezone)
3. Show the network status badge (ONLINE)
4. Navigate through all 5 screens briefly: Map → Trace → Before/After → KPI → Alerts
5. Show the idle state: "No active incidents — system monitoring"

**VOICEOVER:**
"The dashboard monitors Karachi in real time across five views: live map, agent reasoning traces, before/after impact, KPI metrics, and alert history. Right now, the system is idle — no crisis detected."

---

## SEGMENT 2 — Confirmed Flood Scenario (1:00 – 2:00)

**[SCREEN: Click "Confirmed Flood" demo button or POST /simulate]**

**VOICEOVER:**
"Let's simulate a confirmed monsoon flood. A Roman Urdu social post says 'University Road pe pani bhar gaya' — water has filled University Road. The weather API confirms 45mm rainfall. Traffic is severely congested."

**ACTIONS:**
1. Trigger the confirmed flood scenario
2. Switch to Agent Trace screen
3. Watch traces appear in real time:
   - [SIFTER] Parses social signals, detects flood keywords
   - [STRATEGIST] Estimates 45,000 affected people, generates rerouting
   - [VALIDATOR] Confirms: strong signal + strong telemetry match
   - [COMMANDER] Dispatches 5 suction pumps, issues SMS advisory
4. Switch to Map screen — show marker placed at University Road
5. Show the result overlay with severity scorecard

**VOICEOVER:**
"Watch the agent reasoning chain. The Sifter parses the Roman Urdu signal. The Strategist cross-validates with weather and traffic data, estimates 45,000 people at risk. The ValidatorGate confirms — social signals match physical telemetry. The Commander generates an alert and simulates dispatching emergency resources."

---

## SEGMENT 3 — False Alarm Rejection (2:00 – 2:30)

**[SCREEN: Trigger "False Alarm" scenario]**

**VOICEOVER:**
"But what if someone posts fake flood reports? Let's test it."

**ACTIONS:**
1. Trigger false alarm scenario (high social score + 0mm rainfall)
2. Show agent traces:
   - [SIFTER] Detects social flood signals
   - [VALIDATOR] "Contradiction: Social signal high but telemetry reports no rain"
3. Show result: `requires_operator_review`
4. Point out the orange "REQUIRES REVIEW" safety label

**VOICEOVER:**
"The social signals claim severe flooding, but the weather API reports zero millimeters of rain. The ValidatorGate catches this contradiction and flags it for operator review. No false dispatch. No wasted resources. AI safety in action."

---

## SEGMENT 4 — Missing Telemetry / Fallback Mode (2:30 – 3:00)

**[SCREEN: Trigger "Missing Telemetry" scenario]**

**VOICEOVER:**
"What happens when the APIs themselves go down?"

**ACTIONS:**
1. Trigger missing telemetry scenario
2. Show traces:
   - [VALIDATOR] "Telemetry API unavailable. Running in Mock Fallback Mode."
3. Show `fallback_mode: true` in response
4. Show MOCK badge on the response

**VOICEOVER:**
"When weather or traffic APIs are unavailable, CIRO doesn't crash. It activates fallback mode, uses cached data, and clearly labels all results as MOCK data. The system degrades gracefully — it never goes blind."

---

## SEGMENT 5 — Antigravity's Role (3:00 – 3:30)

**[SCREEN: Show Antigravity workspace briefly]**

**VOICEOVER:**
"CIRO was built with Google Antigravity as the principal development orchestrator. Antigravity designed the architecture, generated the multi-agent pipeline, implemented safety gates, built the mobile dashboard, and generated this entire evidence pack."

**ACTIONS:**
1. Briefly show the Antigravity workspace
2. Show a file being generated (e.g., orchestrator.py)
3. Show the evidence pack folder

---

## SEGMENT 6 — Impact Summary (3:30 – 4:00)

**[SCREEN: KPI dashboard screen]**

**VOICEOVER:**
"In summary: CIRO processes crisis signals in under 6 seconds. It runs 4 AI agents with built-in safety gates. It catches false alarms before they waste resources. And it costs zero dollars to operate on Firebase Spark and Gemini free tier."

**ACTIONS:**
1. Show KPI cards: Pipeline latency, Agent count, False alarm catch rate
2. Show evidence pack folder (20+ files)
3. End on title card: "CIRO — Built with Google Antigravity for AISeekho 2026"

**CLOSING:**
"CIRO. Crisis intelligence that knows when to act — and when not to."

---

## Technical Notes for Recording
- Use OBS Studio or similar screen recorder
- Record at 1920×1080 minimum
- Narrate over screen recording (or use AI voiceover from `voiceover-script-google-ai-studio.md`)
- Keep transitions clean — no fancy effects needed
- Ensure CIRO logo/title is visible in opening and closing frames
