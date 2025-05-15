import tkinter as tk
from tkinter import ttk
import sv_ttk

root = tk.Tk()
root.title("Sun Valley Test")
root.geometry("300x150")

sv_ttk.set_theme("dark")

ttk.Label(root, text="Sun Valley Theme Active", font=("Segoe UI", 12)).pack(pady=20)
ttk.Button(root, text="Test Button").pack()

root.mainloop()
