"""
UserScreen Module – Smart Fitness Management System

This module handles the User Management interface in the Smart Fitness app.
It allows users to:
- Add a new user profile (Name, Age, Goal)
- Load an existing profile
- Delete a profile
- View profile details in a formatted display

Author: Jawad Khan
Date: [YYYY-MM-DD]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from tkinter.font import nametofont

# File path for user data
DATA_FILE = "data/users.json"

# Ensure the data directory and file exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

class UserScreen:
    """
    GUI window for managing user profiles:
    - Create, save, and delete profiles
    - View profile information
    - Store data in a local JSON file
    """
    def __init__(self, parent):
        """
        Initialize the User Management window UI.
        :param parent: Reference to parent Tk window
        """
        self.window = tk.Toplevel(parent)
        self.window.title("User Management")
        self.window.geometry("520x420")

        # Apply default font for ttk widgets
        default_font = nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=11)

        # === Header Title ===
        ttk.Label(self.window, text="User Profile Manager", font=("Helvetica", 14, "bold")).pack(pady=10)

        # === Form Section ===
        form = ttk.Frame(self.window, padding=10)
        form.pack()

        # Labels and input fields
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(form, text="Age:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(form, text="Goal (e.g., weight loss):").grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.name_entry = ttk.Entry(form, width=30)
        self.age_entry = ttk.Entry(form, width=30)
        self.goal_entry = ttk.Entry(form, width=30)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)
        self.goal_entry.grid(row=2, column=1, padx=5, pady=5)

        # === Buttons ===
        button_frame = ttk.Frame(self.window, padding=10)
        button_frame.pack()

        ttk.Button(button_frame, text="Save Profile", command=self.save_user).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(button_frame, text="Delete Profile", command=self.delete_user).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(button_frame, text="Load Profile", command=self.load_user).grid(row=0, column=2, padx=10, pady=5)

        # === Profile Display Box ===
        display_frame = ttk.Frame(self.window, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        self.profile_display = tk.Text(
            display_frame,
            height=8,
            wrap="word",
            font=("Helvetica", 11),
            bg=self.window.cget("bg"),  # Match parent background
            relief="solid",
            bd=1,
            padx=10,
            pady=10
        )
        self.profile_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.profile_display.configure(state="disabled")

    def save_user(self):
        """
        Save a new user or update an existing user profile.
        Validates input and updates the JSON file.
        """
        name = self.name_entry.get()
        age = self.age_entry.get()
        goal = self.goal_entry.get()

        # Basic validation
        if not name or not age or not goal:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        # Age must be numeric
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Invalid Age", "Age must be a number.")
            return

        user_data = {"name": name, "age": age, "goal": goal}

        with open(DATA_FILE, "r+") as file:
            users = json.load(file)
            # Remove existing user with same name (case-insensitive)
            users = [u for u in users if u["name"].lower() != name.lower()]
            users.append(user_data)
            file.seek(0)
            json.dump(users, file, indent=4)
            file.truncate()

        messagebox.showinfo("Success", "Profile saved.")
        self.display_profile(user_data)

    def delete_user(self):
        """
        Delete a user profile based on the entered name.
        Updates the JSON file after deletion.
        """
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Input Error", "Enter a name to delete.")
            return

        with open(DATA_FILE, "r+") as file:
            users = json.load(file)
            new_users = [u for u in users if u["name"].lower() != name.lower()]
            if len(new_users) == len(users):
                messagebox.showinfo("Not Found", "No profile found with that name.")
                return
            file.seek(0)
            json.dump(new_users, file, indent=4)
            file.truncate()

        messagebox.showinfo("Deleted", f"Profile for {name} deleted.")
        self.profile_display.config(state="normal")
        self.profile_display.delete(1.0, tk.END)
        self.profile_display.config(state="disabled")

    def load_user(self):
        """
        Load and display a user profile from JSON based on the name entered.
        """
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Input Error", "Enter a name to load.")
            return

        with open(DATA_FILE, "r") as file:
            users = json.load(file)
            for u in users:
                if u["name"].lower() == name.lower():
                    self.display_profile(u)
                    # Optionally clear fields after load
                    self.name_entry.delete(0, tk.END)
                    self.age_entry.delete(0, tk.END)
                    self.goal_entry.delete(0, tk.END)
                    return

        messagebox.showinfo("Not Found", "No profile found with that name.")

    def display_profile(self, user):
        """
        Display a user's profile details in the text box.
        :param user: Dictionary containing name, age, and goal
        """
        text = f"Name: {user['name']}\nAge: {user['age']}\nGoal: {user['goal']}"
        self.profile_display.config(state="normal")
        self.profile_display.delete(1.0, tk.END)
        self.profile_display.insert(tk.END, text)
        self.profile_display.config(state="disabled")
