import os
import sys
import tkinter as tk
from tkinter import messagebox


def setup_tkdnd():
    """Setup TkinterDnD2 library paths"""
    try:
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        # Import tkinterdnd2 after setting up paths
        import tkinterdnd2
        return tkinterdnd2.TkinterDnD.Tk()
    except Exception as e:
        root = tk.Tk()
        messagebox.showwarning(
            "Limited Functionality",
            "Drag and drop feature is not available.\nPlease use the browse button to select files."
        )
        return root


def main():
    from src import ConverterGUI

    root = setup_tkdnd()
    root.title("M4A to MP3 Converter")

    # Set minimum window size
    root.minsize(600, 400)

    # Center the window on screen
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    app = ConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()