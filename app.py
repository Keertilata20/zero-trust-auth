from flask import Flask, render_template, request, jsonify, redirect, session
from risk_engine import calculate_risk
import time

app = Flask(__name__)
app.secret_key = "zero_trust_secret"

current_risk = "Trusted"
learning_until = 0
grace_until = 0


@app.route('/', methods=['GET', 'POST'])
def login():
    global learning_until, current_risk

    if request.method == 'POST':
        session['user'] = request.form['username']

        # Start short learning phase
        learning_until = time.time() + 3
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


@app.route('/behavior', methods=['POST'])
def behavior():
    global current_risk, grace_until

    if 'user' not in session:
        return jsonify({"risk": "No session"})

    # Grace period after reverify
    if time.time() < grace_until:
        return jsonify({"risk": "Trusted"})

    data = request.json
    keystrokes = data.get("keystrokes", [])
    mouse = data.get("mouse", [])

    current_risk = calculate_risk(keystrokes, mouse)

    return jsonify({"risk": current_risk})


@app.route('/status')
def status():
    global current_risk, learning_until

    # If learning time expired, move to Trusted automatically
    if current_risk == "Learning" and time.time() > learning_until:
        current_risk = "Trusted"

    return jsonify({"risk": current_risk})


@app.route('/reset')
def reset():
    global current_risk, grace_until

    current_risk = "Trusted"
    grace_until = time.time() + 5

    return jsonify({"status": "reset"})


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))