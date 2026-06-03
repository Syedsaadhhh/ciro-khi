"""
core/signal_validator.py
─────────────────────────
Backend-side ValidatorGate pre-check.

Validates raw SignalInput before the orchestrator pipeline runs.
Returns a structured result dict using the shared CIRO decision schema,
or None to indicate the input is clean and the pipeline should proceed.

Decision schema (shared with frontend via JSON response):
{
    "status":                   str,   # confirmed | requires_operator_review |
                                       # invalid_signal | false_alarm | missing_telemetry
    "reason":                   str,
    "severity":                 int | None,
    "confidence":               float | None,
    "requires_operator_approval": bool,
    "simulated":                bool,
    "fallback_mode":            bool,
    "source_labels": {
        "weather":  "Live | Mock | Unavailable",
        "traffic":  "Live | Mock | Unavailable",
        "social":   "User-entered | Demo | Mock",
        "validation": "Confirmed | Review | Invalid",
    },
    "resources":                list,
    "stakeholder_messages":     list,
    "session_id":               str | None,
    "run_id":                   str | None,
}

Hotspot support: future `hotspot_data` field can be added to SignalInput
and validated here without changing the orchestrator pipeline.
"""

import re
import uuid
from typing import Optional


# ── Helpers ──────────────────────────────────────────────────────────────

def _has_language_words(text: str, min_words: int = 2) -> bool:
    """Return True if text contains at least `min_words` 4+ char alpha words."""
    words = re.findall(r'[a-zA-Z\u0600-\u06FF]{4,}', text)
    return len(words) >= min_words


def _special_char_ratio(text: str) -> float:
    """Ratio of non-safe characters to total length."""
    safe = len(re.findall(r'[\w\u0600-\u06FF\s,.\-\'"!?]', text))
    return (len(text) - safe) / max(len(text), 1)


def _is_symbols_only(text: str) -> bool:
    """True if the whole string is symbols/digits/colons with no alpha."""
    return bool(re.match(r'^[\s@#$%^&*!?\d:.,;_|\-]+$', text.strip()))


def _has_repetitive_pattern(text: str) -> bool:
    """Catch '666666', '::::::', '5:5:5:5' style patterns."""
    return bool(re.search(r'(.{1,3})\1{4,}', text))


def _build_early_exit(
    status: str,
    reason: str,
    session_id: str,
    run_id: str,
    validation_label: str = "Invalid",
    requires_approval: bool = False,
) -> dict:
    """Build a full CIRO decision schema response for early exits."""
    return {
        "status": status,
        "reason": reason,
        "severity": None,
        "confidence": None,
        "requires_operator_approval": requires_approval,
        "simulated": True,
        "fallback_mode": False,
        "source_labels": {
            "weather": "Unavailable",
            "traffic": "Unavailable",
            "social": "User-entered",
            "validation": validation_label,
        },
        "resources": [],
        "stakeholder_messages": [],
        "session_id": session_id,
        "run_id": run_id,
    }


# ── Public API ────────────────────────────────────────────────────────────

def validate_signal_input(
    social_text: Optional[str],
    rainfall_mm: Optional[float],
    congestion_level: Optional[int],
    session_id: Optional[str] = None,
    run_id: Optional[str] = None,
) -> Optional[dict]:
    """
    Validate raw user input before it enters the orchestrator pipeline.

    Returns:
        None   → input is valid; proceed with orchestrator.
        dict   → early-exit CIRO decision schema; return this directly as
                 the /simulate response result.

    Rules applied in order of increasing cost:
      1. Empty / missing signal
      2. Too short (< 12 chars)
      3. No language words (catches '@#:5:5:6:6:')
      4. Symbols-only string
      5. Repetitive character pattern
      6. Excessive special characters (> 30 %)
      7. Rainfall out of range
      8. Congestion out of range
      9. Weak signal (too few words + no telemetry)
     10. Contradiction (text present but all telemetry zero)
    """
    sid = session_id or str(uuid.uuid4())
    rid = run_id or str(uuid.uuid4())

    text = (social_text or "").strip()

    # 1. Empty signal
    if not text:
        return _build_early_exit(
            "invalid_signal",
            "Crisis signal is empty. No text provided.",
            sid, rid,
        )

    # 2. Too short
    if len(text) < 12:
        return _build_early_exit(
            "invalid_signal",
            f"Signal too short ({len(text)} chars). Minimum 12 characters required.",
            sid, rid,
        )

    # 3. No language words — catches '@#:5:5:6:6:', '6:5:6:6:6'
    if not _has_language_words(text, min_words=2):
        return _build_early_exit(
            "invalid_signal",
            "Signal contains no readable language words. "
            "ValidatorGate requires at least 2 meaningful words (e.g. Roman Urdu or English).",
            sid, rid,
        )

    # 4. Symbols-only
    if _is_symbols_only(text):
        return _build_early_exit(
            "invalid_signal",
            "Signal appears to be symbols or digits only — not a valid crisis description.",
            sid, rid,
        )

    # 5. Repetitive pattern
    if _has_repetitive_pattern(text):
        return _build_early_exit(
            "invalid_signal",
            "Signal contains a repetitive character pattern — not a valid crisis report.",
            sid, rid,
        )

    # 6. Excessive special chars
    ratio = _special_char_ratio(text)
    if ratio > 0.30:
        return _build_early_exit(
            "invalid_signal",
            f"Signal contains excessive special characters ({ratio:.0%}) — appears to be gibberish.",
            sid, rid,
        )

    # 7. Rainfall range
    rain = rainfall_mm if rainfall_mm is not None else 0.0
    if rain < 0 or rain > 300:
        return _build_early_exit(
            "invalid_signal",
            f"Rainfall value ({rain} mm) is out of valid range (0–300 mm).",
            sid, rid,
        )

    # 8. Congestion range
    cong = congestion_level if congestion_level is not None else 0
    if cong < 0 or cong > 10:
        return _build_early_exit(
            "invalid_signal",
            f"Congestion level ({cong}) must be 0–10.",
            sid, rid,
        )

    # 9. Weak signal
    word_count = len([w for w in text.split() if len(w) >= 3])
    if word_count < 3 and rain <= 0 and cong <= 1:
        return _build_early_exit(
            "requires_operator_review",
            "Signal is too weak: fewer than 3 meaningful words and no supporting telemetry. "
            "Flagged for operator review.",
            sid, rid,
            validation_label="Review",
            requires_approval=True,
        )

    # 10. Contradiction — text present but all telemetry is zero
    if rain <= 0 and cong <= 0:
        return _build_early_exit(
            "requires_operator_review",
            "Telemetry contradiction: social signal present but rainfall=0 and congestion=0. "
            "Cannot confirm without corroborating telemetry.",
            sid, rid,
            validation_label="Review",
            requires_approval=True,
        )

    # All checks passed
    return None
