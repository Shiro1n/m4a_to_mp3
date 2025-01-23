import src.pydub_override
import src.subprocess_handler
import logging
import os
import sys
import tkinter as tk
from tkinter import messagebox


def setup_tkdnd():
    try:
        import tkinterdnd2
        root = tkinterdnd2.TkinterDnD.Tk()
        logging.info("TkinterDnD initialized successfully.")
        return root
    except ImportError as e:
        logging.error(f"TkinterDnD initialization failed: {e}")
        root = tk.Tk()
        messagebox.showwarning(
            "Limited Functionality",
            "Drag and drop feature is not available.\nPlease use the browse button to select files."
        )
        return root


def main():
    from src.gui import ConverterGUI
    root = setup_tkdnd()
    root.title("M4A to MP3 Converter")
    root.minsize(600, 400)

    # Center window
    window_width, window_height = 800, 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    app = ConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()