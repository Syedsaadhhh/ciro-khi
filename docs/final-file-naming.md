# CIRO — Final File Naming Guide

> **Purpose:** Expected file names for AISeekho 2026 submission

---

## Required Submission Files

| File Name | Type | Description | Status |
|---|---|---|---|
| `CIRO-Demo-Video.mp4` | Video | 3-5 minute demo recording | 📝 Script ready |
| `CIRO-Antigravity-Usage.mp4` | Video | 2-3 minute Antigravity usage recording | 📝 Script ready |
| `CIRO-Antigravity-Traces.zip` | Archive | Antigravity trace pack (14 files) | ✅ Ready to package |
| `README.md` | Document | Judge-ready project documentation | ✅ Complete |

---

## Optional/Recommended Files

| File Name | Type | Description | Status |
|---|---|---|---|
| `CIRO-Mobile-Demo.apk` | Android | Mobile app package | ⏳ Build pending |
| `CIRO-One-Pager.pdf` | Document | One-page project summary (exported from MD) | ✅ Content ready |
| `CIRO-Screenshots.zip` | Archive | Dashboard and API screenshots | 📝 Checklist ready |

---

## Source Code

| Location | Description |
|---|---|
| GitHub repository | Complete source code (link in submission form) |
| `main.py` | FastAPI entry point |
| `agents/` | SifterAgent, StrategistAgent, CommanderAgent |
| `core/` | Orchestrator, config, state |
| `tools/` | Weather, traffic, social, geofence, reroute, alert tools |
| `services/` | Firestore and WebSocket services |
| `models/` | Pydantic data models |
| `static/` | Dashboard SPA |
| `docs/` | Evidence pack + submission docs |

---

## Naming Conventions

- **Project prefix:** `CIRO-` for all submission files
- **No spaces:** Use hyphens for multi-word names
- **Descriptive:** File name should indicate content at a glance
- **Version-free:** No version numbers in file names (submission is final)

---

## ZIP Archive Contents

### CIRO-Antigravity-Traces.zip
```
antigravity-trace-pack/
├── 01-main-orchestrator-proof.md
├── 02-implementation-plan.md
├── 03-task-list.md
├── 04-walkthrough.md
├── 05-agent-observations.md
├── 06-error-recovery-log.md
├── 07-final-outcomes.md
├── 08-team-usage-notes.md
├── 09-submission-readiness.md
├── ZIP_README.md
└── team/
    ├── saad-backend-cloud-tasks.md
    ├── farheen-ai-agent-tasks.md
    ├── arisha-uiux-tasks.md
    └── areeba-documentation-tasks.md
```
