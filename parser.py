import pyshark
from datetime import datetime
from collections import defaultdict

def parse_pcap(filepath):
    cap = pyshark.FileCapture(
        filepath,
        display_filter="sip",
        keep_packets=False
    )

    calls = defaultdict(dict)

    for pkt in cap:
        try:
            if not hasattr(pkt, "sip"):
                continue

            ts = datetime.fromtimestamp(float(pkt.sniff_timestamp))
            call_id = getattr(pkt.sip, "call_id", None)
            method = getattr(pkt.sip, "method", None)
            status = getattr(pkt.sip, "status_code", None)

            if not call_id:
                continue

            call = calls[call_id]

            if method == "INVITE" and "invite_ts" not in call:
                call["invite_ts"] = ts

            if status and status.startswith(("2", "3", "4", "5", "6")):
                call["final_ts"] = ts
                call["final_status"] = status

        except:
            continue

    cap.close()

    structured_calls = []

    for call_id, data in calls.items():
        invite_ts = data.get("invite_ts")
        final_ts = data.get("final_ts")
        final_status = data.get("final_status")

        pdd = None
        duration = None

        if invite_ts and final_ts:
            pdd = (final_ts - invite_ts).total_seconds()

        structured_calls.append({
            "call_id": call_id,
            "invite_ts": invite_ts.isoformat() if invite_ts else None,
            "final_ts": final_ts.isoformat() if final_ts else None,
            "final_status": final_status,
            "pdd": pdd,
            "duration": duration
        })

    return structured_calls
