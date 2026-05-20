# CIRO — Google Drive Folder Structure for Submission

> **Purpose:** Organize all submission materials in a clean Drive folder

---

## Recommended Folder Structure

```
📁 CIRO-AISeekho-2026/
│
├── 📁 01-Videos/
│   ├── CIRO-Demo-Video.mp4
│   └── CIRO-Antigravity-Usage.mp4
│
├── 📁 02-Source-Code/
│   └── [GitHub repository link — paste in README or separate text file]
│
├── 📁 03-Mobile-App/
│   └── CIRO-Mobile-Demo.apk (when built)
│
├── 📁 04-Documentation/
│   ├── README.md
│   ├── CIRO-One-Pager.pdf (export from one-page-project-summary.md)
│   └── MOBILE_INSTALL.md
│
├── 📁 05-Evidence-Pack/
│   ├── health-response.json
│   ├── simulate-response.json
│   ├── false-positive-response.json
│   ├── weak-signal-response.json
│   ├── contradiction-response.json
│   ├── missing-telemetry-fallback.json
│   ├── firestore-incident-sample.json
│   ├── cost-latency-scaling.md
│   ├── demo-script.md
│   ├── mobile-app-proof.md
│   └── screenshot-checklist.md
│
├── 📁 06-Antigravity-Traces/
│   ├── CIRO-Antigravity-Traces.zip
│   └── [OR individual .md files from trace pack]
│
├── 📁 07-Screenshots/
│   ├── screenshot-request.png
│   ├── screenshot-response.png
│   ├── screenshot-swagger.png
│   └── [Additional screenshots per checklist]
│
└── 📄 SUBMISSION-README.txt
    └── Links to GitHub repo, videos, and quick description
```

---

## Folder Descriptions

| Folder | Contents | Priority |
|---|---|---|
| `01-Videos/` | Demo video (3-5 min) + Antigravity usage video (2-3 min) | **Required** |
| `02-Source-Code/` | GitHub link or source ZIP | **Required** |
| `03-Mobile-App/` | Android APK | Recommended |
| `04-Documentation/` | README, one-pager, build instructions | **Required** |
| `05-Evidence-Pack/` | JSON responses + documentation | **Required** |
| `06-Antigravity-Traces/` | Trace pack ZIP or individual files | **Required** |
| `07-Screenshots/` | Dashboard and API screenshots | Recommended |

---

## Sharing Settings

1. Set folder to **"Anyone with the link can view"**
2. Verify all files are accessible (not just the folder)
3. Test the link in an incognito browser window
4. Include the Drive link in the submission form

---

## SUBMISSION-README.txt Content

```
CIRO — Crisis Intelligence & Response Orchestrator
AISeekho 2026 — Challenge 3

Team: Syed Muhammad Saad (Lead), Farheen, Arisha, Areeba

GitHub: [Insert URL]
Demo Video: See 01-Videos/CIRO-Demo-Video.mp4
Antigravity Video: See 01-Videos/CIRO-Antigravity-Usage.mp4
README: See 04-Documentation/README.md
Evidence: See 05-Evidence-Pack/
Traces: See 06-Antigravity-Traces/

Built with Google Antigravity + Google Gemini 3 Flash-Preview.
```
