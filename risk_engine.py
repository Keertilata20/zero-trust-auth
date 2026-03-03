import json
import numpy as np
import time

BASELINE_FILE = "data/baseline.json"

def load_baseline():
    try:
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def calculate_deviation(current, baseline_avg):
    if not current or baseline_avg == 0:
        return 0
    return abs(np.mean(current) - baseline_avg)

def calculate_risk(keystrokes, mouse):
    baseline = load_baseline()

    if not baseline:
        return "Monitoring"

    key_dev = calculate_deviation(keystrokes, baseline["keystroke_avg"])
    mouse_dev = calculate_deviation(mouse, baseline["mouse_avg"])

    # Weighted risk score
    risk_score = (0.6 * key_dev) + (0.4 * mouse_dev)

    if risk_score < 20:
        return "Trusted"
    elif risk_score < 50:
        return "Monitoring"
    else:
        return "Re-Verify Required"