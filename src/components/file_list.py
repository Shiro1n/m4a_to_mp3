import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES
import os


class FileListComponent:
    def __init__(self, parent, translations):
        self.parent = parent
        self.translations = translations
        self.selected_files = set()
        self.file_vars = {}
        self.setup_component()

    def setup_component(self):
        # File list frame with drag & drop
        self.file_frame = ttk.LabelFrame(self.parent, text=self.translations.get("files_to_convert"))
        self.file_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=5)
        self.file_frame.grid_columnconfigure(0, weight=1)
        self.file_frame.grid_rowconfigure(1, weight=1)  # Make row with canvas expandable

        self.setup_button_frame()
        self.create_scrollable_list()
        self.setup_drag_drop()

    def setup_button_frame(self):
        button_frame = ttk.Frame(self.file_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        ttk.Button(button_frame, text=self.translations.get("select_all"),
                   command=self.select_all_files).pack(side="left", padx=5)
        ttk.Button(button_frame, text=self.translations.get("clear_all"),
                   command=self.clear_all_files).pack(side="left", padx=5)
        ttk.Button(button_frame, text=self.translations.get("remove_selected"),
                   command=self.remove_selected_files).pack(side="left", padx=5)

    def create_scrollable_list(self):
        # Create a container frame for the canvas
        container = ttk.Frame(self.file_frame)
        container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        # Create a frame to contain the list items
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window inside canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Grid layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind mouse events
        self.canvas.bind('<Enter>', self.bind_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_mousewheel)

        # Bind canvas resize
        self.canvas.bind('<Configure>', self.on_canvas_configure)

    def bind_mousewheel(self, event=None):
        """Bind mousewheel to scrolling"""
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        # For Linux
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)

    def unbind_mousewheel(self, event=None):
        """Unbind mousewheel scrolling"""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        self.canvas.itemconfig("all", width=event.width)

    def setup_drag_drop(self):
        """Configure drag and drop for file list"""
        self.file_frame.drop_target_register(DND_FILES)
        self.canvas.drop_target_register(DND_FILES)
        self.scrollable_frame.drop_target_register(DND_FILES)

        for widget in (self.file_frame, self.canvas, self.scrollable_frame):
            widget.dnd_bind("<<Drop>>", self.handle_drop)
            widget.dnd_bind("<<DragEnter>>", self.on_drag_enter)
            widget.dnd_bind("<<DragLeave>>", self.on_drag_leave)

    def on_drag_enter(self, event):
        self.canvas.configure(relief="solid", borderwidth=2)

    def on_drag_leave(self, event):
        self.canvas.configure(relief="flat", borderwidth=0)

    def handle_drop(self, event):
        self.canvas.configure(relief="flat", borderwidth=0)
        try:
            if event.data.startswith("{") and event.data.endswith("}"):
                files = event.data[1:-1].split("} {")
            else:
                files = event.data.split()

            for file in files:
                if file.lower().endswith('.m4a'):
                    self.selected_files.add(file)

            self.update_file_list()

        except Exception as e:
            print(f"Error handling drop: {e}")

    def select_all_files(self):
        for var in self.file_vars.values():
            var.set(True)

    def clear_all_files(self):
        self.selected_files.clear()
        self.update_file_list()

    def remove_selected_files(self):
        to_remove = [file for file, var in self.file_vars.items() if var.get()]
        for file in to_remove:
            self.selected_files.discard(file)
        self.update_file_list()

    def update_file_list(self):
        # Clear existing items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.file_vars.clear()

        for i, file in enumerate(sorted(self.selected_files)):
            var = tk.BooleanVar(value=True)
            self.file_vars[file] = var

            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.grid(row=i, column=0, sticky="ew", pady=1)
            row_frame.grid_columnconfigure(0, weight=1)

            cb = ttk.Checkbutton(
                row_frame,
                text=os.path.basename(file),
                variable=var
            )
            cb.grid(row=0, column=0, sticky="w")

    def get_selected_files(self):
        return [file for file, var in self.file_vars.items() if var.get()]