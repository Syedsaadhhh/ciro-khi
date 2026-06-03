from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid

from models.action import SimulateRequest
from models.incident import SignalInput
from core.orchestrator import FloodOrchestrator
from core.signal_validator import validate_signal_input
from services.firestore_service import (
    get_all_incidents, get_all_alerts, get_all_traces, get_memory_store_summary
)
from tools.social_signal_tool import get_mock_posts

router = APIRouter()
orchestrator = FloodOrchestrator()


@router.get("/incidents")
async def get_incidents():
    """Return all detected flooding incidents."""
    incidents = await get_all_incidents()
    return {"count": len(incidents), "incidents": incidents}


@router.get("/alerts")
async def get_alerts():
    """Return all generated emergency alerts."""
    alerts = await get_all_alerts()
    return {"count": len(alerts), "alerts": alerts}


@router.get("/traces")
async def get_traces():
    """Return all agent reasoning traces."""
    traces = await get_all_traces()
    return {"count": len(traces), "traces": traces}


@router.post("/simulate")
async def simulate(request: SimulateRequest):
    """
    Trigger a full multi-agent workflow simulation.

    Phase 1 reliability upgrade:
    1. Validate raw signal input BEFORE entering the orchestrator pipeline.
       Invalid/gibberish input is rejected here and never reaches Sifter/Gemini.
    2. Returns a structured CIRO decision schema for all outcomes.
    3. Adds session_id and run_id to every response for frontend state tracking.
    """
    session_id = str(uuid.uuid4())
    run_id = str(uuid.uuid4())

    # ── Step 1: Backend input validation ────────────────────────────────
    # Determine if this is user-entered text or a mock/demo fallback
    social_is_user_entered = bool(request.social_posts)
    social_text = (request.social_posts[0] if request.social_posts else None)

    early_exit = validate_signal_input(
        social_text=social_text,
        rainfall_mm=request.rainfall_mm,
        congestion_level=request.congestion_level,
        session_id=session_id,
        run_id=run_id,
    )

    if early_exit is not None:
        # Input failed validation — return structured error, never run pipeline
        return {
            "session_id": session_id,
            "run_id": run_id,
            "status": early_exit["status"],
            "result": early_exit,
            "reasoning_trace": [
                {
                    "agent": "SignalValidator",
                    "message": f"Pre-pipeline validation failed: {early_exit['reason']}",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "errors": [],
        }

    # ── Step 2: Build SignalInput and run orchestrator ───────────────────
    posts = request.social_posts or get_mock_posts(request.location)

    signal_input = SignalInput(
        location=request.location,
        social_posts=posts,
        precipitation_mm=request.rainfall_mm,
    )
    if request.congestion_level is not None:
        signal_input.traffic_data = {"congestion_level": request.congestion_level}

    result = await orchestrator.run_workflow(
        signal_input,
        session_id=session_id,
        run_id=run_id,
        social_is_user_entered=social_is_user_entered,
    )
    return result


@router.get("/live-status")
async def live_status():
    """System health and current agent state."""
    from core.config import get_settings
    store_summary = get_memory_store_summary()
    store_summary["simulation_mode"] = get_settings().simulation_mode
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "system": "Karachi Flood Command Center",
        "agents": ["sifter", "strategist", "validator", "commander"],
        "store": store_summary,
        "simulation_mode": get_settings().simulation_mode,
        "websocket_connections": 0,
    }
