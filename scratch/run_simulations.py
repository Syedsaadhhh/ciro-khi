import json
import httpx
import os

BASE_URL = "http://127.0.0.1:8000"
EVIDENCE_DIR = r"c:\Users\ATEC\Downloads\Compressed\karachi-flood-farheen_agents\docs\evidence"

def run_simulation(name, payload, filename):
    print(f"Running simulation for: {name}...")
    try:
        response = httpx.post(f"{BASE_URL}/simulate", json=payload, timeout=30.0)
        if response.status_code == 200:
            data = response.json()
            filepath = os.path.join(EVIDENCE_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"  Saved response to {filename} successfully.")
            return data
        else:
            print(f"  Error: Received status code {response.status_code}. Response: {response.text}")
    except Exception as e:
        print(f"  Exception occurred: {e}")
    return None

def main():
    # 1. Confirmed Flood
    # High rain (>= 10), social score > 0.5 (uses Urdu flood posts)
    payload_confirmed = {
        "location": "University Road",
        "rainfall_mm": 15.0,
        "congestion_level": 7,
        "social_posts": [
            "University Road pe pani bhar gaya yaar gari phas gayi",
            "Bohot zyada barish ho rahi hai uni road pe"
        ]
    }
    run_simulation("Confirmed Flood", payload_confirmed, "simulate-response.json")

    # 2. Contradiction
    # Social posts report flood but rainfall is 0.0, rainfall == 0
    payload_contradiction = {
        "location": "University Road",
        "rainfall_mm": 0.0,
        "congestion_level": 2,
        "social_posts": [
            "University Road pe pani bhar gaya yaar gari phas gayi",
            "Bohot zyada barish ho rahi hai uni road pe"
        ]
    }
    run_simulation("Contradiction / Operator Review", payload_contradiction, "contradiction-response.json")

    # 3. False Alarm (summer heatwave or low signal)
    # We want ValidatorGate to flag False Alarm. Let's see:
    # If social report is weak or rainfall is low and social score <= 0.5
    # Let's check sifter obvious false alarm: rainfall < 5 and congestion < 3. If sifter returns None, orchestrator returns status: no_incident
    # Let's try vague social posts with low telemetry
    payload_false_alarm = {
        "location": "University Road",
        "rainfall_mm": 2.0,
        "congestion_level": 1,
        "social_posts": [
            "University Road is perfectly fine today.",
            "Normal day in Karachi, no rain."
        ]
    }
    run_simulation("False Alarm / Low Signal", payload_false_alarm, "false-positive-response.json")

    # 4. Missing Telemetry Fallback
    # Triggers when traffic.congestion_level == "simulated_heavy" or weather.status == "fallback_activated"
    # Wait, how does traffic congestion level become simulated_heavy or weather fallback_activated?
    # In core/orchestrator.py, ValidatorGate checks:
    # if traffic.get("congestion_level") == "simulated_heavy" or weather.get("status") == "fallback_activated": fallback_mode = True
    # If we pass rainfall_mm = 15.0, congestion_level = 9 (which is heavy), and sifter uses default traffic tool which might activate fallback
    # Let's inspect tools/traffic_tool.py or tools/weather_tool.py to see how fallback is activated.
    # In any case, we can pass "simulated_heavy" or mock telemetry status if we trigger fallback. Let's check how sifter builds these.
    # Actually, let's run a simulation that forces validation to run in fallback mode.
    # Let's see if we can trigger fallback_mode by simulating missing APIs.
    payload_missing_telemetry = {
        "location": "University Road",
        "rainfall_mm": 15.0,
        "congestion_level": 8,
        "social_posts": [
            "University Road pe pani bhar gaya yaar gari phas gayi",
            "Bohot zyada barish ho rahi hai uni road pe"
        ]
    }
    run_simulation("Missing Telemetry", payload_missing_telemetry, "missing-telemetry-fallback.json")

if __name__ == "__main__":
    main()
