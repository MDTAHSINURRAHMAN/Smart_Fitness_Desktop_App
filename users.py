"""
UserScreen

This window lets users create and manage their profiles.
Main Features:
- Add name, age and a fitness goal
- Save and load those profiles
- See them displayed nicely in the app
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from tkinter.font import nametofont

# File where we store user profiles
data_file = "data/users.json"

# Make sure the data folder and file exist before we try using them
os.makedirs("data", exist_ok=True)
if not os.path.exists(data_file):
    with open(data_file, "w") as f:
        json.dump([], f)

class UserScreen:
    """
    User profile management window.
    """

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("User Management")
        self.window.geometry("520x420")

        # Set global font
        default_font = nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=11)

        # === Title/Header ===
        ttk.Label(self.window, text="User Profile Manager", font=("Helvetica", 14, "bold")).pack(pady=10)

        # === Form Section ===
        form = ttk.Frame(self.window, padding=10)
        form.pack()

        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(form, text="Age:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(form, text="Goal (e.g., weight loss):").grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.name = ttk.Entry(form, width=30)
        self.age = ttk.Entry(form, width=30)
        self.goal = ttk.Entry(form, width=30)

        self.name.grid(row=0, column=1, padx=5, pady=5)
        self.age.grid(row=1, column=1, padx=5, pady=5)
        self.goal.grid(row=2, column=1, padx=5, pady=5)

        # === Action Buttons ===
        btn_frame = ttk.Frame(self.window, padding=10)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Save Profile", command=self.save_user).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="Delete Profile", command=self.delete_user).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(btn_frame, text="Load Profile", command=self.load_user).grid(row=0, column=2, padx=10, pady=5)

        # === Profile Display Output ===
        display_frame = ttk.Frame(self.window, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        self.profile_display = tk.Text(
            display_frame,
            height=8,
            wrap="word",
            font=("Helvetica", 11),
            bg=self.window.cget("bg"),
            relief="solid",
            bd=1,
            padx=10,
            pady=10
        )
        self.profile_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.profile_display.configure(state="disabled")

    def save_user(self):
        """
        Collect form input and save/update it in the JSON file.
        """
        name = self.name.get()
        age = self.age.get()
        goal = self.goal.get()

        if not name or not age or not goal:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Invalid Age", "Age must be a number.")
            return

        user_data = {"name": name, "age": age, "goal": goal}

        with open(data_file, "r+") as file:
            users = json.load(file)
            users = [u for u in users if u["name"].lower() != name.lower()]
            users.append(user_data)
            file.seek(0)
            json.dump(users, file, indent=4)
            file.truncate()

        messagebox.showinfo("Success", "Profile saved.")
        self.display_profile(user_data)

    def delete_user(self):
        """
        Delete a user profile from the file based on entered name.
        """
        name = self.name.get()
        if not name:
            messagebox.showwarning("Input Error", "Enter a name to delete.")
            return

        with open(data_file, "r+") as file:
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
        Load and display a user profile by name.
        """
        name = self.name.get()
        if not name:
            messagebox.showwarning("Input Error", "Enter a name to load.")
            return

        with open(data_file, "r") as file:
            users = json.load(file)
            for u in users:
                if u["name"].lower() == name.lower():
                    self.display_profile(u)
                    self.name.delete(0, tk.END)
                    self.age.delete(0, tk.END)
                    self.goal.delete(0, tk.END)
                    return

        messagebox.showwarning("Not Found", "No profile found with that name.")

    def display_profile(self, user):
        """
        Show selected user profile in the text display area.
        """
        text = f"Name: {user['name']}\nAge: {user['age']}\nGoal: {user['goal']}"
        self.profile_display.config(state="normal")
        self.profile_display.delete(1.0, tk.END)
        self.profile_display.insert(tk.END, text)
        self.profile_display.config(state="disabled")
