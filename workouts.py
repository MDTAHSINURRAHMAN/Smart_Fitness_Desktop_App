"""
WorkoutScreen Module – Smart Fitness Management System

This module provides a GUI screen for logging and managing workout history.
Users can:
- Add a workout (type, duration, calories, notes)
- View workouts in a table
- Double-click to view notes
- Delete selected workouts

Data is stored in a local JSON file (data/workouts.json).

Author: Jawad Khan
Date: [YYYY-MM-DD]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from tkinter.font import nametofont

DATA_FILE = "data/workouts.json"

# Ensure data directory and file exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

class WorkoutScreen:
    """
    A GUI window for logging, viewing, and deleting workout records.
    """

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Workout Tracking")
        self.window.geometry("600x560")
        self.window.resizable(False, False)

        # Set default font
        default_font = nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=11)

        # === Workout Input Form ===
        form_frame = ttk.Frame(self.window, padding=10)
        form_frame.pack(fill=tk.X)

        ttk.Label(form_frame, text="Exercise Type:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.exercise_entry = ttk.Entry(form_frame, width=30)
        self.exercise_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Duration (mins):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.duration_entry = ttk.Entry(form_frame, width=30)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Calories Burned:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.calories_entry = ttk.Entry(form_frame, width=30)
        self.calories_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Notes:").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        self.notes_text = tk.Text(
            form_frame,
            width=30,
            height=4,
            font=("Helvetica", 10),
            relief="solid",
            borderwidth=1,
            padx=5,
            pady=5
        )
        self.notes_text.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Log Workout", command=self.log_workout).grid(row=4, column=1, sticky="e", pady=10)

        # === Workout History Table ===
        table_frame = ttk.Frame(self.window, padding=(10, 0))
        table_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(table_frame, text="Workout History", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Date", "Type", "Duration", "Calories"),
            show="headings",
            height=5
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)

        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.tree.bind("<Double-1>", self.on_row_double_click)

        # === Delete Button ===
        button_bottom = ttk.Frame(self.window)
        button_bottom.pack(pady=10)
        ttk.Button(button_bottom, text="Delete Selected", command=self.delete_selected).pack()

        # Load workouts into the table
        self.load_workouts()

    def log_workout(self):
        """
        Save a new workout after validating the fields.
        """
        exercise = self.exercise_entry.get()
        duration = self.duration_entry.get()
        calories = self.calories_entry.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not exercise or not duration or not calories:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        try:
            duration = int(duration)
            calories = int(calories)
        except ValueError:
            messagebox.showerror("Invalid Input", "Duration and Calories must be numbers.")
            return

        workout = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": exercise,
            "duration": duration,
            "calories": calories,
            "notes": notes
        }

        with open(DATA_FILE, "r+") as f:
            data = json.load(f)
            data.append(workout)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        messagebox.showinfo("Success", "Workout logged.")
        self.clear_fields()
        self.load_workouts()

    def load_workouts(self):
        """
        Load workouts from JSON file and populate the Treeview.
        """
        self.tree.delete(*self.tree.get_children())  # Clear table first

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for workout in data:
                self.tree.insert("", tk.END, values=(
                    workout["date"],
                    workout["type"],
                    workout["duration"],
                    workout["calories"]
                ))

    def delete_selected(self):
        """
        Delete selected workout from table and file.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a workout to delete.")
            return

        values = self.tree.item(selected[0], "values")
        date, wtype, duration, _ = values

        with open(DATA_FILE, "r+") as f:
            data = json.load(f)
            data = [w for w in data if not (
                w["date"] == date and
                w["type"] == wtype and
                str(w["duration"]) == duration
            )]
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        messagebox.showinfo("Deleted", "Workout deleted.")
        self.load_workouts()

    def on_row_double_click(self, event):
        """
        Show workout notes in a messagebox on double-click.
        """
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        date, wtype, duration, _ = values

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for w in data:
                if (w["date"], w["type"], str(w["duration"])) == (date, wtype, str(duration)):
                    notes = w.get("notes", "No notes available.")
                    messagebox.showinfo("Workout Notes", notes)
                    return

    def clear_fields(self):
        """
        Clear all entry fields.
        """
        self.exercise_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)
