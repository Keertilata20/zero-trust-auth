# Zero-Trust-Auth
**Continuous Authentication Engine Project**

## Featuring
- **Risk scoring**: Device + location + behavior (0-100 score)
- **Continuous authentication**: JWT refresh every 5 minutes
- **Behavioral biometrics**: Mouse & typing patterns
- **Zero Trust**: Never trust, always verify

## Risk Engine Formula
- risk_score = 0.4×device + 0.3×geo_velocity + 0.3×behavior
- High risk, **BLOCKED** - unusual IP + late hour

## Tech Stack
- Java Spring Boot
- Redis
- WebSocket biometrics

## Status
- Risk engine prototype  
- Browser extension  
- Production deployment
