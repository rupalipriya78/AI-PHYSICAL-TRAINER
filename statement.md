1.Problem Statement
Many individuals struggle to accurately track their workout performance due to the lack of real-time feedback, proper rep counting, and a unified system that logs exercise data. Existing fitness applications often require wearables or advanced pose-estimation libraries that do not work with newer Python versions (like Python 3.13).
Users need a lightweight, webcam-based AI system that can automatically detect movements, count reps, estimate calories, and maintain workout history—without requiring sensors or expensive hardware.

2.Scope of the Project
The scope of this project includes:
-Developing a real-time computer vision model using OpenCV for motion-based rep detection.
-Supporting three core exercises: Squats, Jumping Jacks, and Sit-Ups.
-Creating an interactive Tkinter GUI for selecting and starting workouts.
-Implementing calibration, rep-counting logic, and audio feedback.
-Logging all training sessions into a CSV file for persistent history.
-Visualizing workout progress through a Streamlit dashboard, which auto-opens after each session.
-Ensuring full compatibility with Python 3.13, avoiding unsupported libraries like MediaPipe.
The project does not aim to perform advanced posture correction, full skeletal tracking, or multi-user tracking. It is intentionally lightweight and simple.

3.Target Users
This project is designed for:
-Students who need a simple AI fitness project for academics
-Beginners who want to track home workouts using only a webcam
-Fitness enthusiasts looking for an easy rep counter
-People without access to sensors or wearables
-Users wanting a graphical dashboard to monitor their progress

4.High-Level Features

-Webcam-based motion tracking with OpenCV

-Accurate rep counting for:
  ->Squats
  ->Jumping Jacks
  ->Sit-Ups
  
-Calibration system to adapt detection to different users

-Real-time bounding box + rep feedback

-Audio beep on each completed rep

-Tkinter GUI for selecting exercise and starting workouts

-Session logging into session_log.csv

-Automatic dashboard opening after workout

-Streamlit dashboard showing:
  ->Total reps
  ->Calories burned
  ->Reps-over-time chart
  ->Session comparison
  ->Performance trends

