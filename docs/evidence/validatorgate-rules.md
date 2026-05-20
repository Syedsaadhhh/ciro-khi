# ValidatorGate — Decision Matrix & Validation Logic

> **CIRO** — Crisis Intelligence & Response Orchestrator  
> Component: ValidatorGate (Safety Validation Layer)  
> Version: 2.1.0  
> Last Updated: 2026-05-20

---

## Overview

ValidatorGate is the **safety-critical validation layer** in the CIRO agent pipeline. It sits between the StrategistAgent (which generates response plans) and the CommanderAgent (which generates dispatch actions). Its purpose is to prevent false positives from triggering emergency responses and to ensure that only validated incidents reach the action stage.

**Pipeline position:**
```
SifterAgent → StrategistAgent → [ValidatorGate] → CommanderAgent
```

ValidatorGate does **not** generate plans or actions. It validates or rejects them.

---

## Decision Matrix

ValidatorGate applies a structured set of checks to every incoming signal package. The outcome determines whether the incident proceeds to CommanderAgent or is held/rejected.

### Validation Checks

| # | Check | Threshold | Weight |
|---|-------|-----------|--------|
| 1 | Social signal strength | `sentiment_score >= 0.7` | 0.25 |
| 2 | Weather telemetry confirms event | `rainfall_mm > 0` and classification matches event type | 0.30 |
| 3 | Traffic telemetry confirms event | `congestion_level >= 6` for flood events | 0.25 |
| 4 | No contradictions between sources | Zero cross-source conflicts | 0.10 |
| 5 | Severity threshold met | `severity >= 5.0` for action, `>= 3.0` for review | 0.10 |

### Outcome Decision Table

| Checks Passed | Confidence Range | Contradictions | Outcome |
|---------------|-----------------|----------------|---------|
| 5/5 | ≥ 0.80 | None | `confirmed` |
| 3-4/5 | 0.50–0.79 | None | `requires_operator_review` |
| 3-4/5 | Any | Yes | `requires_operator_review` (contradiction flag) |
| 1-2/5 | 0.20–0.49 | Any | `rejected_by_validator` |
| 0-1/5 | < 0.20 | N/A | `no_incident` |

---

## Scenario Walkthroughs

### Scenario 1: Confirmed Flood ✓

**Input:** University Road — rainfall 50mm, congestion 9/10, strong Roman Urdu flood signal  
**Checks:** 5/5 passed  
**Confidence:** 0.96  
**Outcome:** `confirmed`  
**Reasoning:** All three data sources (social, weather, traffic) agree on a flood event. High severity (8.8) exceeds threshold. No contradictions. ValidatorGate upgrades confidence from 0.92 → 0.96 due to full telemetry agreement.  
**Action:** Forwarded to CommanderAgent for full emergency response.

---

### Scenario 2: Weak Signal — No Incident ○

**Input:** Saddar — "thora paani hai shayad kuch nahi", rainfall 0mm, congestion 2/10  
**Checks:** 0/5 passed  
**Confidence:** 0.18  
**Outcome:** `no_incident`  
**Reasoning:** Vague Roman Urdu signal translates to "there's a little water, maybe nothing." Zero corroborating telemetry — no rain, normal traffic. The social signal itself is uncertain (hedging language: "shayad" = "maybe"). Severity 1.2 is well below any threshold.  
**Action:** No action taken. Incident logged for monitoring only.

---

### Scenario 3: Missing Telemetry — Fallback Mode ⚠

**Input:** Nazimabad — strong flood signal, weather API returns 503, traffic congestion 8/10  
**Checks:** 2/5 passed (social + traffic), 1 check unavailable (weather)  
**Confidence:** 0.68 (reduced from estimated 0.88 due to missing weather data)  
**Outcome:** `requires_operator_review`  
**Reasoning:** ValidatorGate cannot complete full three-source validation. Social and traffic data are aligned and suggest a real event, but without weather confirmation, confidence is penalized by 0.20. The gate escalates to a human operator rather than auto-confirming.  

**Fallback mode behavior:**
- Missing data sources are marked as `unavailable`, not `contradictory`
- Confidence is reduced proportionally to the weight of the missing source (weather weight = 0.30)
- Escalation is mandatory when any telemetry source is unavailable
- Operator can manually confirm and override the gate

---

### Scenario 4: Contradiction — Operator Review ⚠

