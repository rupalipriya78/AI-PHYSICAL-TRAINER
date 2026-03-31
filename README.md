AI Physical Trainer-
A real-time, webcam-based fitness tracking system that detects human body movement using OpenCV and automatically counts repetitions for exercises such as Squats, Jumping Jacks, and Sit-Ups.
The system includes a GUI interface, audio feedback, session logging, and an auto-opening dashboard for visual analytics.

1. Overview of the Project

The AI Physical Trainer is a Python-based application that transforms your webcam into a smart fitness assistant.
It detects motion patterns and counts reps automatically without requiring advanced libraries like MediaPipe (fully compatible with Python 3.13).

The project also stores workout sessions (time, reps, calories) and visualizes them through a Streamlit Dashboard, giving users insights into their progress.

2. Features
a.Real-Time Exercise Tracking
-Tracks Squats, Jumping Jacks, and Sit-Ups
-Uses OpenCV motion detection
-Accurate rep counting with noise filtering

b.Calibration System
-User calibrates before starting
-Auto-adjusts detection thresholds

c.Audio Feedback
-Beep sound on every rep
-Motivates users and confirms detection

d.GUI (Tkinter)
-Select exercise
-Start/stop workout
-Seamless user interaction

e.Streamlit Dashboard
1.Auto-opens after session
2.Shows:
-Total reps
-Calories burned
-Session timeline
-Performance trend chart
-Session history table

f.Session Logging
-All data saved in session_log.csv
-Persistent history across sessions

3. Technologies / Tools Used

Language-	Python 3.13
Computer- Vision	OpenCV
GUI-	Tkinter
Dashboard-	Streamlit
Data Storage-	CSV
Audio Alerts-	winsound / system beep
OS-	Windows 10/11

4.Steps to Install & Run the Project

Step 1: Install Dependencies

Open terminal inside project folder:
pip install -r requirements.txt

Step 2: Run the GUI
python gui.py

Step 3: Inside the app
1.Select the exercise
2.Click Start Workout
3.Press c to calibrate
4.Perform exercise
5.Press q to quit
6.Dashboard opens automatically

5. Instructions for Testing
   
To test each feature:

Test 1: Webcam Detection
-Stand in front of camera
-Press c
-Check bounding box movement

 Test 2: Rep Counting
-Perform slow-to-medium reps
-Check correct count in console
-Validate beep sound

Test 3: Session Logging
-After pressing q, open session_log.csv
-Confirm new row added
-Check fields: reps, time, calories

Test 4: Dashboard
-After workout, dashboard opens automatically
-Validate:
->graphs
->stats
->history
->last session entry

6. Screenshots
GUI homescreen
<img width="1158" height="602" alt="image" src="https://github.com/user-attachments/assets/b173e9a8-5049-47bd-a509-1c068a2fb565" />

Camera window+Rep counting
<img width="597" height="458" alt="image" src="https://github.com/user-attachments/assets/1035a8bc-6222-47de-8c90-f407db9ac6e2" />

dashboard
<img width="1161" height="627" alt="image" src="https://github.com/user-attachments/assets/4f70cb44-7330-4a3b-993b-492c509b9c76" />

