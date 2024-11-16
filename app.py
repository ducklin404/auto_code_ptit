import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import threading
import os
import json
from backend import Backend
from multiprocessing import freeze_support

class QuizSettingsApp:
    def __init__(self, root, backend):
        self.root = root
        self.backend = Backend()
        self.root.title("Code PTIT submit")

        # Define settings file path
        self.settings_file = os.path.join(os.getcwd(), 'settings.json')

        # Load settings if they exist
        self.load_settings()

        # Dropdown for language selection
        self.language_label = ttk.Label(root, text="Select Language:")
        self.language_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(root, textvariable=self.language_var)
        self.language_dropdown['values'] = ("Java", "Python")
        self.language_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Number input for max amount of questions
        self.max_questions_label = ttk.Label(root, text="Max Number of Questions:")
        self.max_questions_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.max_questions_var = tk.IntVar()
        self.max_questions_entry = ttk.Entry(root, textvariable=self.max_questions_var)
        self.max_questions_entry.grid(row=1, column=1, padx=10, pady=5)

        # Number input for min time between tasks
        self.min_time_label = ttk.Label(root, text="Min Time Between Tasks (seconds):")
        self.min_time_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.min_time_var = tk.IntVar()
        self.min_time_entry = ttk.Entry(root, textvariable=self.min_time_var)
        self.min_time_entry.grid(row=2, column=1, padx=10, pady=5)

        # Number input for max time between tasks
        self.max_time_label = ttk.Label(root, text="Max Time Between Tasks (seconds):")
        self.max_time_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.max_time_var = tk.IntVar()
        self.max_time_entry = ttk.Entry(root, textvariable=self.max_time_var)
        self.max_time_entry.grid(row=3, column=1, padx=10, pady=5)

        # Submit button
        self.submit_button = ttk.Button(root, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Login button
        self.login_button = ttk.Button(root, text="Login", command=self.start_login_process)
        self.login_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        # Load settings into UI
        self.load_ui_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                self.settings = json.load(file)
        else:
            self.settings = {}

    def load_ui_settings(self):
        if 'language' in self.settings:
            self.language_var.set(self.settings['language'])
        else:
            self.language_dropdown.current(0)

        self.max_questions_var.set(self.settings.get('max_questions', 0))
        self.min_time_var.set(self.settings.get('min_time', 0))
        self.max_time_var.set(self.settings.get('max_time', 0))

    def save_settings(self):
        self.settings = {
            'language': self.language_var.get(),
            'max_questions': self.max_questions_var.get(),
            'min_time': self.min_time_var.get(),
            'max_time': self.max_time_var.get()
        }
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings, file)

    def start_login_process(self):
        self.submit_button.config(state="disabled")
        login_thread = threading.Thread(target=self.backend.login)
        login_thread.start()

        # Create always-on-top window for login confirmation
        login_window = tk.Toplevel(self.root)
        login_window.title("Login Completed")
        login_window.attributes('-topmost', True)
        ttk.Label(login_window, text="Please finish logging in and click OK.").pack(padx=20, pady=20)
        ttk.Button(login_window, text="OK", command=lambda: self.login_finished(login_window)).pack(pady=10)

    def login_finished(self, login_window):
        self.backend.login_finished()
        self.submit_button.config(state="normal")
        login_window.destroy()

    def submit(self):
        language = self.language_var.get()
        max_questions = self.max_questions_var.get()
        min_time = self.min_time_var.get()
        max_time = self.max_time_var.get()

        if min_time > max_time:
            messagebox.showerror("Input Error", "Min time cannot be greater than max time.")
        else:
            # Save settings to file
            self.save_settings()
            threading.Thread(target=self.backend.run, args=(language, max_questions, min_time, max_time)).start()

if __name__ == "__main__":
    freeze_support()
    root = ThemedTk(theme="breeze")
    backend = Backend()
    app = QuizSettingsApp(root, backend)
    root.mainloop()