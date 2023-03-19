#!/usr/bin/env python3
import os
from datetime import datetime

# If the time difference between two lines is less than this many
# seconds, treat them as part of the same run
time_threshold = 10

def flush(lines, ts):
    if not lines:
        return
    dt = datetime.utcfromtimestamp(ts)
    path = dt.strftime("history/%Y/%Y%m%d_%H%M%S.csv")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as out:
        out.writelines(lines)
    os.utime(path, (ts, ts))

with open("history.csv") as history:
    prev_ts = 0
    lines = []
    for line in history:
        ts = int(line.split(",")[0])
        if ts - prev_ts > time_threshold:
            flush(lines, prev_ts)
            lines = []
        prev_ts = ts
        lines.append(line)
    flush(lines, prev_ts)
