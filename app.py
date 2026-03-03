from flask import Flask, render_template, request, jsonify, redirect, session
from risk_engine import calculate_risk
import time
import json
import os

app = Flask(__name__)
app.secret_key = "zero_trust_secret"

current_risk = "Trusted"
learning_until = 0
grace_until = 0

learning_data = {
    "desktop": {"keystrokes": [], "mouse": []},
    "mobile": {"touch_avg": [], "touch_distance": []}
}

BASELINE_PATH = "data/baseline.json"


# ================================
# LOGIN
# ================================
@app.route('/', methods=['GET', 'POST'])
def login():
    global learning_until, current_risk, learning_data

    if request.method == 'POST':
        session['user'] = request.form['username']

        learning_data = {
            "desktop": {"keystrokes": [], "mouse": []},
            "mobile": {"touch_avg": [], "touch_distance": []}
        }

        learning_until = time.time() + 8
        current_risk = "Learning"

        print("Learning phase started")

        return redirect('/dashboard')

    return render_template('login.html')


# ================================
# PAGES
# ================================
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/reports')
def reports():
    return render_template('reports.html')


@app.route('/security')
def security():
    return render_template('security.html')


# ================================
# BEHAVIOR CAPTURE
# ================================
@app.route('/behavior', methods=['POST'])
def behavior():
    global current_risk, grace_until, learning_until, learning_data

    if 'user' not in session:
        return jsonify({"risk": "No session"})

    data = request.json
    device = data.get("device")

    # ---------- LEARNING PHASE ----------
    if time.time() < learning_until:

        if device == "mobile":
            learning_data["mobile"]["touch_avg"].append(data.get("touch_avg", 0))
            learning_data["mobile"]["touch_distance"].append(data.get("touch_distance", 0))
        else:
            learning_data["desktop"]["keystrokes"].extend(data.get("keystrokes", []))
            learning_data["desktop"]["mouse"].extend(data.get("mouse", []))

        current_risk = "Learning"
        return jsonify({"risk": "Learning"})

    # ---------- BUILD BASELINE ----------
    if not os.path.exists(BASELINE_PATH):

        os.makedirs("data", exist_ok=True)

        baseline = {}

        # Desktop baseline
        baseline["keystroke_avg"] = (
            sum(learning_data["desktop"]["keystrokes"]) / len(learning_data["desktop"]["keystrokes"])
            if learning_data["desktop"]["keystrokes"] else 0
        )

        baseline["mouse_avg"] = (
            sum(learning_data["desktop"]["mouse"]) / len(learning_data["desktop"]["mouse"])
            if learning_data["desktop"]["mouse"] else 0
        )

        # Mobile baseline
        baseline["touch_avg"] = (
            sum(learning_data["mobile"]["touch_avg"]) / len(learning_data["mobile"]["touch_avg"])
            if learning_data["mobile"]["touch_avg"] else 0
        )

        baseline["touch_distance"] = (
            sum(learning_data["mobile"]["touch_distance"]) / len(learning_data["mobile"]["touch_distance"])
            if learning_data["mobile"]["touch_distance"] else 0
        )

        with open(BASELINE_PATH, "w") as f:
            json.dump(baseline, f)

        print("Baseline created:", baseline)

        current_risk = "Trusted"
        return jsonify({"risk": "Trusted"})

    # ---------- GRACE PERIOD ----------
    if time.time() < grace_until:
        return jsonify({"risk": "Trusted"})

    # ---------- NORMAL RISK EVALUATION ----------
    if device == "mobile":
        current_risk = calculate_risk(
            [],
            [],
            data.get("touch_avg"),
            data.get("touch_distance")
        )
    else:
        current_risk = calculate_risk(
            data.get("keystrokes", []),
            data.get("mouse", []),
            None,
            None
        )

    return jsonify({"risk": current_risk})


# ================================
# STATUS
# ================================
@app.route('/status')
def status():
    return jsonify({"risk": current_risk})


# ================================
# DEBUG BASELINE
# ================================
@app.route("/debug-baseline")
def debug_baseline():
    if os.path.exists(BASELINE_PATH):
        with open(BASELINE_PATH, "r") as f:
            return jsonify(json.load(f))
    return jsonify({"status": "No baseline found"})


# ================================
# RESET
# ================================
@app.route('/reset')
def reset():
    global current_risk, grace_until
    current_risk = "Trusted"
    grace_until = time.time() + 5
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))