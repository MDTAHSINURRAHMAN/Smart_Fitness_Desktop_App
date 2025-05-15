"""
ReportScreen Module – Smart Fitness Management System

This module generates:
- A Fitness Report: Summary + Line Chart of daily calories burned
- A Nutrition Report: Summary + Pie Chart of macronutrient distribution

Uses:
- workouts.json → for fitness analysis
- meals.json → for nutrition analysis

Visualized with Matplotlib in embedded Tkinter tabs.

Author: [Your Name]
Date: [YYYY-MM-DD]
"""

import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Paths to JSON data files
WORKOUTS_FILE = "data/workouts.json"
MEALS_FILE = "data/meals.json"

# Ensure data directory and files exist
for path in [WORKOUTS_FILE, MEALS_FILE]:
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)

class ReportScreen:
    """
    A Tkinter window displaying fitness and nutrition reports using tabbed views.
    """

    def __init__(self, parent):
        """
        Initialize the Reports window with two tabs: Fitness and Nutrition.
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Reports and Analytics")
        self.window.geometry("800x550")
        self.window.resizable(False, False)

        # Create notebook tabs
        notebook = ttk.Notebook(self.window)
        self.fitness_tab = ttk.Frame(notebook, padding=15)
        self.nutrition_tab = ttk.Frame(notebook, padding=15)
        notebook.add(self.fitness_tab, text="Fitness Report")
        notebook.add(self.nutrition_tab, text="Nutrition Report")
        notebook.pack(expand=1, fill="both")

        self.build_fitness_report()
        self.build_nutrition_report()

    def build_fitness_report(self):
        """
        Builds the fitness summary: workout count, calories burned, average duration, and a line chart.
        """
        ttk.Label(self.fitness_tab, text="📊 Fitness Summary").pack(pady=(0, 10))

        # Summary: total workouts, calories, average duration
        summary_frame = ttk.Frame(self.fitness_tab)
        summary_frame.pack()

        with open(WORKOUTS_FILE, "r") as f:
            data = json.load(f)
            total_workouts = len(data)
            total_calories = sum(w.get("calories", 0) for w in data)
            durations = [w.get("duration", 0) for w in data]

        avg_duration = round(sum(durations) / total_workouts, 1) if total_workouts else 0

        labels = [
            ("Total Workouts:", total_workouts),
            ("Total Calories Burned:", f"{total_calories} kcal")
        ]

        for i, (label, value) in enumerate(labels):
            ttk.Label(summary_frame, text=label, width=25).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            ttk.Label(summary_frame, text=str(value)).grid(row=i, column=1, sticky="w", padx=5, pady=3)

        # Display fitness insight based on avg duration
        ttk.Label(self.fitness_tab, text="\nFitness Performance Analysis:").pack()

        if avg_duration >= 40:
            summary = "Great improvement in endurance. You're sustaining longer workouts!"
        elif avg_duration >= 25:
            summary = "Moderate endurance improvement detected."
        elif avg_duration > 0:
            summary = "Short sessions logged. Try to increase duration for endurance."
        else:
            summary = "No workouts yet to analyze."

        ttk.Label(self.fitness_tab, text=summary, wraplength=760, justify="center").pack(padx=10, pady=(0, 10))

        # Show line chart
        self.show_fitness_chart()

    def show_fitness_chart(self):
        """
        Shows a 7-day line chart of calories burned.
        """
        with open(WORKOUTS_FILE, "r") as f:
            data = json.load(f)

        # Last 7 days
        today = datetime.today()
        days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        calories_by_day = {day: 0 for day in days}

        for w in data:
            if w["date"] in calories_by_day:
                calories_by_day[w["date"]] += w.get("calories", 0)

        # Create and embed the line chart
        fig, ax = plt.subplots(figsize=(5.5, 3.2))
        ax.plot(list(calories_by_day.keys()), list(calories_by_day.values()), marker='o', color='tab:blue')
        ax.set_title("Calories Burned - Last 7 Days")
        ax.set_ylabel("Calories")
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.fitness_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=5)

    def build_nutrition_report(self):
        """
        Builds the nutrition summary: total macros and pie chart breakdown.
        """
        ttk.Label(self.nutrition_tab, text="📈 Nutrition Summary").pack(pady=(0, 10))

        summary_frame = ttk.Frame(self.nutrition_tab)
        summary_frame.pack()

        with open(MEALS_FILE, "r") as f:
            data = json.load(f)
            meals = len(data)
            total_protein = sum(m.get("protein", 0) for m in data)
            total_carbs = sum(m.get("carbs", 0) for m in data)
            total_fats = sum(m.get("fats", 0) for m in data)
            total_cals = sum(m.get("calories", 0) for m in data)

        labels = [
            ("Total Meals:", meals),
            ("Total Protein:", f"{total_protein} g"),
            ("Total Carbs:", f"{total_carbs} g"),
            ("Total Fats:", f"{total_fats} g"),
            ("Total Calories Consumed:", f"{total_cals} kcal")
        ]

        for i, (label, value) in enumerate(labels):
            ttk.Label(summary_frame, text=label, width=25).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            ttk.Label(summary_frame, text=str(value)).grid(row=i, column=1, sticky="w", padx=5, pady=3)

        self.show_nutrition_pie(total_protein, total_carbs, total_fats)

    def show_nutrition_pie(self, protein, carbs, fats):
        """
        Draws a pie chart of macronutrient breakdown (protein, carbs, fats).
        """
        fig, ax = plt.subplots(figsize=(4.2, 2.8))
        labels = ['Protein', 'Carbs', 'Fats']
        values = [protein, carbs, fats]
        colors = ['#4caf50', '#2196f3', '#ff9800']

        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title("Macronutrient Breakdown")

        canvas = FigureCanvasTkAgg(fig, master=self.nutrition_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
