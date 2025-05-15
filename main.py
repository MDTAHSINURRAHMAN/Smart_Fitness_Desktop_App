"""
Smart Fitness Management System - Main GUI Launcher

This module initializes the main window of the application using Tkinter.
It provides navigation to various functional modules:
- User Management
- Workout Tracking
- Goal Tracking
- Nutrition Tracking
- Reports & Analytics

Author: Jawad Khan
Date: [YYYY-MM-DD]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk  # Sun Valley modern theme for ttk widgets

# Import individual module screens
from users import UserScreen
from workouts import WorkoutScreen
from goals import GoalScreen
from nutrition import NutritionScreen
from reports import ReportScreen

class HomeScreen:
    """
    Main GUI window for the Smart Fitness Management System.

    Features:
    - Modern dark theme using sv_ttk
    - Button-based navigation to functional modules
    - Handles runtime errors with popup alerts
    """
    def __init__(self):
        """
        Initialize the root window and build the navigation UI.
        """
        self.root = tk.Tk()
        self.root.title("Smart Fitness Management System")
        self.root.geometry("500x420")

        # Apply Sun Valley theme (can be 'light' or 'dark')
        sv_ttk.set_theme("dark")

        # Title label for the app
        title_label = ttk.Label(
            self.root,
            text="Smart Fitness Management System",
            font=("Helvetica", 16, "bold"),
            anchor="center",
            justify="center"
        )
        title_label.pack(pady=25)

        # Frame to hold all navigation buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack()

        # Button labels and corresponding method mappings
        buttons = [
            ("User Management", self.open_users),
            ("Workout Tracking", self.open_workouts),
            ("Goal Tracking", self.open_goals),
            ("Nutrition Tracking", self.open_nutrition),
            ("Reports & Analytics", self.open_reports),
        ]

        # Generate and pack each button
        for text, command in buttons:
            ttk.Button(button_frame, text=text, width=32, command=command).pack(pady=6)

        # Start the GUI event loop
        self.root.mainloop()

    # === Navigation Functions for Module Windows ===

    def open_users(self):
        """
        Open the User Management screen.
        """
        try:
            UserScreen(self.root)
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def open_workouts(self):
        """
        Open the Workout Tracking screen.
        """
        try:
            WorkoutScreen(self.root)
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def open_goals(self):
        """
        Open the Goal Tracking screen.
        """
        try:
            GoalScreen(self.root)
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def open_nutrition(self):
        """
        Open the Nutrition Tracking screen.
        """
        try:
            NutritionScreen(self.root)
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def open_reports(self):
        """
        Open the Reports and Analytics screen.
        """
        try:
            ReportScreen(self.root)
        except Exception as e:
            messagebox.showinfo("Error", str(e))

# Entry point check to avoid unintended execution during imports
if __name__ == "__main__":
    HomeScreen()
