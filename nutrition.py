"""
NutritionScreen – Smart Fitness Management System

This module allows users to:
- Log daily meals with calorie and nutrient data
- Display a table showing meal history
- Provide simple nutrition tips based on most recent meal

Data file used: data/meals.json

Author: Jawad Khan
Date: [YYYY-MM-DD]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from tkinter.font import nametofont

# === Ensure meals data file exists ===
DATA_FILE = "data/meals.json"
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

class NutritionScreen:
    """
    GUI window for logging and reviewing meals and nutrients.
    """

    def __init__(self, parent):
        """
        Build the meal logging and nutrition tracking window.
        :param parent: Tkinter root or Toplevel
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Nutrition Tracking")
        self.window.geometry("620x520")
        self.window.resizable(False, False)

        # Apply global font for consistency
        default_font = nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=11)

        # === Header ===
        ttk.Label(
            self.window,
            text="Nutrition Tracking & Meal Logging",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        # === Input Form ===
        form_frame = ttk.Frame(self.window, padding=10)
        form_frame.pack(fill=tk.X)

        # Labels and input fields for meal tracking
        ttk.Label(form_frame, text="Meal Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form_frame, text="Calories:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form_frame, text="Protein (g):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form_frame, text="Carbs (g):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form_frame, text="Fats (g):").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Input fields
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

        # === Buttons ===
        button_frame = ttk.Frame(self.window, padding=(10, 0))
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Log Meal", command=self.log_meal).pack(side="right", padx=10, pady=10)
        ttk.Button(button_frame, text="Get Nutrition Tip", command=self.show_tip).pack(side="left", padx=10, pady=10)

        # === Table Label ===
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

        # Load meals from JSON file on start
        self.load_meals()

    def log_meal(self):
        """
        Save a meal to JSON file using form data.
        """
        try:
            meal = self.meal_type.get()
            cal = int(self.calories_entry.get())
            protein = int(self.protein_entry.get())
            carbs = int(self.carbs_entry.get())
            fats = int(self.fats_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter only numeric values.")
            return

        if not meal:
            messagebox.showwarning("Missing Field", "Please select a meal type.")
            return

        meal_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": meal,
            "calories": cal,
            "protein": protein,
            "carbs": carbs,
            "fats": fats
        }

        with open(DATA_FILE, "r+") as f:
            data = json.load(f)
            data.append(meal_data)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        messagebox.showinfo("Logged", "Meal has been saved successfully.")
        self.clear_fields()
        self.load_meals()

    def load_meals(self):
        """
        Load meal data and refresh the table view.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        with open(DATA_FILE, "r") as f:
            meals = json.load(f)
            for m in meals:
                self.tree.insert("", tk.END, values=(
                    m["date"], m["type"], m["calories"], m["protein"], m["carbs"], m["fats"]
                ))

    def clear_fields(self):
        """
        Reset all input fields.
        """
        self.meal_type.set("")
        self.calories_entry.delete(0, tk.END)
        self.protein_entry.delete(0, tk.END)
        self.carbs_entry.delete(0, tk.END)
        self.fats_entry.delete(0, tk.END)

    def show_tip(self):
        """
        Show a nutrition tip based on the last meal entry.
        """
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        if not data:
            messagebox.showinfo("Tip", "Log a meal to receive personalized nutrition advice.")
            return

        latest = data[-1]
        tips = []

        if latest["protein"] < 10:
            tips.append("Add more protein (e.g. eggs, chicken, tofu).")
        if latest["carbs"] > 100:
            tips.append("Too many carbs! Reduce sugar and starchy foods.")
        if latest["fats"] > 40:
            tips.append("High fat detected. Choose leaner meals.")
        if latest["calories"] > 700:
            tips.append("That meal was heavy. Consider balancing with a lighter one.")

        if not tips:
            tips.append("Your meal looks balanced. Keep it up!")

        messagebox.showinfo("Nutrition Tip", "\n\n".join(tips))
