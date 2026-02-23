# Zero-Trust-Auth
**Continuous Authentication Engine Project**

## Features
- **Risk scoring**: Device + location + behavior (0-100 score)
- **Continuous authentication**: JWT refresh every 5 minutes
- **Behavioral biometrics**: Mouse, typing patterns, geography
- **Zero Trust**: Never trust, always verify
- **JWT security**: 15-min sliding expiry + geo-fencing

## Risk Engine Formula
- risk_score = 0.4×device + 0.3×geo_velocity + 0.3×behavior
- High risk, **BLOCKED** - unusual IP + late hour

## Working
**Login → Behavioral baseline → Continuous monitoring → Risk score → Re-authenticate**

## Tech Stack
- Java Spring Boot
- PostgreSQL
- Redis
- WebSocket biometrics

## Status
- Risk engine prototype  
- Browser extension  
- Production deployment


## Performance Targets
- Auth/sec: 10K+ 
- Risk scoring: <10ms 
- False positives: <0.5% 
- JWT expiry: 15 min 

## Quick Start
- git clone https://github.com/Keertilata20/zero-trust-auth
- cd zero-trust-auth
- mvn spring-boot:run

