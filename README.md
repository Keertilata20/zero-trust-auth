# Behavioral Zero-Trust Authentication

A continuous authentication prototype based on behavioral biometrics and dynamic risk scoring.

Traditional systems trust users after login.  This system implements a Zero Trust principle:

**Never trust once. Verify Continuously.**

Instead of relying only on passwords or tokens, the system monitors behavioral signals during a session and updates a real-time trust score.

---

## 🔐 Core Idea

User identity is validated continuously using behavioral patterns such as:

- Keystroke dynamics
- Mouse movement patterns
- Session consistency

If behavior deviates from the user's baseline, the system flags elevated risk and can trigger re-authentication.

---

## ⚙️ Working

1. User interacts normally after login
2. Behavioral signals are captured
3. A risk score is computed continuously
4. Trust level is updated dynamically
5. If trust drops → session verification required

This aligns with modern Zero Trust Architecture principles.

---

## 🧠 Risk Engine Logic

The system evaluates:

- Typing consistency
- Mouse stability
- Session deviation

Example conceptual model:

Trust Score = Behavioral Stability - Session Anomaly


Output:

- Trusted
- Monitor
- Re-Verify Required

---

## 🛠 Tech Stack

- Python (Flask)
- JavaScript (behavior tracking)
- Risk scoring engine
- JSON baseline modeling

---

## 🚀 Importance

Static authentication assumes identity remains constant.

Modern threats exploit:

- Session hijacking
- Insider compromise
- Credential reuse

Behavioral authentication introduces:

✔ Continuous trust evaluation  
✔ Passive identity validation  
✔ Reduced reliance on static credentials  

---

## 📌 Current Scope

Prototype includes:

- Real-time behavior capture
- Trust score calculation
- Risk-based session flagging

Future scope:

- Geo-risk integration
- Device fingerprinting
- ML-based anomaly detection

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
python app.py
