# silent-failure-detection
Heartbeat-based monitoring project analysing silent failures (missing/delayed telemetry) using Arduino UNO R4 WiFi + Python log analysis.

# Silent Failure Detection in Monitoring Systems

This project explores how **silent failures** (missing or delayed heartbeat signals) can be detected and analysed using a heartbeat monitoring pipeline.

## Why this matters
In real monitoring environments, systems don’t always fail loudly. Devices may stop checking in, telemetry may drop, or messages may be delayed, creating blind spots for detection and investigation. This project measures that silence and analyses its impact.

## Current status
 Day 1 complete: baseline heartbeat generation verified via Serial Monitor (Arduino UNO R4 WiFi).

## Planned workflow
1. Generate periodic heartbeat messages on Arduino UNO R4 WiFi  
2. Transmit heartbeats over a controlled Wi-Fi network (phone hotspot)  
3. Log received heartbeats on a Windows laptop  
4. Analyse missing/delayed telemetry using Python (Jupyter)  
5. Document findings from detection and forensic perspectives

## Tools (planned)
- Arduino UNO R4 WiFi, Arduino IDE
- Python (pandas, matplotlib), Jupyter Notebook
- Wireshark for network observation
