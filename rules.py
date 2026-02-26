from db import get_conn

def apply_rules(cid, calls):
    alerts = []

    total = len(calls)
    failures = [c for c in calls if c["final_status"] and c["final_status"].startswith(("4","5"))]

    if total > 0:
        error_rate = len(failures) / total
        if error_rate > 0.2:
            alerts.append({
                "rule_name": "High Call Failure Rate",
                "severity": "warning",
                "message": f"{error_rate:.1%} failed calls"
            })

    slow_calls = [c for c in calls if c["pdd"] and c["pdd"] > 5]
    if len(slow_calls) > 5:
        alerts.append({
            "rule_name": "High PDD",
            "severity": "warning",
            "message": f"{len(slow_calls)} calls with PDD > 5s"
        })

    if alerts:
        conn = get_conn()
        cur = conn.cursor()
        for a in alerts:
            cur.execute(
                "INSERT INTO alerts (capture_id, rule_name, severity, message) VALUES (?,?,?,?)",
                (cid, a["rule_name"], a["severity"], a["message"])
            )
        conn.commit()
        conn.close()

    return alerts
