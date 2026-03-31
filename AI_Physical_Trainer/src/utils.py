import numpy as np
import platform
import os
from datetime import datetime
import csv

# Audio beep helper: use winsound on Windows, else fallback to system bell
def beep():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 120)
        else:
            print("\a", end="", flush=True)
    except Exception:
        try:
            print("\a", end="", flush=True)
        except:
            pass

def moving_average(values, window=5):
    if len(values) < window:
        return float(np.mean(values)) if values else 0.0
    return float(np.mean(values[-window:]))

def save_session(exercise, reps, duration_seconds, calories_estimate, out_file="session_log.csv"):
    row = [datetime.now().isoformat(), exercise, int(reps), float(round(duration_seconds,1)), float(round(calories_estimate,2))]
    header = ['timestamp','exercise','reps','duration_seconds','calories']
    write_header = not os.path.exists(out_file)
    with open(out_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row)

