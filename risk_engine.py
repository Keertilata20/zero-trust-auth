import json
import numpy as np
import os

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


def calculate_risk(keystrokes, mouse, touch_avg=None, touch_distance=None):

    baseline = load_baseline()

    if not baseline:
        return "Monitoring"

    risk_score = 0
    active_metrics = 0

    # ---------------- MOBILE ----------------
    if touch_avg is not None and touch_distance is not None:

        if baseline.get("touch_avg", 0) > 0:
            risk_score += abs(touch_avg - baseline["touch_avg"])
            active_metrics += 1

        if baseline.get("touch_distance", 0) > 0:
            risk_score += abs(touch_distance - baseline["touch_distance"])
            active_metrics += 1

    # ---------------- DESKTOP ----------------
    else:

        if baseline.get("keystroke_avg", 0) > 0 and keystrokes:
            risk_score += abs(sum(keystrokes)/len(keystrokes) - baseline["keystroke_avg"])
            active_metrics += 1

        if baseline.get("mouse_avg", 0) > 0 and mouse:
            risk_score += abs(sum(mouse)/len(mouse) - baseline["mouse_avg"])
            active_metrics += 1

    # Normalize if multiple metrics active
    if active_metrics > 0:
        risk_score = risk_score / active_metrics

    # ---------------- THRESHOLDS ----------------
    if risk_score < 60:
        return "Trusted"
    elif risk_score < 150:
        return "Monitoring"
    else:
        return "Re-Verify Required"