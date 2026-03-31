# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

def start_exercise():
    ex = exercise_var.get()
    if not ex:
        messagebox.showerror("Select exercise", "Please choose an exercise")
        return
    # run trainer script in a new terminal window (platform-specific)
    python_exec = sys.executable  # ensures same python interpreter
    script = os.path.join("src","trainer_motion.py")
    # Open in same console (blocking) — user can close window after exercise
    subprocess.call([python_exec, script, "--exercise", ex])

root = tk.Tk()
root.title("AI Physical Trainer (Motion)")
root.geometry("420x260")

tk.Label(root, text="AI Physical Trainer", font=("Arial", 18, "bold")).pack(pady=12)
tk.Label(root, text="Select exercise:", font=("Arial", 12)).pack()
exercise_var = tk.StringVar()
combo = ttk.Combobox(root, textvariable=exercise_var, state="readonly", values=["squat","jumping_jack","situp"])
combo.pack(pady=8)
combo.current(0)

start_btn = tk.Button(root, text="Start Workout", bg="#4CAF50", fg="white", font=("Arial",12), width=20, command=start_exercise)
start_btn.pack(pady=18)

def open_dashboard():
    python_exec = sys.executable
    script = os.path.join("src","dashboard_app.py")
    subprocess.call([python_exec, "-m", "streamlit", "run", script])

dash_btn = tk.Button(root, text="Open Dashboard", bg="#2196F3", fg="white", font=("Arial",10), width=20, command=open_dashboard)
dash_btn.pack()

root.mainloop()
