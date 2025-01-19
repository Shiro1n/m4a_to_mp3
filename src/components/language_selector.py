import tkinter as tk
from tkinter import ttk


class LanguageSelectorComponent:
    def __init__(self, parent, translations, on_language_change):
        self.parent = parent
        self.translations = translations
        self.on_language_change = on_language_change

        # Create a frame to hold the language selector
        self.frame = ttk.Frame(parent)
        self.setup_component()

    def setup_component(self):
        self.label = ttk.Label(self.frame, text=self.translations.get("language"))
        self.label.pack(side="left", padx=(0, 5))

        self.lang_var = tk.StringVar(value="tr")
        self.lang_combo = ttk.Combobox(
            self.frame,
            textvariable=self.lang_var,
            values=["tr", "en"],
            width=5,
            state="readonly"
        )
        self.lang_combo.pack(side="left")
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

    def change_language(self, event=None):
        self.translations.current_lang = self.lang_var.get()
        if self.on_language_change:
            self.on_language_change()

    def get_current_language(self):
        return self.lang_var.get()

    def update_translations(self):
        """Update all text elements with current translations"""
        self.label.configure(text=self.translations.get("language"))