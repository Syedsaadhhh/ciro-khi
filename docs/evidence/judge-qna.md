# CIRO - Judge Q&A Cheat Sheet

**Q: "If someone spams fake social media posts, won't your system deploy fire trucks for no reason?"**
**A:** "No. This is exactly why we built the `ValidatorGate`. Our architecture does not trigger based purely on social noise. The Strategist and Sifter agents cross-reference social sentiment with hard telemetry (like Meteosource API rainfall and TomTom traffic data). If the system detects high distress on Twitter but 0mm of rainfall, the Validator explicitly rejects the workflow as a False Alarm. You can see this logic in `docs/evidence/false-positive-response.json`."

**Q: "What happens if your traffic or weather APIs go down or you run out of credits during a crisis?"**
**A:** "We engineered CIRO with Graceful Fallbacks. If an environment variable is missing or a 500 error is caught from TomTom, the specific tool class (`tools/traffic_tool.py`) automatically intercepts the traceback and returns a locally structured 'simulated_heavy' JSON payload. This ensures the orchestrator never crashes and the crisis pipeline completes."

**Q: "How are you updating the frontend without React or complex state management?"**
**A:** "We utilized vanilla JavaScript mapped securely to two distinct real-time pipelines. 
1. The WebSocket (`/ws/live-trace`) actively streams the internal agent reasoning to a terminal DOM element and uses Regex to inject live math into the scorecards.
2. Google Firebase Firestore's `onSnapshot` listener passively watches the `incidents` collection, triggering organic Google Map UI `.panTo()` events the second the backend Commander commits an alert."

**Q: "How did Google Antigravity help you?"**
**A:** "Antigravity acted as our Principal Architect. We focused on the product logic and design logic, while Antigravity executed the repository restructuring, Python dependency management, complex WebSocket trace debugging, and implemented the explicit Firestore database routing logic perfectly across the environment variables."
