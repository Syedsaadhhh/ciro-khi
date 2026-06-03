"""
core/response_builder.py
─────────────────────────
Builds the standardised CIRO decision schema response from orchestrator outputs.

Generates dynamic action text and resource recommendations based on location,
severity, and validation status — no hardcoded dispatch strings.

Decision schema (canonical):
{
    "status":                     str,
    "reason":                     str,
    "severity":                   int | None,
    "confidence":                 float | None,
    "requires_operator_approval": bool,
    "simulated":                  bool,
    "fallback_mode":              bool,
    "source_labels": {
        "weather":    "Live | Mock | Unavailable",
        "traffic":    "Live | Mock | Unavailable",
        "social":     "User-entered | Demo | Mock",
        "validation": "Confirmed | Review | Invalid",
    },
    "resources":                  list[dict],
    "stakeholder_messages":       list[dict],
    "action_text":                str,
    "affected_population":        int | None,
    "estimated_delay_minutes":    int | None,
    "priority":                   str | None,
    "session_id":                 str,
    "run_id":                     str,
    # Legacy nested fields for frontend backwards compatibility:
    "incident":                   dict | None,
    "plan":                       dict | None,
    "action":                     dict | None,
    "safety_validation":          dict,
}

Hotspot support: pass hotspot_data=dict to build_confirmed() in future.
"""

from __future__ import annotations
from typing import Optional
import uuid


# ── Resource scaling ──────────────────────────────────────────────────────

def _scale_resources(severity: int, location: str) -> list[dict]:
    """Generate resource allocation list scaled to incident severity."""
    pumps   = 5 if severity >= 9 else 3 if severity >= 7 else 2 if severity >= 5 else 1
    police  = 6 if severity >= 9 else 4 if severity >= 7 else 3 if severity >= 5 else 2
    rescue  = 3 if severity >= 9 else 2 if severity >= 7 else 1
    utility = 2 if severity >= 7 else 1
    hosp    = "Civil Hospital + Liaquat National" if severity >= 8 else "Civil Hospital Karachi"

    return [
        {"type": "Drainage Pumps",     "count": pumps,   "status": "SIMULATED — Pending approval"},
        {"type": "Traffic Police",      "count": police,  "status": "SIMULATED — Pending approval"},
        {"type": "Rescue Teams",        "count": rescue,  "status": "SIMULATED — Pending approval"},
        {"type": "Utility Response",    "count": utility, "status": "SIMULATED — Pending approval"},
        {"type": "Hospital Alert",      "name":  hosp,    "status": "SIMULATED — Standby"},
    ]


# ── Action text generation ────────────────────────────────────────────────

def _generate_action_text(
    status: str,
    location: str,
    severity: Optional[int],
    resources: list[dict],
    reason: str = "",
) -> str:
    """
    Generate readable action text dynamically. Never hardcodes unit numbers
    in a string — derives them from the resources list.
    """
    if status == "invalid_signal":
        return f"Signal at {location} rejected by ValidatorGate. {reason}"

    if status in ("requires_operator_review", "missing_telemetry"):
        return (
            f"Incident at {location} flagged for operator review. "
            f"Reason: {reason} No automated dispatch until human approval."
        )

    if status == "false_alarm":
        return f"Signal at {location} classified as false alarm. No crisis detected. No action required."

    # For confirmed status, build from resources
    if status == "confirmed" and resources:
        pumps_entry  = next((r for r in resources if "Pump" in r.get("type", "")), None)
        police_entry = next((r for r in resources if "Police" in r.get("type", "")), None)
        rescue_entry = next((r for r in resources if "Rescue" in r.get("type", "")), None)

        parts = []
        if pumps_entry:
            parts.append(f"{pumps_entry['count']} drainage pump(s)")
        if police_entry:
            parts.append(f"{police_entry['count']} traffic police unit(s)")
        if rescue_entry:
            parts.append(f"{rescue_entry['count']} rescue team(s)")

        resource_text = ", ".join(parts) if parts else "emergency units"
        sev_label = "CRITICAL" if (severity or 0) >= 8 else "HIGH" if (severity or 0) >= 6 else "MODERATE"

        return (
            f"[SIMULATED — OPERATOR APPROVAL REQUIRED] "
            f"{sev_label} incident at {location}. "
            f"Recommended response: deploy {resource_text}. "
            f"All actions pending operator authorisation."
        )

    return f"Incident at {location} processed. Status: {status}."


