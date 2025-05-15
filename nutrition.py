"""
NutritionScreen Module – Smart Fitness Management System

This module provides a GUI interface for:
- Logging meals with calorie and macronutrient info
- Displaying a meal history table
- Offering simple nutrition tips based on recent intake

Data is stored in: data/meals.json

Author: [Your Name]
Date: [YYYY-MM-DD]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from tkinter.font import nametofont

# === File Configuration ===
DATA_FILE = "data/meals.json"
os.makedirs("data", exist_ok=True)

# Create meals.json file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

class NutritionScreen:
    """
    A GUI screen for tracking meals and nutrition intake.
    """

    def __init__(self, parent):
        """
        Initialize the Nutrition Tracking screen and layout.
        :param parent: Parent window or root
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Nutrition Tracking")
        self.window.geometry("620x520")
        self.window.resizable(False, False)

        # Apply global font
        default_font = nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=11)

        # === Header Title ===
        ttk.Label(
            self.window,
            text="Nutrition Tracking & Meal Logging",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        # === Meal Logging Form ===
        form_frame = ttk.Frame(self.window, padding=10)
        form_frame.pack(fill=tk.X)

        # Form fields: meal type, calories, protein, carbs, fats
        ttk.Label(form_frame, text="Meal Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form_frame, text="Calories:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form_frame, text="Protein (g):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form_frame, text="Carbs (g):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form_frame, text="Fats (g):").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.meal_type = ttk.Combobox(form_frame, values=["Breakfast", "Lunch", "Dinner", "Snack"], state="readonly")
        self.meal_type.grid(row=0, column=1, padx=5, pady=5)

        self.calories_entry = ttk.Entry(form_frame)
        self.calories_entry.grid(row=1, column=1, padx=5, pady=5)

        self.protein_entry = ttk.Entry(form_frame)
        self.protein_entry.grid(row=2, column=1, padx=5, pady=5)

        self.carbs_entry = ttk.Entry(form_frame)
        self.carbs_entry.grid(row=3, column=1, padx=5, pady=5)

        self.fats_entry = ttk.Entry(form_frame)
        self.fats_entry.grid(row=4, column=1, padx=5, pady=5)

        # === Action Buttons ===
        button_frame = ttk.Frame(self.window, padding=(10, 0))
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Log Meal", command=self.log_meal).pack(side="right", padx=10, pady=10)
        ttk.Button(button_frame, text="Get Nutrition Tip", command=self.show_tip).pack(side="left", padx=10, pady=10)

        # === Table Header ===
        ttk.Label(self.window, text="Meal History", font=("Helvetica", 12, "bold")).pack(anchor="w", padx=15)

        # === Table Display ===
        table_frame = ttk.Frame(self.window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Date", "Type", "Calories", "Protein", "Carbs", "Fats"),
            show="headings",
            height=10
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=95, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Load saved meals into table
        self.load_meals()

    def log_meal(self):
        """
        Log a new meal entry from form input and save to meals.json.
        """
        try:
            meal = self.meal_type.get()
            cal = int(self.calories_entry.get())
            p = int(self.protein_entry.get())
            c = int(self.carbs_entry.get())
            f = int(self.fats_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "Please enter numeric values.")
            return

        if not meal:
            messagebox.showwarning("Missing", "Select a meal type.")
            return

        meal_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": meal,
            "calories": cal,
            "protein": p,
            "carbs": c,
            "fats": f
        }

        # Save new meal to JSON file
        with open(DATA_FILE, "r+") as f:
            data = json.load(f)
            data.append(meal_data)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        messagebox.showinfo("Logged", "Meal saved.")
        self.clear_fields()
        self.load_meals()

    def load_meals(self):
        """
        Reload meal data from JSON and refresh the table view.
        """
        # Clear existing table rows
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Load data and insert into table
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for m in data:
                self.tree.insert("", tk.END, values=(
                    m["date"], m["type"], m["calories"], m["protein"], m["carbs"], m["fats"]
                ))

    def clear_fields(self):
        """
        Clear all input fields after submission.
        """
        self.meal_type.set("")
        self.calories_entry.delete(0, tk.END)
        self.protein_entry.delete(0, tk.END)
        self.carbs_entry.delete(0, tk.END)
        self.fats_entry.delete(0, tk.END)

    def show_tip(self):
        """
        Generate a basic nutrition tip based on the last meal entry.
        """
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        if not data:
            messagebox.showinfo("Tip", "Log some meals to get personalized tips.")
            return

        latest = data[-1]
        cal = latest["calories"]
        protein = latest["protein"]
        carbs = latest["carbs"]
        fats = latest["fats"]

        tips = []

        if protein < 10:
            tips.append("Add more protein (e.g. eggs, chicken, tofu) to support muscle repair.")
        if carbs > 100:
            tips.append("High carb alert! Consider cutting down on sugar-heavy or starchy meals.")
        if fats > 40:
            tips.append("Fat intake is high. Try more lean meals or salads.")
        if cal > 700:
            tips.append("That was a heavy meal! Balance with lighter meals today.")
        if not tips:
            tips.append("Balanced intake! Keep up the good work!")

        messagebox.showinfo("Nutrition Tip", "\n\n".join(tips))
