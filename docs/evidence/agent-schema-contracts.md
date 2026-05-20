# CIRO Agent Schema Contracts

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Schema Contracts for Inter-Agent Communication  
> Version: 2.1.0  
> Last Updated: 2026-05-20

---

## Overview

This document defines the data contracts between CIRO's four agents and the external API surface. Each schema is described with field names, types, constraints, and example values. All agents communicate via these structured objects through the orchestrator.

---

## 1. SignalInput Schema

**Used by:** POST `/simulate` endpoint → ingested by SifterAgent  
**Purpose:** Raw input from the operator or simulation interface.

```json
{
  "location": "string — required, free-text location name in Karachi",
  "social_posts": ["string[] — required, array of Roman Urdu or English crisis posts"],
  "rainfall_mm": "number — required, 0–200, rainfall in millimeters",
  "congestion_level": "number — required, 1–10, traffic congestion score"
}
```

### Field Details

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `location` | string | Yes | Non-empty | Free-text location name (e.g., "University Road") |
| `social_posts` | string[] | Yes | Min 1 item | Array of social media posts, typically in Roman Urdu |
| `rainfall_mm` | number | Yes | 0 ≤ x ≤ 200 | Rainfall measurement in millimeters |
| `congestion_level` | number | Yes | 1 ≤ x ≤ 10 | Traffic congestion score (1 = free flow, 10 = total gridlock) |

### Example

```json
{
  "location": "University Road",
  "social_posts": ["pani bhar gaya gari phas gayi university road emergency"],
  "rainfall_mm": 50,
  "congestion_level": 9
}
```

---

## 2. IncidentModel Schema

**Used by:** SifterAgent → StrategistAgent → stored in Firestore `/incidents/{incident_id}`  
**Purpose:** Represents a parsed and classified crisis incident.

```json
{
  "incident_id": "string — auto-generated, format: INC-YYYY-MMDD-NNNN",
  "session_id": "string — auto-generated, format: sess-YYYYMMDD-HHMMSS-location",
  "event_type": "string — enum: flood | heatwave | earthquake | infrastructure | uncertain",
  "location": "string — human-readable location",
  "coordinates": {
    "lat": "number — latitude (Karachi range: 24.80–24.95)",
    "lng": "number — longitude (Karachi range: 67.00–67.20)"
  },
  "severity": "number — 0.0–10.0, computed severity score",
  "priority": "string — enum: CRITICAL | HIGH | MEDIUM | LOW",
  "confidence": "number — 0.0–1.0, validation confidence",
  "validated": "boolean — true if ValidatorGate confirmed",
  "estimated_affected_population": "number | null",
  "estimated_delay_minutes": "number | null",
  "fallback_mode": "boolean — true if any telemetry source was unavailable",
  "raw_signals": {
    "weather": "WeatherSignal object",
    "traffic": "TrafficSignal object",
    "social": "SocialSignal object"
  },
  "timestamp": "string — ISO 8601 UTC",
  "created_at": "string — ISO 8601 UTC",
  "updated_at": "string — ISO 8601 UTC"
}
```

### Nested: WeatherSignal

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Data source identifier (e.g., "simulated_weather_api") |
| `rainfall_mm` | number \| null | Rainfall in mm, null if unavailable |
| `classification` | string | "clear", "light", "moderate", "heavy", "extreme", "unavailable" |
| `data_quality` | string | "nominal" or "degraded" |

### Nested: TrafficSignal

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Data source identifier |
| `congestion_level` | number | 1–10 scale |
| `classification` | string | "normal_flow", "moderate", "heavy_congestion", "severe_gridlock", "total_gridlock" |
| `data_quality` | string | "nominal" or "degraded" |

### Nested: SocialSignal

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Origin of social data |
| `posts_analyzed` | number | Count of posts processed |
| `flood_signals_detected` | number | Count of flood-related keywords/intents |
| `sentiment_score` | number | 0.0–1.0, crisis sentiment strength |
| `language` | string | "roman_urdu", "english", "urdu" |
| `parsed_intent` | string | "flood_emergency", "uncertain_observation", etc. |
| `original_text` | string | Raw input text |

---

## 3. PlanModel Schema

**Used by:** StrategistAgent → ValidatorGate  
**Purpose:** Strategic response plan with cross-validation and resource recommendations.