# ── Stakeholder messages ──────────────────────────────────────────────────

def _generate_stakeholder_messages(
    status: str,
    location: str,
    severity: Optional[int],
    population: Optional[int],
    priority: Optional[str],
    resources: list[dict],
) -> list[dict]:
    """Generate stakeholder message cards dynamically from result data."""
    if status not in ("confirmed",):
        return []

    sev = severity or 0
    pop = population or 0
    pri = (priority or "high").upper()

    police_count = next(
        (r["count"] for r in resources if "Police" in r.get("type", "")), 3
    )
    util_count = next(
        (r["count"] for r in resources if "Utility" in r.get("type", "")), 1
    )
    hosp = next(
        (r["name"] for r in resources if "Hospital" in r.get("type", "")),
        "Civil Hospital Karachi",
    )

    return [
        {
            "recipient": "public",
            "title": f"⚠ FLOOD ALERT — {location}",
            "body": (
                f"SIMULATED: {pri} priority flood event detected at {location}. "
                f"Estimated {pop:,} people at risk. Avoid the area. Use alternate routes. "
                f"[No real alert sent — operator approval required]"
            ),
            "simulated": True,
        },
        {
            "recipient": "traffic_police",
            "title": "Traffic Diversion Order",
            "body": (
                f"SIMULATED: Deploy {police_count} units to {location} junction control. "
                f"Redirect inbound traffic per CIRO advisory. ETA: <10 min. "
                f"[Pending operator authorisation]"
            ),
            "simulated": True,
        },
        {
            "recipient": "hospital",
            "title": "Hospital Readiness — Possible Intake",
            "body": (
                f"SIMULATED: Flood zone {location}. Severity {sev}/10. "
                f"Population at risk: {pop:,}. Alert {hosp}. "
                f"Activate emergency intake protocol if severity ≥ 7. "
                f"[No real alert sent — operator approval required]"
            ),
            "simulated": True,
        },
        {
            "recipient": "utility",
            "title": "Utility Infrastructure Check",
            "body": (
                f"SIMULATED: Flooding at {location}. "
                f"Deploy {util_count} utility team(s). Inspect drainage sub-mains and electrical. "
                f"[Pending operator authorisation]"
            ),
            "simulated": True,
        },
        {
            "recipient": "municipal",
            "title": "Municipal Control — Incident Logged",
            "body": (
                f"SIMULATED: Incident logged in Firestore (database=cirokhi). "
                f"Priority: {pri}. All dispatch requires console approval. "
                f"Trace streaming on /ws/live-trace. "
                f"[All actions remain simulated until operator approval]"
            ),
            "simulated": True,
        },
    ]


# ── Source labels ────────────────────────────────────────────────────────

def _source_labels(
    weather_source: str,
    traffic_source: str,
    social_is_user_entered: bool,
    validation_label: str,
) -> dict:
    """Map internal source keys to human-readable labels."""

    def _weather_label(src: str) -> str:
        if "google" in src.lower() or "live" in src.lower():
            return "Live"
        if "fallback" in src.lower() or "unavailable" in src.lower():
            return "Unavailable"
        return "Mock"

    def _traffic_label(src: str) -> str:
        if "google" in src.lower() or "live" in src.lower():
            return "Live"
        if "simulated" in src.lower() or "mock" in src.lower():
            return "Mock"
        return "Mock"

    return {
        "weather":    _weather_label(weather_source),
        "traffic":    _traffic_label(traffic_source),
        "social":     "User-entered" if social_is_user_entered else "Demo / Mock",
        "validation": validation_label,
    }


# ── Public builders ───────────────────────────────────────────────────────

