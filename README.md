# silent-failure-detection

Heartbeat-based monitoring project analysing silent failures (missing or delayed telemetry) using Arduino UNO R4 WiFi and Python-based log analysis.

## Silent Failure Detection in Monitoring Systems

This project explores how silent failures (missing or delayed heartbeat signals) can be detected and analysed using a heartbeat monitoring pipeline.

The goal is not to replace existing monitoring platforms, but to make the underlying assumptions, failure modes, and detection logic explicit and inspectable.

---

## Why this matters

In real monitoring environments, systems do not always fail loudly. Devices may stop checking in, telemetry may drop, or messages may be delayed, creating blind spots for detection and investigation.

This project focuses on measuring that silence and analysing its impact rather than relying on explicit error signals.

---


## Current status
- **Day 1:** Baseline heartbeat generation verified locally via Serial Monitor (Arduino UNO R4 WiFi).

- **Day 2:** UDP-based heartbeat transport implemented, backend listener added, silent failure detection and outage tracking validated through real Wi-Fi disconnect tests.

- **Day 3:** Heartbeat timing analysis completed. Raw heartbeat logs were parsed to calculate inter-arrival intervals, sequence deltas, and uptime deltas. Silent failure windows were detected using time-gap thresholds, and malformed, non-heartbeat, and sequence-reset events were classified instead of discarded.

- **Day 4:** Trust and security implications analysed. Silent outages were examined as periods of lost observability and assurance, highlighting how telemetry gaps affect security, incident response, and decision-making.

Detailed implementation notes and observations are documented in the [docs](docs/) directory.


---

## Planned workflow

- Generate periodic heartbeat messages on Arduino UNO R4 WiFi  
- Transmit heartbeats over a controlled Wi-Fi network (UDP)  
- Log received heartbeats on a Windows laptop  
- Detect missing or delayed telemetry using time-gap analysis  
- Record outage start, recovery, and downtime duration  
- Analyse findings from monitoring and forensic perspectives  

---

## Tools

- Arduino UNO R4 WiFi, Arduino IDE  
- Python (standard library, CSV logging; analysis planned with pandas and matplotlib)  
- Wireshark for network observation and validation  
