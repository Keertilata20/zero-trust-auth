from flask import Flask, render_template, request, jsonify, redirect, session
from risk_engine import calculate_risk
import time
import json
import os

app = Flask(__name__)
app.secret_key = "zero_trust_secret"

# ---------------- GLOBAL STATE ----------------

current_risk = "Trusted"
learning_until = 0
grace_until = 0

learning_data = {
    "keystrokes": [],
    "mouse": []
}

BASELINE_PATH = "data/baseline.json"

# ---------------- ROUTES ----------------

@app.route('/', methods=['GET', 'POST'])
def login():
    global learning_until, current_risk, learning_data

    if request.method == 'POST':
        session['user'] = request.form['username']

        # Reset learning data
        learning_data = {"keystrokes": [], "mouse": []}

        # Start learning phase (5 seconds)
        learning_until = time.time() + 5
        current_risk = "Learning"

        return redirect('/dashboard')

    return render_template('login.html')


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


# ---------------- BEHAVIOR ENGINE ----------------

@app.route('/behavior', methods=['POST'])
def behavior():
    global current_risk, grace_until, learning_until, learning_data

    if 'user' not in session:
        return jsonify({"risk": "No session"})

    data = request.json
    keystrokes = data.get("keystrokes", [])
    mouse = data.get("mouse", [])

    # ---------------- LEARNING PHASE ----------------
    if time.time() < learning_until:
        learning_data["keystrokes"].extend(keystrokes)
        learning_data["mouse"].extend(mouse)
        current_risk = "Learning"
        return jsonify({"risk": "Learning"})

    # After learning ends → build baseline once
    if learning_data["keystrokes"] and learning_data["mouse"]:

        os.makedirs("data", exist_ok=True)

        baseline = {
            "keystroke_avg": sum(learning_data["keystrokes"]) / len(learning_data["keystrokes"]),
            "mouse_avg": sum(learning_data["mouse"]) / len(learning_data["mouse"])
        }

        with open(BASELINE_PATH, "w") as f:
            json.dump(baseline, f)

        learning_data = {"keystrokes": [], "mouse": []}
        current_risk = "Trusted"
        return jsonify({"risk": "Trusted"})

    # ---------------- GRACE PERIOD ----------------
    if time.time() < grace_until:
        return jsonify({"risk": "Trusted"})

    # ---------------- NORMAL RISK EVALUATION ----------------
    current_risk = calculate_risk(keystrokes, mouse)
    return jsonify({"risk": current_risk})


@app.route('/status')
def status():
    return jsonify({"risk": current_risk})


@app.route('/reset')
def reset():
    global current_risk, grace_until

    current_risk = "Trusted"
    grace_until = time.time() + 5  # short trust window

    return jsonify({"status": "reset"})


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))