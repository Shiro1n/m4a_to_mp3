import tkinter as tk
from tkinter import ttk, filedialog
import os
import json


class ControlsComponent:
    def __init__(self, parent, translations, file_list_component):
        self.parent = parent
        self.translations = translations
        self.file_list = file_list_component
        self.start_conversion = None  # Will be set by main GUI
        self.config_file = 'config.json'

        # Create a frame to hold all controls
        self.frame = ttk.Frame(parent)
        self.setup_component()
        self.load_saved_config()

    def load_saved_config(self):
        """Load saved output path from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if 'output_path' in config:
                        self.output_path.set(config['output_path'])
        except Exception as e:
            print(f"Error loading config: {e}")

    def save_config(self):
        """Save current output path to config file"""
        try:
            config = {'output_path': self.output_path.get()}
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")

    def setup_component(self):
        # Folder selection
        self.setup_folder_selection()

        # Concurrent conversions
        self.setup_conversion_controls()

        # Progress and status
        self.setup_progress_and_status()

    def setup_folder_selection(self):
        # Input folder (optional)
        self.input_label = ttk.Label(self.frame, text=self.translations.get("input_folder"))
        self.input_label.grid(row=0, column=0, sticky="w")

        self.input_path = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.input_path).grid(
            row=0, column=1, sticky="ew", padx=5)

        self.input_button = ttk.Button(self.frame, text=self.translations.get("browse"),
                                       command=self.browse_input)
        self.input_button.grid(row=0, column=2)

        # Output folder
        self.output_label = ttk.Label(self.frame, text=self.translations.get("output_folder"))
        self.output_label.grid(row=1, column=0, sticky="w")

        self.output_path = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.output_path).grid(
            row=1, column=1, sticky="ew", padx=5)

        self.output_button = ttk.Button(self.frame, text=self.translations.get("browse"),
                                        command=self.browse_output)
        self.output_button.grid(row=1, column=2)

        # Configure grid column weights
        self.frame.grid_columnconfigure(1, weight=1)

    def setup_conversion_controls(self):
        self.concurrent_label = ttk.Label(self.frame, text=self.translations.get("concurrent"))
        self.concurrent_label.grid(row=2, column=0, sticky="w")

        self.concurrent = ttk.Spinbox(self.frame, from_=1, to=10, width=5)
        self.concurrent.set(3)
        self.concurrent.grid(row=2, column=1, sticky="w", padx=5)

    def setup_progress_and_status(self):
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.frame, variable=self.progress_var, maximum=100)
        self.progress.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)

        self.status_var = tk.StringVar(value=self.translations.get("ready"))
        self.status = ttk.Label(self.frame, textvariable=self.status_var)
        self.status.grid(row=4, column=0, columnspan=3, sticky="w")

        self.convert_btn = ttk.Button(
            self.frame,
            text=self.translations.get("convert"),
            command=self._handle_convert_click
        )
        self.convert_btn.grid(row=5, column=0, columnspan=3, pady=10)

    def _handle_convert_click(self):
        """Handle convert button click"""
        if self.start_conversion:
            self.start_conversion()

    def update_translations(self):
        """Update all text elements with current translations"""
        self.input_label.configure(text=self.translations.get("input_folder"))
        self.output_label.configure(text=self.translations.get("output_folder"))
        self.concurrent_label.configure(text=self.translations.get("concurrent"))
        self.input_button.configure(text=self.translations.get("browse"))
        self.output_button.configure(text=self.translations.get("browse"))
        self.convert_btn.configure(text=self.translations.get("convert"))
        self.status_var.set(self.translations.get("ready"))

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_path.set(folder)
            self.add_files_from_folder(folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
            self.save_config()  # Save the output path when selected

    def add_files_from_folder(self, folder):
        m4a_files = [os.path.join(folder, f) for f in os.listdir(folder)
                     if f.lower().endswith('.m4a')]
        self.file_list.selected_files.update(m4a_files)
        self.file_list.update_file_list()

    def get_concurrent_value(self):
        return int(self.concurrent.get())

    def get_output_path(self):
        return self.output_path.get()

    def set_converting_state(self, is_converting):
        if is_converting:
            self.convert_btn.state(['disabled'])
        else:
            self.convert_btn.state(['!disabled'])

    def reset_progress(self):
        """Reset progress bar to zero"""
        self.progress_var.set(0)
        self.update()  # Ensure the UI updates

    def update_progress(self, value):
        """Update progress bar value"""
        self.progress_var.set(value)
        self.update()  # Ensure the UI updates immediately

    def update_status(self, status):
        """Update status text"""
        self.status_var.set(status)
        self.update()  # Ensure the UI updates immediately

    def update(self):
        """Force the frame to update"""
        self.frame.update_idletasks()
