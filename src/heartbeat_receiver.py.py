import socket
import csv
import os
import uuid
from datetime import datetime, timezone

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5005

HEARTBEATS_CSV = "data/raw/heartbeats.csv"
OUTAGES_CSV = "data/processed/outages.csv"

# If sender is every 10s, 30s means ~3 missed heartbeats
MISSING_THRESHOLD_SECONDS = 30


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def init_csv_if_empty(path: str, header: list[str]) -> None:
    """Create CSV and write header only if file is missing or empty."""
    ensure_parent_dir(path)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(header)


def main() -> None:
    # Create a session id each time you run this script
    session_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]

    # Prepare outputs
    init_csv_if_empty(HEARTBEATS_CSV, ["session_id", "received_utc", "source_ip", "raw_message"])
    init_csv_if_empty(OUTAGES_CSV, ["session_id", "source_ip", "downtime_start_utc", "downtime_end_utc", "downtime_seconds", "notes"])

    # UDP listener
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))

    print("=" * 60)
    print("Starting heartbeat monitoring run...")
    print(f"Session ID:         {session_id}")
    print(f"Listening on UDP:   {LISTEN_IP}:{LISTEN_PORT}")
    print(f"Heartbeats CSV:     {HEARTBEATS_CSV}")
    print(f"Outages CSV:        {OUTAGES_CSV}")
    print(f"Missing threshold:  {MISSING_THRESHOLD_SECONDS}s")
    print("=" * 60)

    # Tracking state
    last_seen: dict[str, float] = {}     # source_ip -> epoch seconds of last heartbeat received
    outage_open: dict[str, float] = {}   # source_ip -> epoch seconds of downtime start

    with open(HEARTBEATS_CSV, "a", newline="", encoding="utf-8") as hb_file, \
         open(OUTAGES_CSV, "a", newline="", encoding="utf-8") as out_file:

        hb_writer = csv.writer(hb_file)
        out_writer = csv.writer(out_file)

        while True:
            data, addr = sock.recvfrom(2048)

            source_ip = addr[0]
            now_dt = datetime.now(timezone.utc)
            now_ts = now_dt.timestamp()

            msg = data.decode(errors="replace").strip()

            # --- Log raw heartbeat ---
            hb_writer.writerow([session_id, now_dt.isoformat(), source_ip, msg])
            hb_file.flush()

            # --- Determine gap since previous heartbeat for this source ---
            prev_ts = last_seen.get(source_ip)
            if prev_ts is not None:
                gap = now_ts - prev_ts

                # Open outage if gap exceeds threshold and none is open yet
                if gap > MISSING_THRESHOLD_SECONDS and source_ip not in outage_open:
                    outage_open[source_ip] = prev_ts  # downtime starts after last good heartbeat
                    print(f"[ALERT] Possible silent failure for {source_ip}: gap={gap:.1f}s (threshold={MISSING_THRESHOLD_SECONDS}s)")

            # --- If outage was open and we now received a heartbeat, close it ---
            if source_ip in outage_open:
                start_ts = outage_open.pop(source_ip)
                end_ts = now_ts
                duration = end_ts - start_ts

                out_writer.writerow([
                    session_id,
                    source_ip,
                    datetime.fromtimestamp(start_ts, tz=timezone.utc).isoformat(),
                    now_dt.isoformat(),
                    f"{duration:.1f}",
                    "Recovered: heartbeat received"
                ])
                out_file.flush()

                print(f"[RECOVERY] {source_ip} recovered. Downtime: {duration:.1f}s")

            # Update last_seen
            last_seen[source_ip] = now_ts

            # Console output
            print(now_dt.isoformat(), source_ip, msg)


if __name__ == "__main__":
    main()
