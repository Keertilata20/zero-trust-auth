## Zero Trust Behavioral Authentication Portal

A web-based adaptive authentication system that continuously verifies user identity using behavioral biometrics such as typing rhythm, mouse movement, and touch interaction patterns.

Traditional systems authenticate a user only at login.
This system applies continuous behavioral verification during the entire session.

The model learns a behavioral baseline and evaluates real-time interaction patterns to detect anomalies.

---

## Project Overview

This project demonstrates an implementation of Zero Trust Architecture (ZTA) principles in a web authentication environment.

Instead of trusting a user after login, the system continuously evaluates behavioral signals and determines whether the current session still matches the authenticated user.

If behavioral deviation exceeds acceptable limits, the system can shift the session to a higher risk state and require re-verification.

---

## Key Features
Continuous Behavioral Authentication

The system verifies user identity throughout the session rather than relying solely on login credentials.

Multi-Signal Behavioral Monitoring

The model analyzes interaction patterns including:

Desktop signals

Keystroke timing cadence

Mouse movement velocity

Mobile signals

Touch interval rhythm

Swipe movement distance

Learning Phase

After login, the system enters a short learning window where baseline behavioral metrics are recorded.

Adaptive Risk Evaluation

User behavior is continuously compared against the baseline to determine the trust state:

Trusted

Monitoring

Re-Verify Required

Device-Aware Authentication

The system adapts automatically to desktop and mobile interaction styles.

Real-Time Monitoring

The browser streams behavioral signals to the backend where risk evaluation occurs continuously.

System Architecture
Behavioral Authentication Pipeline
Behavioral Baseline Model

During the learning phase, the system records interaction metrics and computes average values.

## Example baseline structure:

baseline = {
  keystroke_avg,
  mouse_avg,
  touch_avg,
  touch_distance
}

Only metrics observed during the learning phase are activated for future risk evaluation.

This prevents false alerts when certain signals are absent.

Risk Evaluation

The system calculates deviation between current behavior and the baseline.

## Example concept:

risk_score = deviation(current_behavior, baseline)

Session state transitions depend on configurable thresholds:

Trusted → Monitoring → Re-Verify

The model ignores behavioral signals that were not observed during baseline learning.

## Technology Stack

 Backend

Python

Flask

 Frontend

JavaScript

HTML

CSS

 Behavioral Modeling

NumPy

Real-time behavioral signal processing

 Deployment

Render Cloud Platform

Example Baseline Output
{
  "keystroke_avg": 144.42,
  "mouse_avg": 6.19,
  "touch_avg": 0,
  "touch_distance": 0
}
Testing the System

Open the deployed portal.

Log in to start a session.

Interact normally during the learning phase.

Continue interacting to maintain a trusted session.

Sudden behavioral deviations may trigger monitoring or re-verification.

Debug endpoint:

/debug-baseline

This endpoint displays the learned behavioral baseline.

Security Concept

This project demonstrates key Zero Trust security principles:

Never trust, always verify

Continuous authentication

Behavioral anomaly detection

Session-level risk evaluation

Future Improvements

Planned extensions include:

Adaptive confidence scoring

Persistent baseline storage

Multi-user behavioral profiles

Behavioral drift adaptation

Anomaly detection dashboard

Trust score visualization

Author

Developed as an experimental implementation of continuous behavioral authentication using modern web technologies.

License

This project is intended for educational and research purposes.