def build_confirmed(
    incident: dict,
    plan: dict,
    action: dict,
    safety_validation: dict,
    session_id: str,
    run_id: str,
    social_is_user_entered: bool = False,
    hotspot_data: Optional[dict] = None,   # reserved for Phase 2 hotspot
) -> dict:
    """Build a full confirmed CIRO decision response."""
    location    = incident.get("location", "Karachi")
    severity    = incident.get("severity")
    confidence  = incident.get("confidence")
    pop         = plan.get("affected_population")
    delay       = plan.get("estimated_delay_minutes")
    priority    = plan.get("priority")

    raw = incident.get("raw_signals") or {}
    weather_src = (raw.get("weather") or {}).get("source", "mock")
    traffic_src = (raw.get("traffic") or {}).get("source", "mock")

    resources = _scale_resources(severity or 5, location)
    action_text = _generate_action_text(
        "confirmed", location, severity, resources
    )
    stakeholders = _generate_stakeholder_messages(
        "confirmed", location, severity, pop, priority, resources
    )
    labels = _source_labels(
        weather_src, traffic_src,
        social_is_user_entered,
        "Confirmed",
    )

    return {
        "status":                     "completed",
        "reason":                     "Incident confirmed by ValidatorGate.",
        "severity":                   severity,
        "confidence":                 confidence,
        "requires_operator_approval": True,
        "simulated":                  True,
        "fallback_mode":              safety_validation.get("fallback_mode", False),
        "source_labels":              labels,
        "resources":                  resources,
        "stakeholder_messages":       stakeholders,
        "action_text":                action_text,
        "affected_population":        pop,
        "estimated_delay_minutes":    delay,
        "priority":                   priority,
        "session_id":                 session_id,
        "run_id":                     run_id,
        # Legacy nested fields for frontend backwards compatibility
        "incident":                   incident,
        "plan":                       plan,
        "action":                     {
            **action,
            "alert_message": action_text,  # override with dynamic text
        },
        "safety_validation":          safety_validation,
        "hotspot_data":               hotspot_data,  # None until Phase 2
    }


def build_review(
    incident_id: str,
    reason: str,
    session_id: str,
    run_id: str,
    safety_validation: Optional[dict] = None,
) -> dict:
    """Build a requires_operator_review response."""
    sv = safety_validation or {}
    return {
        "status":                     "requires_operator_review",
        "reason":                     reason,
        "severity":                   None,
        "confidence":                 None,
        "requires_operator_approval": True,
        "simulated":                  True,
        "fallback_mode":              sv.get("fallback_mode", False),
        "source_labels": {
            "weather":    "Unavailable",
            "traffic":    "Unavailable",
            "social":     "User-entered",
            "validation": "Review",
        },
        "resources":            [],
        "stakeholder_messages": [],
        "action_text":          f"Operator review required. Reason: {reason}",
        "session_id":           session_id,
        "run_id":               run_id,
        "incident":             {"incident_id": incident_id},
        "plan":                 None,
        "action":               None,
        "safety_validation":    sv,
    }


def build_rejected(
    incident_id: str,
    reason: str,
    session_id: str,
    run_id: str,
    status: str = "rejected",
) -> dict:
    """Build a rejected / false_alarm response."""
    return {
        "status":                     status,
        "reason":                     reason,
        "severity":                   None,
        "confidence":                 None,
        "requires_operator_approval": False,
        "simulated":                  True,
        "fallback_mode":              False,
        "source_labels": {
            "weather":    "Unavailable",
            "traffic":    "Unavailable",
            "social":     "User-entered",
            "validation": "Invalid",
        },
        "resources":            [],
        "stakeholder_messages": [],
        "action_text":          f"Signal rejected: {reason}",
        "session_id":           session_id,
        "run_id":               run_id,
        "incident":             {"incident_id": incident_id},
        "plan":                 None,
        "action":               None,
        "safety_validation":    {"validated": False, "fallback_mode": False},
    }


def build_no_incident(
    location: str,
    session_id: str,
    run_id: str,
) -> dict:
    """Build a no_incident (false alarm) response."""
    return {
        "status":                     "no_incident",
        "reason":                     f"No crisis detected at {location}. Classified as false alarm.",
        "severity":                   None,
        "confidence":                 None,
        "requires_operator_approval": False,
        "simulated":                  True,
        "fallback_mode":              False,
        "source_labels": {
            "weather":    "Mock",
            "traffic":    "Mock",
            "social":     "User-entered",
            "validation": "Invalid",
        },
        "resources":            [],
        "stakeholder_messages": [],
        "action_text":          f"No incident at {location}. Signal closed.",
        "session_id":           session_id,
        "run_id":               run_id,
        "incident":             None,
        "plan":                 None,
        "action":               None,
        "safety_validation":    {"validated": False, "fallback_mode": False},
    }