```json
{
  "generated_by": "string — always 'StrategistAgent'",
  "strategy": "string — enum: full_emergency_response | partial_response_pending_confirmation | hold_for_contradiction_resolution | pending_validation | no_action_required",
  "cross_validation": {
    "weather_confirms_social": "boolean | null — null if weather unavailable",
    "traffic_confirms_social": "boolean | null",
    "telemetry_agreement": "string — enum: strong | partial_degraded | contradictory | none"
  },
  "alternative_routes": [
    {
      "name": "string — route name",
      "description": "string — route description",
      "estimated_delay_minutes": "number",
      "status": "string — enum: recommended | available | congested"
    }
  ],
  "resource_recommendations": ["string[] — list of resource deployment instructions"],
  "contradiction_analysis": {
    "social_vs_weather": "string | null — conflict description",
    "social_vs_traffic": "string | null",
    "possible_explanations": ["string[]"]
  },
  "strategist_note": "string | null — optional human-readable note"
}
```

---

## 4. ActionModel Schema

**Used by:** CommanderAgent → API response + Firestore  
**Purpose:** Emergency action package with alerts, geofences, and dispatch tickets.

```json
{
  "generated_by": "string — always 'CommanderAgent'",
  "alert_message": "string | null — human-readable alert text, null if no action",
  "channels": ["string[] — enum values: sms | app_push | dashboard | public_pa"],
  "geofence": {
    "center": {
      "lat": "number",
      "lng": "number"
    },
    "radius_km": "number — geofence radius in kilometers",
    "restriction": "string — enum: avoid_zone | caution_zone | heat_advisory_zone"
  },
  "emergency_ticket": {
    "ticket_id": "string — format: EMR-YYYY-MMDD-NNNN",
    "dispatched_to": ["string[] — agency identifiers"],
    "dispatch_mode": "string — always 'simulated' in prototype",
    "requires_operator_approval": "boolean — always true in prototype"
  },
  "suppressed_reason": "string | null — reason if action was suppressed by ValidatorGate"
}
```

---

## 5. SafetyValidation Schema

**Used by:** ValidatorGate → included in API response and Firestore document  
**Purpose:** Structural validation result with pass/fail checks and confidence scoring.

```json
{
  "validated_by": "string — always 'ValidatorGate'",
  "validated": "boolean — true if incident is confirmed",
  "status": "string — enum: confirmed | requires_operator_review | rejected_by_validator | no_incident",
  "confidence_score": "number — 0.0–1.0, final confidence after adjustments",
  "checks_passed": ["string[] — list of check descriptions that passed"],
  "checks_failed": ["string[] — list of check descriptions that failed"],
  "escalation_required": "boolean — true if operator must review",
  "escalation_reason": "string | null — why escalation is needed",
  "contradiction_flag": "boolean | null — true if cross-source contradiction detected",
  "rejection_reason": "string | null — why incident was rejected",
  "notes": "string | null — additional context"
}
```

---

## 6. WebSocket Trace Event Shape

**Used by:** `/ws/live-trace` WebSocket endpoint  
**Purpose:** Real-time trace events streamed to the frontend during pipeline execution.

```json
{
  "event_type": "string — enum: orchestrator | sifter | strategist | validator | commander | error",
  "session_id": "string — session identifier",
  "timestamp": "string — ISO 8601 UTC with milliseconds",
  "agent": "string — agent name (e.g., 'SifterAgent')",
  "stage": "number — pipeline stage (0=input, 1=sifter, 2=strategist, 3=validator, 4=commander)",
  "message": "string — human-readable log message",
  "data": "object | null — optional structured data payload",
  "is_final": "boolean — true if this is the last event in the pipeline"
}
```

### Example Trace Events

```json
{
  "event_type": "sifter",
  "session_id": "sess-20260520-023000-univ-road",
  "timestamp": "2026-05-20T02:30:00.812Z",
  "agent": "SifterAgent",
  "stage": 1,
  "message": "Parsed Roman Urdu crisis signal: 'pani bhar gaya gari phas gayi university road emergency'",
  "data": {
    "language": "roman_urdu",
    "intent": "flood_emergency",
    "flood_signals": 4
  },
  "is_final": false
}
```

```json
{
  "event_type": "orchestrator",
  "session_id": "sess-20260520-023000-univ-road",
  "timestamp": "2026-05-20T02:30:04.914Z",
  "agent": "Orchestrator",
  "stage": 4,
  "message": "Workflow pipeline complete.",
  "data": {
    "incident_id": "INC-2026-0520-0001",
    "status": "confirmed",
    "duration_ms": 4812
  },
  "is_final": true
}
```

---

## Schema Versioning

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-05-20 | Added fallback_mode, contradiction_analysis, multi-crisis support |
| 2.0.0 | 2026-05-18 | Introduced ValidatorGate, SafetyValidation schema |
| 1.0.0 | 2026-05-15 | Initial schema with SifterAgent and CommanderAgent |

---

*CIRO is a production-oriented prototype. All schemas are subject to refinement based on real-world deployment feedback.*
