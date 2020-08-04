## SIRAS (Security Incident Response Automated Simulations)
Security Incident Response Automated Simulations (SIRAS) are internal/controlled events that provide a structured opportunity to practice the incident response plan and procedures during a realistic scenario.

SIRAS is limited to test current detection and response capabilities in order to have internal metrics and a scheduled process to test the same in an automated way.

![alt text](images/deployment.png "SIRAS")

##  Why SIRAS?
Currently, the incident detection and response team are developing differents mechanisms to prevent/detect several types of incidents, leaving aside the test stage. Although each alert/automation is tested before implementing it, and it is not constantly monitored.
For this, SIRAS proposes an automated test model where it is expected to trigger alerts in a controlled manner to make security incidents simulation.

## How to run:

```bash

python3 siras.py

```

## Requeriments
Use the requeriments.txt to get all dependencies. 