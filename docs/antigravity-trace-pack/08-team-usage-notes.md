# 08 — Team Usage Notes

> **Project:** CIRO — Crisis Intelligence & Response Orchestrator
> **Scope:** How each team member utilized Google Antigravity during development

---

## Syed Muhammad Saad — Team Lead & Principal Cloud Architect

### Antigravity Usage Areas
- **Backend architecture design:** Antigravity planned the FastAPI project structure, module organization, and async patterns
- **Cloud configuration:** Firestore database setup, credential management, environment variable design
- **Firestore service layer:** `services/firestore_service.py` with dual-mode storage (Firestore + in-memory fallback)
- **Deployment planning:** Uvicorn server configuration, CORS middleware, static file serving
- **Security hardening:** `.gitignore` rules, `.env.example` template, credential path configuration
- **API design:** REST endpoint structure, request/response models, Swagger documentation

### Key Files Touched
- `main.py`
- `core/config.py`
- `services/firestore_service.py`
- `api/routes.py`
- `api/websocket.py`
- `.env`, `.env.example`, `.gitignore`
- `requirements.txt`

### Antigravity Value
Antigravity accelerated the backend setup from estimated 2-3 days to under 4 hours. The Firestore integration, in particular, benefited from Antigravity's knowledge of the `database_id` parameter — a fix that would have required significant debugging time to discover manually.

---

## Farheen — Lead AI Core Engineer

### Antigravity Usage Areas
- **Agent prompt engineering:** System prompts for SifterAgent, StrategistAgent, and CommanderAgent
- **Gemini integration:** `google.genai.Client` setup, model selection (`gemini-3-flash-preview`), response parsing
- **Signal fusion logic:** Multi-source scoring algorithm in `SifterAgent._deterministic_analysis()`
- **ValidatorGate design:** Structural validation rules for false alarm, contradiction, and weak signal detection
- **Fallback architecture:** Deterministic logic in every agent for Gemini-unavailable scenarios
- **Roman Urdu parsing:** Social signal keyword matching and scoring in `social_signal_tool.py`

### Key Files Touched
- `agents/sifter_agent.py`
- `agents/strategist_agent.py`
- `agents/commander_agent.py`
- `core/orchestrator.py`
- `tools/social_signal_tool.py`
- `tools/weather_tool.py`
- `tools/traffic_tool.py`

### Antigravity Value
Antigravity's ability to generate complete agent classes with both Gemini and deterministic paths saved significant development time. The prompt engineering workflow — where Antigravity generated system prompts, tested them against sample inputs, and iterated — was particularly efficient.

---

## Arisha — Lead UI/UX Designer

### Antigravity Usage Areas
- **Dashboard CSS architecture:** CSS custom properties for dark ops theme, responsive layouts
- **Mobile viewport optimization:** 390×844 device frame, touch-friendly navigation
- **Animation system:** CSS keyframe animations for status transitions, blinking indicators
- **Screen navigation:** 5-screen tab system with smooth opacity transitions
- **Color-coded agent traces:** Per-agent color mapping (Sifter=blue, Strategist=orange, etc.)
- **KPI card design:** Orbitron font counters, progress bars, delta indicators

### Key Files Touched
- `static/index.html` (CSS sections)
- CSS custom properties (`:root` variables)
- Bottom navigation component
- Map overlay and marker styling

### Antigravity Value
Antigravity generated the complete CSS architecture including the custom property system, responsive breakpoints, and animation keyframes. The military/ops aesthetic was achieved through Antigravity's coordinated color palette design — a task that would have required multiple design iterations.

---

## Areeba — Technical Communications & Media Lead

### Antigravity Usage Areas
- **README authoring:** 21-section README with tables, Mermaid diagrams, and testing matrix
- **Demo script writing:** Structured demo scripts with timing and shotlists
- **Evidence documentation:** JSON evidence files with realistic pipeline responses
- **Screenshot checklist:** Systematic guide for capturing demo screenshots
- **Submission documentation:** Form answer drafts, file naming guides, Drive folder maps
- **Trace pack organization:** Structured documentation of Antigravity's development role

### Key Files Touched
- `README.md`
- `docs/evidence/*.json`
- `docs/evidence/*.md`
- `docs/antigravity-trace-pack/*.md`
- `docs/final-submission-checklist.md`

### Antigravity Value
Antigravity's documentation generation capability was critical for the evidence pack — producing 20+ evidence files that accurately reflect the system's behavior. The README, in particular, benefited from Antigravity's ability to generate comprehensive technical documentation that matches the actual codebase.

---

## Cross-Cutting Usage Patterns

### Pattern 1: Generate → Test → Fix → Harden
Every team member followed a similar workflow:
1. Describe the requirement to Antigravity
2. Antigravity generates initial implementation
3. Test the implementation against real scenarios
4. Report failures back to Antigravity
5. Antigravity generates fixes and hardening

### Pattern 2: Parallel Workstreams
Antigravity enabled parallel development by generating complete modules that could be integrated:
- Saad: Backend infrastructure (independent of agent logic)
- Farheen: Agent pipeline (independent of frontend)
- Arisha: Dashboard CSS (independent of backend API)
- Areeba: Documentation (captures output of all other streams)

### Pattern 3: Evidence as Code
Rather than manually testing and screenshotting, Antigravity generated evidence files programmatically — ensuring consistency between the documented behavior and the actual system.