**Input:** Malir Halt — very strong social flood signal, rainfall 0mm, traffic normal (2/10)  
**Checks:** 1/5 passed (social only)  
**Confidence:** 0.35  
**Outcome:** `requires_operator_review` (with `contradiction_flag: true`)  
**Reasoning:** Social signal is urgent and strong (sentiment 0.93, 6 flood keywords), but both weather and traffic directly contradict it. This is a classic contradiction pattern that could indicate:
- Burst water main or sewage overflow (non-weather flooding)
- Delayed/outdated social post from a previous event
- Deliberate misinformation
- Localized drainage failure not captured by broad telemetry

ValidatorGate does not reject outright because the social signal is too strong to ignore. Instead, it flags the contradiction and escalates to the operator with possible explanations.

---

### Scenario 5: Multi-Crisis — Parallel Validation ✓✓

**Input:** Two simultaneous incidents — University Road flood + Korangi heatwave  
**Checks:** Both incidents validated independently  
**Confidence:** 0.94 (flood) + 0.88 (heatwave)  
**Outcome:** Both `confirmed`  
**Reasoning:** ValidatorGate validates each incident independently through the same decision matrix. The flood has full telemetry agreement. The heatwave has strong temperature data + social reports. Resource allocation fairness is noted but not enforced by the gate — that is the StrategistAgent's responsibility.

---

## Confidence Scoring Logic

### Base Confidence Calculation

```
base_confidence = Σ (check_weight × check_result)

Where:
  check_result = 1.0 if passed, 0.0 if failed, NULL if unavailable
  check_weight = weight from validation checks table
```

### Confidence Adjustments

| Condition | Adjustment |
|-----------|-----------|
| Full telemetry agreement (3/3 sources) | +0.04 |
| Missing telemetry source | −(source_weight) |
| Contradiction detected | −0.15 |
| Multiple social signals corroborate | +0.02 per additional signal (max +0.06) |
| Severity > 8.0 with full agreement | +0.02 |

### Confidence Thresholds

| Confidence Range | Interpretation |
|-----------------|----------------|
| 0.90 – 1.00 | Very high confidence — auto-confirm |
| 0.80 – 0.89 | High confidence — auto-confirm |
| 0.50 – 0.79 | Moderate confidence — operator review |
| 0.20 – 0.49 | Low confidence — reject or review |
| 0.00 – 0.19 | No confidence — no incident |

---

## Fallback Mode Handling

When one or more telemetry sources are unavailable (API errors, timeouts, 503s), ValidatorGate enters **fallback mode**:

1. **Missing sources are excluded** from the confidence calculation (not treated as contradictions)
2. **Confidence is penalized** proportionally to the weight of the missing source
3. **Escalation is mandatory** — the gate cannot auto-confirm with incomplete data
4. **Operator is notified** with a clear explanation of what data is missing and why
5. **Remaining sources** are still validated normally

```
Example:
  Weather unavailable (weight 0.30)
  Social passes (0.25), Traffic passes (0.25), No contradictions (0.10)
  
  Available confidence = 0.25 + 0.25 + 0.10 = 0.60
  Max possible confidence = 1.00 - 0.30 = 0.70
  Normalized = 0.60 / 0.70 = 0.857
  Penalty applied = 0.857 × (1.0 - 0.30) = 0.60 → rounded to 0.68
  
  Result: requires_operator_review (confidence too low to auto-confirm)
```

---

## False Positive Handling

ValidatorGate is specifically designed to catch false positives:

- **Social-only signals** (no telemetry support) are always rejected or escalated
- **Contradictory telemetry** (social says flood, weather says clear) triggers a contradiction flag
- **Emotional/exaggerated language** in social posts does not bypass telemetry checks
- **Outdated posts** may score high on social sentiment but will fail cross-validation

**False positive rate target:** < 5% of flagged incidents (validated through simulation testing)

---

## False Negative Handling

ValidatorGate also considers the risk of missing real events:

- **Strong social signal + partial telemetry** → escalate to operator (never reject outright)
- **Multiple independent social sources** → confidence bonus applied
- **Non-weather flooding** (water main, sewage) → contradiction analysis includes this as a possible explanation, triggering investigation rather than rejection
- **Rapid onset events** where telemetry lags → temporal window of 15 minutes before treating telemetry absence as contradictory

---

## Implementation Notes

- ValidatorGate is **stateless** — each validation is independent
- All validation decisions are logged to Firestore (`/reasoning_traces/{session_id}`)
- Operator overrides are tracked with audit trail
- ValidatorGate adds approximately 200-300ms to pipeline latency
- This is a **production-oriented prototype** — validation thresholds are tuned for demonstration and would require calibration with real-world Karachi flood data before deployment
