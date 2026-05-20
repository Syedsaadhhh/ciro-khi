import uuid
import asyncio
import structlog
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

from core.state import WorkflowState
from core.config import get_settings
from agents.sifter_agent import SifterAgent
from agents.strategist_agent import StrategistAgent
from agents.commander_agent import CommanderAgent
from models.incident import SignalInput, IncidentModel
from models.action import ActionModel
from services.firestore_service import (
    save_incident, save_plan, save_alert, save_trace, log_agent_event
)
from services.websocket_service import ws_manager

logger = structlog.get_logger()
settings = get_settings()


class FloodOrchestrator:
    """
    Orchestrates the multi-agent workflow:
    Sifter → Strategist → Validator → Commander

    Manages state, retries, trace logging, and real-time WebSocket broadcasts.
    Follows Google ADK multi-agent coordination patterns.
    """

    def __init__(self):
        self.sifter = SifterAgent()
        self.strategist = StrategistAgent()
        self.commander = CommanderAgent()

    async def run_workflow(self, signal_input: SignalInput) -> dict:
        session_id = str(uuid.uuid4())
        state = WorkflowState(session_id=session_id)

        logger.info("workflow_started",
            session_id=session_id,
            location=signal_input.location,
        )

        await ws_manager.broadcast_status("started", session_id)
        state.add_trace("Orchestrator", f"Workflow started for {signal_input.location}")

        try:
            result = await self._execute_with_retry(signal_input, state)
            state.status = "completed"
            await ws_manager.broadcast_status("completed", session_id)

        except Exception as e:
            state.status = "failed"
            state.add_error("Orchestrator", str(e))
            logger.error("workflow_failed", session_id=session_id, error=str(e))
            await ws_manager.broadcast_status("failed", session_id)
            result = {"status": "failed", "session_id": session_id, "error": str(e)}

        # Persist full trace
        await save_trace(state)
        await log_agent_event("Orchestrator", "workflow_complete", {
            "session_id": session_id,
            "status": state.status,
            "trace_count": len(state.reasoning_trace),
        })

        return {
            "session_id": session_id,
            "status": state.status,
            "result": result,
            "reasoning_trace": state.reasoning_trace,
            "errors": state.errors,
        }

    async def _execute_with_retry(self, signal_input: SignalInput, state: WorkflowState) -> dict:
        while state.retry_count <= state.max_retries:
            try:
                return await self._pipeline(signal_input, state)
            except Exception as e:
                state.retry_count += 1
                state.add_error(state.current_agent, str(e))
                state.add_trace("Orchestrator",
                    f"Retry {state.retry_count}/{state.max_retries} after error: {str(e)}"
                )
                logger.warning("pipeline_retry",
                    attempt=state.retry_count,
                    agent=state.current_agent,
                    error=str(e),
                )
                if state.retry_count > state.max_retries:
                    raise
                await asyncio.sleep(0.5 * state.retry_count)

        raise RuntimeError("Max retries exceeded")

    async def _pipeline(self, signal_input: SignalInput, state: WorkflowState) -> dict:
        # ─── STAGE 1: SIFTER ─────────────────────────────────────────────
        state.add_trace("Orchestrator", "Routing to Sifter Agent")
        await ws_manager.broadcast_trace("Orchestrator", "Routing to Sifter Agent")

        incident = await self.sifter.run(signal_input, state)

        # Broadcast sifter traces
        for trace in state.reasoning_trace[-5:]:
            if trace["agent"] == "Sifter":
                await ws_manager.broadcast_trace(trace["agent"], trace["message"])

        if incident is None:
            state.add_trace("Orchestrator", "No incident detected. Workflow terminated early.")
            await ws_manager.broadcast_trace("Orchestrator",
                f"No incident detected at {signal_input.location}. Classified as false alarm."
            )
            return {
                "status": "no_incident",
                "location": signal_input.location,
                "message": "No crisis detected at this location.",
            }

        await save_incident(incident.model_dump())
        await ws_manager.broadcast_incident(incident.model_dump())
        state.add_trace("Orchestrator",
            f"Incident confirmed: {incident.incident_id[:8]} | Routing to Strategist"
        )

        # ─── STAGE 2: STRATEGIST ──────────────────────────────────────────────
        await ws_manager.broadcast_status("validating", state.session_id)
        await ws_manager.broadcast_trace("Orchestrator", "Routing to Strategist Agent")

        plan = await self.strategist.run(incident, state)

        for trace in state.reasoning_trace[-8:]:
            if trace["agent"] == "Strategist":
                await ws_manager.broadcast_trace(trace["agent"], trace["message"])

        if plan is None or not plan.validated:
            state.add_trace("Orchestrator",
                f"Incident invalidated by Strategist: {plan.rejected_reason if plan else 'unknown'}"
            )
            await ws_manager.broadcast_trace("Orchestrator",
                f"Incident rejected by Strategist: {plan.rejected_reason if plan else 'validation failed'}"
            )
            return {
                "status": "rejected",
                "incident_id": incident.incident_id,
                "reason": plan.rejected_reason if plan else "validation failed",
            }

        await save_plan(plan.model_dump())

        state.add_trace("Orchestrator",
            f"Plan approved: {plan.priority.upper()} priority | Routing to Validator"
        )

        # ─── VALIDATION GATEWAY ───────────────────────────────────────────
        validation_result = await self.run_validator_gate(incident, state)
        
        for trace in state.reasoning_trace[-4:]:
            if trace["agent"] == "ValidatorGate":
                await ws_manager.broadcast_trace(trace["agent"], trace["message"])

        if validation_result.get("fallback_mode"):
            await ws_manager.broadcast_status("mock_fallback", state.session_id)
        
        if validation_result.get("requires_review"):
            await ws_manager.broadcast_status("under_review", state.session_id)
            return {
                "status": "requires_operator_review",
                "incident_id": incident.incident_id,
                "reason": validation_result.get("reason"),
            }

        if not validation_result.get("validated"):
            await ws_manager.broadcast_status("rejected", state.session_id)
            return {
                "status": "rejected_by_validator",
                "incident_id": incident.incident_id,
                "reason": validation_result.get("reason", "False Alarm caught by validation gateway"),
            }

        # ─── STAGE 3: COMMANDER ─────────────────────────────────────────────
        if not validation_result.get("fallback_mode"):
            await ws_manager.broadcast_status("confirmed", state.session_id)
            
        await ws_manager.broadcast_trace("Orchestrator", "Routing to Commander Agent")

        action = await self.commander.run(incident, plan, state)

        for trace in state.reasoning_trace[-6:]:
            if trace["agent"] == "Commander":
                await ws_manager.broadcast_trace(trace["agent"], trace["message"])

        # Build alert object for storage
        alert_record = {
            "incident_id": incident.incident_id,
            "message": action.alert_message,
            "severity": incident.severity,
            "location": incident.location,
            "actions": action.actions,
            "channels": action.alert_channels,
            "ticket_id": action.ticket_id,
            "geofence_km": action.geofence_radius_km,
            "created_at": action.executed_at,
        }
        await save_alert(alert_record)
        await ws_manager.broadcast_alert(alert_record)
        await ws_manager.broadcast_status("response recommended", state.session_id)

        state.add_trace("Orchestrator", "Workflow pipeline complete. All agents finished.")

        return {
            "status": "completed",
            "incident": incident.model_dump(),
            "plan": plan.model_dump(),
            "action": action.model_dump(),
            "safety_validation": validation_result,
        }

    async def run_validator_gate(self, incident: IncidentModel, state: WorkflowState) -> dict:
        """
        Structural validation method to catch false alarms and handle degraded modes.
        """
        state.add_trace("ValidatorGate", "Running structural validation to catch false alarms")
        
        raw_signals = incident.raw_signals or {}
        weather = raw_signals.get("weather", {})
        social = raw_signals.get("social", {})
        traffic = raw_signals.get("traffic", {})
        
        social_score = social.get("aggregate_score", 0)
        rainfall = weather.get("rainfall_mm", 0)
        temperature = incident.temperature_c or weather.get("temperature", 30)

        fallback_mode = False
        if traffic.get("congestion_level") == "simulated_heavy" or weather.get("status") == "fallback_activated":
            fallback_mode = True
            state.add_trace("ValidatorGate", "Telemetry API unavailable. Running in Mock Fallback Mode.")

        if incident.event_type in ["monsoon_flooding", "urban_flood"]:
            if social_score > 0.5 and rainfall >= 10:
                state.add_trace("ValidatorGate", "Strong signal and telemetry match. Validation passed.")
                return {"validated": True, "requires_review": False, "fallback_mode": fallback_mode, "reason": "Confirmed"}
                
            if social_score > 0.5 and rainfall == 0:
                state.add_trace("ValidatorGate", "Contradiction: Social reports flood but 0mm rainfall. Flagging for Operator Review.")
                return {"validated": False, "requires_review": True, "fallback_mode": fallback_mode, "reason": "Contradiction: Social signal high but telemetry reports no rain."}
                
            if social_score <= 0.5 and rainfall < 10:
                state.add_trace("ValidatorGate", "Weak signal detected. Needs manual review.")
                return {"validated": False, "requires_review": True, "fallback_mode": fallback_mode, "reason": "Weak signal: Low sentiment and telemetry."}

        # check summer heatwave false alarm
        if incident.event_type == "summer_heatwave_power_failure" and social_score > 0.5 and temperature < 35:
            state.add_trace("ValidatorGate", "Validation error trace log: Social says crisis but temperature is low. Flagging False Alarm.")
            return {"validated": False, "requires_review": False, "fallback_mode": fallback_mode, "reason": "False Alarm"}

        state.add_trace("ValidatorGate", "Validation passed.")
        return {"validated": True, "requires_review": False, "fallback_mode": fallback_mode, "reason": "Confirmed"}
