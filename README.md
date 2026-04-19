# silent-failure-detection

Heartbeat-based monitoring project analysing silent failures (missing or delayed telemetry) using Arduino UNO R4 WiFi and Python-based log analysis.

This project demonstrates how silent failures in monitoring systems can be detected, investigated, and analysed using a structured, SOC-style approach.


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

- **Day 5:** Forensic reconstruction completed. Outage events were reconstructed using evidence-based reasoning, explicitly separating facts, indicators, and unknowns to assess trust and integrity after silent telemetry loss.

Detailed implementation notes and observations are documented in the [docs](docs/) directory.


---

## Planned workflow

- Generate periodic heartbeat messages on Arduino UNO R4 WiFi  
- Transmit heartbeats over a controlled Wi-Fi network (UDP)  
- Log received heartbeats on a Windows laptop  
- Detect missing or delayed telemetry using time-gap analysis  
- Record outage start, recovery, and downtime duration  
- Analyse findings from monitoring and forensic perspectives


## Tools

- Arduino UNO R4 WiFi, Arduino IDE  
- Python (standard library, CSV logging; analysis planned with pandas and matplotlib)  
- Wireshark for network observation and validation

## Incident Scenario

During monitoring, the system identified periods of missing or delayed heartbeat signals, indicating a potential silent failure event.

These gaps in telemetry simulate real-world alert scenarios where systems stop reporting expected data, which may indicate:
- system failure
- network disruption
- or loss of observability

This scenario reflects how alerts are generated in monitoring and security environments when expected signals are absent.

---

## Investigation Approach

Following detection of a silent failure event, the analysis focused on understanding the cause and impact of the telemetry gap.

Steps included:
- Reviewing heartbeat logs to identify the exact point of failure
- Analysing inter-arrival timing and sequence data
- Identifying deviation from expected heartbeat patterns
- Distinguishing between normal delay and abnormal outage behaviour

This mirrors the investigation process used in monitoring and SOC environments when responding to alerts.

---

## Findings

The system successfully identified silent failure windows based on time-gap thresholds and sequence inconsistencies.

Analysis showed:
- Clear periods of missing telemetry indicating loss of system visibility
- Detectable patterns that differentiate normal operation from failure conditions
- The importance of structured logging in reconstructing system behaviour

While no malicious activity was simulated, the behaviour observed reflects early indicators that would require further investigation in a real-world environment.

---

## Recommendations

- Improve baseline definitions for expected heartbeat behaviour
- Enhance logging for deeper analysis and traceability
- Introduce alert prioritisation based on severity and duration
- Integrate with centralised monitoring or SIEM platforms for scalability

These improvements would strengthen the system's ability to support operational monitoring and security analysis.

---

## Relevance to Security Operations (SOC)

This project demonstrates foundational skills relevant to Security Operations Centre (SOC) roles, including:

- Detection of anomalies through missing or delayed signals
- Investigation of alerts using structured analysis
- Interpretation of system behaviour under failure conditions
- Evidence-based reasoning and reporting

The workflow reflects how analysts investigate alerts, assess system reliability, and respond to loss of visibility in real-world environments.
