# src/trainer_motion.py
"""
OpenCV motion-based trainer (works on Python 3.13).
Detects: squats, jumping jacks, sit-ups via contour & bbox heuristics.
Usage:
    python src/trainer_motion.py --exercise squat
    python src/trainer_motion.py --exercise jumping_jack
    python src/trainer_motion.py --exercise situp
Press:
    c  -> calibrate (recommended)
    q  -> quit
"""
import subprocess
import sys
import os

import cv2
import argparse
import time
import numpy as np
from utils import moving_average, beep, save_session


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--exercise", choices=["squat","jumping_jack","situp"], default="squat")
    p.add_argument("--camera", type=int, default=0)
    return p.parse_args()

# Utility to find the largest contour area and its bounding rectangle and centroid
def get_largest_contour_info(fgmask):
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, 0, None
    # pick largest contour by area
    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)
    if area < 500:  # too small -> noise
        return None, 0, None
    x,y,w,h = cv2.boundingRect(largest)
    cx = x + w//2
    cy = y + h//2
    return (x,y,w,h), area, (cx,cy)

# Basic rep counter based on centroid changes (state machine)
class MotionRepCounter:
    def __init__(self, mode="squat"):
        self.mode = mode
        self.count = 0
        self.state = "start"
        self.history = []
        self.width_history = []
        self.height_history = []

        # thresholds relative to calibration values (set during calibrate)
        self.calib = {'cy':None, 'cx':None, 'h':None, 'w':None}
        self.down_thresh = 0.85
        self.up_thresh = 1.12
        self.wide_thresh = 1.15

    def calibrate(self, cx, cy, w, h):
        self.calib['cx'] = cx
        self.calib['cy'] = cy
        self.calib['w'] = max(w,1)
        self.calib['h'] = max(h,1)
        print("Calibrated:", self.calib)

    def update(self, cx, cy, w, h):
        # append to history
        self.history.append(cy)
        self.width_history.append(w)
        self.height_history.append(h)

        smooth_cy = moving_average(self.history, window=6)
        smooth_w = moving_average(self.width_history, window=6)
        smooth_h = moving_average(self.height_history, window=6)

        # if not calibrated yet, cannot count
        if self.calib['cy'] is None:
            return self.count, smooth_cy, "not calibrated"

        # For squats and situps use vertical movement (cy)
        if self.mode in ["squat","situp"]:
            base_h = self.calib['h']
            # relative height of bbox (current / base)
            rel_h = smooth_h / base_h if base_h>0 else 1.0
            # relative centroid y (lower means nearer top of frame)
            rel_cy = smooth_cy / self.calib['cy'] if self.calib['cy']>0 else 1.0

            # Heuristic:
            # - For squat: when centroid moves down significantly (rel_cy > down_thresh) -> 'down' state
            #   then when centroid comes back up (rel_cy < up_thresh) -> count rep
            if self.state == "start" or self.state == "up":
                if rel_cy > self.down_thresh:
                    self.state = "down"
            elif self.state == "down":
                if rel_cy < self.up_thresh:
                    self.state = "up"
                    self.count += 1
                    beep()
            feedback = f"rel_cy:{rel_cy:.2f}"
            return self.count, smooth_cy, feedback

        # For jumping jacks use width increase (arms out increases silhouette width)
        elif self.mode == "jumping_jack":
            base_w = self.calib['w']
            rel_w = smooth_w / base_w if base_w>0 else 1.0
            if self.state == "start" or self.state == "in":
                if rel_w > self.wide_thresh:
                    self.state = "out"
            elif self.state == "out":
                if rel_w < 1.05:
                    self.state = "in"
                    self.count += 1
                    beep()
            feedback = f"rel_w:{rel_w:.2f}"
            return self.count, smooth_w, feedback

        else:
            return self.count, smooth_cy, "unknown mode"

def main():
    args = parse_args()
    cap = cv2.VideoCapture(args.camera)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=25, detectShadows=True)

    counter = MotionRepCounter(mode=args.exercise)
    start_time = time.time()
    calibrated = False
    show_info = True

    print("Controls: press 'c' to calibrate, 'q' to quit. Calibrate by standing normally in frame.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not available.")
            break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # preprocess: blur and grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        fgmask = fgbg.apply(blur)

        # morphological ops to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=1)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_DILATE, kernel, iterations=1)

        bbox, area, centroid = get_largest_contour_info(fgmask)

        if bbox is not None:
            x,y,bw,bh = bbox
            cx,cy = centroid
            cv2.rectangle(frame, (x,y), (x+bw, y+bh), (0,255,0), 2)
            cv2.circle(frame, (cx,cy), 4, (0,0,255), -1)

            if calibrated is False:
                cv2.putText(frame, "Press 'c' to calibrate (stand normally)", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
            else:
                count, measure, feedback = counter.update(cx, cy, bw, bh)
                cv2.putText(frame, f"Reps: {counter.count}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 3)
                cv2.putText(frame, f"Feedback: {feedback}", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
        else:
            cv2.putText(frame, "No person detected", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        cv2.imshow("AI Motion Trainer", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        if key == ord('c'):
            # calibrate using current bbox / centroid
            if bbox is not None:
                x,y,bw,bh = bbox
                cx,cy = centroid
                counter.calibrate(cx, cy, bw, bh)
                calibrated = True
                print("Calibrated. Now start exercising.")
            else:
                print("Cannot calibrate: no person detected")

    total_time = time.time() - start_time
    reps = counter.count
    # simple calories estimate (MET approach)
    weight = 70.0
    met = 5.0 if args.exercise == "squat" else 7.0 if args.exercise == "situp" else 6.0
    hours = max(total_time / 3600.0, 1/3600.0)
    calories = met * weight * hours

    print(f"Session ended. Time: {total_time:.1f}s, Reps: {reps}, Calories (est): {calories:.2f}")
    save_session(args.exercise, reps, total_time, calories)
    # --- AUTO OPEN DASHBOARD ---
    script_path = os.path.join(os.path.dirname(__file__), "dashboard_app.py")
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", script_path])
    print("Opening dashboard...")



    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
