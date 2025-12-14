# Arduino Sketches

This directory contains the Arduino-side components of the project.

## Sketches

### heartbeat_test
Baseline heartbeat generation using Serial output only.
Used to validate timing and counter logic before introducing networking.

### wifi_heartbeat_sender
Wi-Fi-enabled heartbeat sender that transmits periodic UDP heartbeats
to a backend monitoring service.

Wi-Fi credentials should be configured locally before uploading.
