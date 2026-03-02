from flask import Flask, render_template, request, jsonify
from risk_engine import calculate_risk

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/behavior', methods=['POST'])
def behavior():
    data = request.json
    keystrokes = data.get("keystrokes", [])
    mouse = data.get("mouse", [])

    risk = calculate_risk(keystrokes, mouse)

    return jsonify({"risk": risk})

if __name__ == "__main__":
    app.run(debug=True)
