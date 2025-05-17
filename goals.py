"""
GoalScreen – Smart Fitness Management System

This module enables users to:
- Set a fitness goal (calorie burn target)
- Track progress based on workout logs
- See progress using a progress bar and percentage
- Reset data upon goal completion
- View a weekly summary report of calories burned

Author: Jawad Khan
Date: [YYYY-MM-DD]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
from tkinter.font import nametofont

# File paths for storing goals and workout data
GOALS_FILE = "data/goals.json"
WORKOUTS_FILE = "data/workouts.json"

# Ensure the necessary files and folders exist
os.makedirs("data", exist_ok=True)
for path in [GOALS_FILE, WORKOUTS_FILE]:
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f) if "workouts" in path else json.dump({}, f)

class GoalScreen:
    """
    Window to allow users to track and manage their fitness goals.
    """

    def __init__(self, parent):
        """
        Initialize the goal tracker interface.
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Fitness Goal Tracking")
        self.window.geometry("520x360")
        self.window.resizable(False, False)

        # Apply global font for consistency
        default_font = nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=11)

        # --- Header ---
        ttk.Label(
            self.window,
            text="Set & Track Your Calorie Burn Goal",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        # --- Goal Input Area ---
        goal_frame = ttk.Frame(self.window, padding=10)
        goal_frame.pack()

        ttk.Label(goal_frame, text="Enter Calorie Goal:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.goal_entry = ttk.Entry(goal_frame, width=30)
        self.goal_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(goal_frame, text="Set Goal", command=self.set_goal).grid(row=1, column=1, sticky="e", pady=10)

        # --- Progress Area ---
        progress_frame = ttk.Frame(self.window, padding=10)
        progress_frame.pack()

        ttk.Label(progress_frame, text="Progress Toward Goal:", font=("Helvetica", 12)).pack(anchor="w")

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, length=400, maximum=100)
        self.progress_bar.pack(pady=(5, 10))

        self.progress_label = ttk.Label(progress_frame, text="0% completed", font=("Helvetica", 11))
        self.progress_label.pack()

        ttk.Button(progress_frame, text="Refresh Progress", command=self.update_progress).pack(pady=5)
        ttk.Button(progress_frame, text="View Weekly Report", command=self.show_report).pack(pady=5)

        # Load previous goal if exists and update progress
        self.load_existing_goal()
        self.update_progress()

    def set_goal(self):
        """
        Save the calorie goal entered by the user.
        """
        try:
            goal = int(self.goal_entry.get())
            if goal <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Please enter a valid positive number.")
            return

        with open(GOALS_FILE, "w") as f:
            json.dump({"calorie_goal": goal}, f)

        messagebox.showinfo("Saved", f"Goal of {goal} calories set.")
        self.update_progress()

    def load_existing_goal(self):
        """
        Load any previously saved goal into the input field.
        """
        with open(GOALS_FILE, "r") as f:
            data = json.load(f)
            goal = data.get("calorie_goal")
            if goal:
                self.goal_entry.delete(0, tk.END)
                self.goal_entry.insert(0, str(goal))

    def update_progress(self):
        """
        Update the progress bar based on calories burned from workouts.
        """
        with open(GOALS_FILE, "r") as f:
            goal_data = json.load(f)
            goal = goal_data.get("calorie_goal", 0)

        with open(WORKOUTS_FILE, "r") as f:
            workouts = json.load(f)
            total_burned = sum(w.get("calories", 0) for w in workouts)

        progress = min(100, (total_burned / goal) * 100 if goal else 0)
        self.progress_var.set(progress)
        self.progress_bar.configure(value=progress)
        self.progress_label.config(text=f"{int(progress)}% completed ({total_burned} of {goal} cal)")

        if progress >= 100:
            response = messagebox.askyesno(
                "Goal Completed",
                "🎉 You've reached your goal!\n\nWould you like to reset and start fresh?"
            )
            if response:
                self.reset_progress_and_goal()

    def reset_progress_and_goal(self):
        """
        Clear the workout history and goal input to restart tracking.
        """
        with open(WORKOUTS_FILE, "w") as f:
            json.dump([], f)

        self.goal_entry.delete(0, tk.END)
        self.progress_var.set(0)
        self.progress_bar.configure(value=0)
        self.progress_label.config(text="0% completed")
        self.window.after(100, lambda: self.goal_entry.focus())

        messagebox.showinfo("Reset", "Workout history cleared. Please enter a new goal to begin again.")

    def show_report(self):
        """
        Show a summary of calories burned for the past 7 days.
        """
        try:
            with open(WORKOUTS_FILE, "r") as f:
                workouts = json.load(f)
        except:
            workouts = []

        today = datetime.today()
        days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        daily_summary = {day: 0 for day in days}

        for w in workouts:
            date = w.get("date")
            if date in daily_summary:
                daily_summary[date] += w.get("calories", 0)

        summary_text = "Weekly Calorie Burn Report:\n\n"
        for day, cal in daily_summary.items():
            summary_text += f"{day}: {cal} cal\n"

        total = sum(daily_summary.values())
        summary_text += f"\n Total This Week: {total} cal"

        messagebox.showinfo("Weekly Report", summary_text)
