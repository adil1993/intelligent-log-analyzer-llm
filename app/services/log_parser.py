
from datetime import datetime

def parse_logs(raw_logs: str, max_lines: int = 200):
    lines = raw_logs.splitlines()
    truncated = lines[:max_lines]

    error_lines = []
    warn_lines = []
    timestamps = []

    for line in truncated:
        if "ERROR" in line:
            error_lines.append(line)
        if "WARN" in line:
            warn_lines.append(line)

        try:
            ts = line.split(" ")[0] + " " + line.split(" ")[1]
            timestamps.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"))
        except Exception:
            pass

    unique_errors = list(set(error_lines))

    metrics = {
        "total_lines_processed": len(truncated),
        "error_count": len(error_lines),
        "warn_count": len(warn_lines),
        "unique_error_count": len(unique_errors),
        "first_error_timestamp": min(timestamps).isoformat() if timestamps else None,
        "last_error_timestamp": max(timestamps).isoformat() if timestamps else None,
    }

    condensed = error_lines if error_lines else truncated

    return {
        "log_summary": "\n".join(condensed),
        "metrics": metrics,
    }
