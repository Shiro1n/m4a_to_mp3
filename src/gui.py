import asyncio
import tkinter as tk
from tkinter import ttk, messagebox
from src.components import FileListComponent, ControlsComponent, LanguageSelectorComponent
from src.translations import Translations
from src.converter import AudioConverter


class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.translations = Translations()
        self.converter = AudioConverter(self.translations)

        # Initialize main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Initialize components
        self.setup_components()
        self.check_ffmpeg()

    def setup_window(self):
        """Configure the main window."""
        self.root.title("M4A to MP3 Converter")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Make the window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_components(self):
        """Initialize and layout all GUI components."""
        # Language selector at the top right
        self.lang_selector = LanguageSelectorComponent(
            self.main_frame,
            self.translations,
            self.update_translations
        )
        self.lang_selector.frame.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # Controls component
        self.controls = ControlsComponent(
            self.main_frame,
            self.translations,
            None  # Will be set after file list is created
        )
        self.controls.frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)

        # File list component
        self.file_list = FileListComponent(
            self.main_frame,
            self.translations
        )
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.file_list.file_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        # Update controls with file list reference
        self.controls.file_list = self.file_list

        # Bind convert button to conversion method
        self.controls.start_conversion = self.start_conversion

    def check_ffmpeg(self):
        """Check for FFmpeg installation."""
        if not self.converter.check_ffmpeg():
            if messagebox.askyesno(
                    self.translations.get("error"),
                    self.translations.get("ffmpeg_required")
            ):
                self.converter.install_ffmpeg(self.controls.update_status)

    def update_translations(self):
        """Update all component translations."""
        # Update window title
        self.root.title(self.translations.get("title"))

        # Update all components
        self.file_list.translations = self.translations
        self.file_list.file_frame.configure(text=self.translations.get("files_to_convert"))
        self.file_list.update_file_list()

        # Update controls
        self.controls.translations = self.translations
        self.controls.update_translations()  # New method in ControlsComponent

        # Update language selector
        self.lang_selector.update_translations()

    async def convert_files(self):
        """Handle the file conversion process."""
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

        # Disable convert button during conversion
        self.controls.set_converting_state(True)

        try:
            # Start conversion
            success = await self.converter.convert_files(
                files_to_convert,
                self.controls.get_output_path(),
                self.controls.get_concurrent_value(),
                self.controls.update_progress,
                self.controls.update_status
            )

            # Show completion message
            if success:
                self.controls.update_status(self.translations.get("completed"))
                messagebox.showinfo(
                    self.translations.get("success"),
                    self.translations.get("all_completed")
                )
            else:
                self.controls.update_status(self.translations.get("error"))
        finally:
            # Always reset progress and re-enable button
            self.controls.reset_progress()
            self.controls.set_converting_state(False)

    def start_conversion(self):
        """Start the conversion process."""
        asyncio.run(self.convert_files())