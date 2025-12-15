import csv
import os
import re
from datetime import datetime, timezone


IN_CSV = "data/raw/heartbeats.csv"
OUT_DIR = "analysis/out"
OUT_INTERVALS = os.path.join(OUT_DIR, "heartbeat_intervals.csv")
OUT_OUTAGES = os.path.join(OUT_DIR, "outages_detected.csv")
OUT_ANOMALIES = os.path.join(OUT_DIR, "anomalous_messages.csv")

OUTAGE_THRESHOLD_SECONDS = 30.0  

HB_RE = re.compile(r"^HB,(\d+),(\d+)\s*$")  # HB,<seq>,<uptime_ms>



def parse_received_utc(s: str) -> datetime:
    """
    Parses timestamps like:
      - 2025-12-14T18:43:09.125258
      - 2025-12-14T19:40:10.030681+00:00

    Returns a timezone-aware datetime in UTC.
    """
    s = (s or "").strip()

   
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    dt = datetime.fromisoformat(s)

   
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc)


def classify_message(raw_message: str):
    """
    Returns: (msg_type, seq, uptime_ms, reason)
      msg_type: "HB" | "NON_HB" | "MALFORMED_HB"
    """
    msg = (raw_message or "").strip()
    if msg.startswith("HB,"):
        m = HB_RE.match(msg)
        if not m:
            return ("MALFORMED_HB", None, None, "HB prefix but does not match HB,<seq>,<uptime_ms>")
        return ("HB", int(m.group(1)), int(m.group(2)), None)

    return ("NON_HB", None, None, "Not a heartbeat message")



def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    
    last_by_ip = {}  

    total_rows = 0
    hb_rows = 0
    non_hb_rows = 0
    malformed_hb_rows = 0
    parse_time_fail_rows = 0

    intervals_out = []
    outages_out = []
    anomalies_out = []

    with open(IN_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        
        for row in reader:
            total_rows += 1

            received_raw = row.get("received_utc", "")
            source_ip = (row.get("source_ip", "") or "").strip()
            raw_message = row.get("raw_message", "")

           
            try:
                ts = parse_received_utc(received_raw)
            except Exception as e:
                parse_time_fail_rows += 1
                anomalies_out.append({
                    "received_utc": received_raw,
                    "source_ip": source_ip,
                    "raw_message": raw_message,
                    "anomaly_type": "BAD_TIMESTAMP",
                    "reason": str(e),
                })
                continue

            
            msg_type, seq, uptime_ms, reason = classify_message(raw_message)

            if msg_type == "NON_HB":
                non_hb_rows += 1
                anomalies_out.append({
                    "received_utc": ts.isoformat(),
                    "source_ip": source_ip,
                    "raw_message": raw_message,
                    "anomaly_type": "NON_HB",
                    "reason": reason,
                })
                continue

            if msg_type == "MALFORMED_HB":
                malformed_hb_rows += 1
                anomalies_out.append({
                    "received_utc": ts.isoformat(),
                    "source_ip": source_ip,
                    "raw_message": raw_message,
                    "anomaly_type": "MALFORMED_HB",
                    "reason": reason,
                })
                continue

           
            hb_rows += 1

            prev = last_by_ip.get(source_ip)
            if prev is not None:
                dt_seconds = (ts - prev["ts"]).total_seconds()
                seq_delta = seq - prev["seq"]
                uptime_delta_ms = uptime_ms - prev["uptime_ms"]

               
                intervals_out.append({
                    "source_ip": source_ip,
                    "received_utc": ts.isoformat(),
                    "seq": seq,
                    "uptime_ms": uptime_ms,
                    "delta_seconds": round(dt_seconds, 6),
                    "seq_delta": seq_delta,
                    "uptime_delta_ms": uptime_delta_ms,
                })

                
                if dt_seconds > OUTAGE_THRESHOLD_SECONDS:
                    outages_out.append({
                        "source_ip": source_ip,
                        "downtime_start_utc": prev["ts"].isoformat(),
                        "downtime_end_utc": ts.isoformat(),
                        "gap_seconds": round(dt_seconds, 3),
                        "threshold_seconds": OUTAGE_THRESHOLD_SECONDS,
                        "prev_seq": prev["seq"],
                        "new_seq": seq,
                        "seq_delta": seq_delta,
                        "note": "Gap exceeded threshold (possible silent failure / telemetry loss)",
                    })

                
                if seq_delta > 1:
                    anomalies_out.append({
                        "received_utc": ts.isoformat(),
                        "source_ip": source_ip,
                        "raw_message": raw_message,
                        "anomaly_type": "SEQ_GAP",
                        "reason": f"Sequence jumped by {seq_delta} (possible missed heartbeats)",
                    })

            
            last_by_ip[source_ip] = {"ts": ts, "seq": seq, "uptime_ms": uptime_ms}

   
    def write_csv(path, fieldnames, rows):
        with open(path, "w", newline="", encoding="utf-8") as wf:
            w = csv.DictWriter(wf, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

    if intervals_out:
        write_csv(
            OUT_INTERVALS,
            ["source_ip", "received_utc", "seq", "uptime_ms", "delta_seconds", "seq_delta", "uptime_delta_ms"],
            intervals_out,
        )

    if outages_out:
        write_csv(
            OUT_OUTAGES,
            ["source_ip", "downtime_start_utc", "downtime_end_utc", "gap_seconds", "threshold_seconds",
             "prev_seq", "new_seq", "seq_delta", "note"],
            outages_out,
        )

    if anomalies_out:
        write_csv(
            OUT_ANOMALIES,
            ["received_utc", "source_ip", "raw_message", "anomaly_type", "reason"],
            anomalies_out,
        )


    print("=== Day 3: Heartbeat timing analysis ===")
    print(f"Input file: {IN_CSV}")
    print(f"Total rows: {total_rows}")
    print(f"Valid HB rows: {hb_rows}")
    print(f"Non-HB rows preserved as anomalies: {non_hb_rows}")
    print(f"Malformed HB rows preserved as anomalies: {malformed_hb_rows}")
    print(f"Bad timestamp rows preserved as anomalies: {parse_time_fail_rows}")
    print("")
    print(f"Intervals output: {OUT_INTERVALS if intervals_out else '(none)'}")
    print(f"Outages output:   {OUT_OUTAGES if outages_out else '(none)'}")
    print(f"Anomalies output: {OUT_ANOMALIES if anomalies_out else '(none)'}")


if __name__ == "__main__":
    main()
