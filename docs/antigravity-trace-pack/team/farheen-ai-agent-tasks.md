# Farheen — AI Agent & Gemini Integration Tasks

> **Role:** Lead AI Core Engineer
> **Project:** CIRO — Crisis Intelligence & Response Orchestrator

---

## Task Log

### SifterAgent Development
- [x] **Agent class structure** — `SifterAgent` with `__init__`, `run()`, Gemini client setup
- [x] **System prompt design** — Crisis classification prompt for Karachi monsoon/heatwave dual-matrix
- [x] **Gemini integration** — `google.genai.Client` with `gemini-3-flash-preview` model
- [x] **Response parsing** — JSON extraction with markdown code fence stripping
- [x] **Deterministic fallback** — `_deterministic_analysis()` with weighted scoring (weather + traffic + social)
- [x] **False alarm detection** — `_is_obvious_false_alarm()` with multi-source threshold checks
- [x] **Roman Urdu parsing** — Signal extraction from posts containing "pani bhar gaya", "barish", "doob gaya"

### StrategistAgent Development
- [x] **Cross-validation logic** — `_validate_incident()` with fresh data re-check against weather/traffic
- [x] **Population estimation** — Integration with `geofence_tool.py` for density-based estimates
- [x] **Rerouting decision** — Congestion threshold (≥6) or severity threshold (≥7) triggers rerouting
- [x] **Priority classification** — Severity-to-priority mapping (1-3→low, 4-6→medium, 7-8→high, 9-10→critical)
- [x] **Mitigation strategy** — Gemini-generated and rule-based strategy text
- [x] **Gemini fallback** — `_gemini_strategy()` with exception handler falling back to `_rule_based_strategy()`

### CommanderAgent Development
- [x] **Alert generation** — `create_alert()` integration with severity-based channel selection
- [x] **Gemini alert messages** — Context-aware citizen alerts with location, severity, alternate routes
- [x] **Emergency ticketing** — `create_emergency_ticket()` for severity ≥7 incidents
- [x] **Emergency ops activation** — Protocol activation for severity ≥9 incidents
- [x] **Geofence creation** — `calculate_geofence()` for impact zone around incident location
- [x] **Action list building** — Dynamic actions: trigger_alert, reroute_traffic, dispatch_ticket, activate_emergency_ops, push_live_update

### ValidatorGate Design
- [x] **Confirmed flood rule** — Social > 0.5 AND rainfall ≥ 10mm → validated
- [x] **Contradiction rule** — Social > 0.5 AND rainfall == 0mm → operator review
- [x] **Weak signal rule** — Social ≤ 0.5 AND rainfall < 10mm → operator review
- [x] **Heatwave false alarm** — Social crisis + temperature < 35°C → rejected
- [x] **Fallback mode detection** — Simulated telemetry markers trigger `fallback_mode: true`
- [x] **Deterministic design decision** — Gate uses hard thresholds, not AI inference (intentional safety choice)

### Tool Modules
- [x] **Weather tool** — Meteosource API integration with hardcoded fallback JSON
- [x] **Traffic tool** — TomTom API integration with congestion mapping fallback
- [x] **Social signal tool** — Roman Urdu keyword parser with mock post generator
- [x] **Geofence tool** — Karachi-specific population density mappings per zone
- [x] **Reroute tool** — Alternative route generation with delay estimation
- [x] **Alert tool** — Alert object factory with severity-based channel selection

### Signal Fusion
- [x] **Multi-source scoring** — Weather (0-4 points) + Traffic (0-3 points) + Social (0-3 points)
- [x] **False alarm penalty** — -1.5 points for >2 false alarm signals
- [x] **Minimum threshold** — Score < 2.0 → no incident created
- [x] **Confidence calculation** — `score / 10.0 + 0.1 * len(sources)`

---

## Antigravity Contribution

Antigravity was instrumental in:
1. Designing the dual-mode (Gemini + deterministic) agent architecture
2. Crafting system prompts that produce structured JSON responses
3. Implementing the ValidatorGate as a deterministic safety layer
4. Building the scoring algorithm for signal fusion
5. Writing the Roman Urdu keyword parser

## Files Authored/Modified
`agents/sifter_agent.py`, `agents/strategist_agent.py`, `agents/commander_agent.py`, `core/orchestrator.py` (ValidatorGate method), `tools/weather_tool.py`, `tools/traffic_tool.py`, `tools/social_signal_tool.py`, `tools/geofence_tool.py`, `tools/reroute_tool.py`, `tools/alert_tool.py`, `models/incident.py`, `models/plan.py`, `models/action.py`
