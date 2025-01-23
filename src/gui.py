# src/gui.py
import asyncio
import tkinter as tk
from tkinter import ttk, messagebox

from .components.file_list import FileListComponent
from .components.controls import ControlsComponent
from .components.language_selector import LanguageSelectorComponent
from .translations import Translations
from .config import Config
from .ffmpeg_handler import FFmpegHandler
from .converter import AudioConverter


class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()

        # Initialize core components
        self.translations = Translations()
        self.config = Config()
        self.ffmpeg_handler = FFmpegHandler(self.config, self.translations)
        self.converter = AudioConverter(self.config, self.ffmpeg_handler, self.translations)

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.setup_components()
        self.check_ffmpeg()

    def setup_window(self):
        """Configure the main window"""
        # Make the window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_components(self):
        # Language selector
        self.lang_selector = LanguageSelectorComponent(
            self.main_frame,
            self.translations,
            self.update_translations
        )
        self.lang_selector.frame.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # File list
        self.file_list = FileListComponent(self.main_frame, self.translations)
        self.file_list.file_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        # Controls
        self.controls = ControlsComponent(self.main_frame, self.translations, self.file_list)
        self.controls.frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)

        # Set up conversion handlers
        self.controls.start_conversion = self.start_conversion
        self.controls.stop_conversion = self.stop_conversion

    def check_ffmpeg(self):
        if not self.ffmpeg_handler.check_installation():
            if messagebox.askyesno(
                    self.translations.get("error"),
                    self.translations.get("ffmpeg_required")
            ):
                asyncio.run(self.ffmpeg_handler.install(self.controls.update_status))

    async def convert_files(self):
        if not self.controls.get_output_path():
            messagebox.showerror(
                self.translations.get("error"),
                self.translations.get("select_folders")
            )
            return

        files_to_convert = self.file_list.get_selected_files()
        if not files_to_convert:
            messagebox.showinfo(
                self.translations.get("error"),
                self.translations.get("no_files")
            )
            return

        self.controls.set_converting_state(True)
        try:
            success = await self.converter.convert_files(
                files_to_convert,
                self.controls.get_output_path(),
                progress_callback=self.controls.update_progress,
                status_callback=self.controls.update_status
            )

            if success:
                messagebox.showinfo(
                    self.translations.get("success"),
                    self.translations.get("all_completed")
                )
        finally:
            self.controls.reset_progress()
            self.controls.set_converting_state(False)

    def start_conversion(self):
        import threading
        thread = threading.Thread(target=lambda: asyncio.run(self.convert_files()))
        thread.daemon = True
        thread.start()

    def stop_conversion(self):
        self.converter.cancel_conversion()
        self.controls.update_status(self.translations.get("conversion_cancelled"))

    def update_translations(self):
        self.root.title(self.translations.get("title"))
        self.file_list.translations = self.translations
        self.file_list.update_file_list()
        self.controls.update_translations()
        self.lang_selector.update_translations()