import tkinter as tk
from tkinter import ttk

class OptionsDropdown(ttk.Combobox):
    """A widget to create dropdowns"""

    def __init__(self, root: tk.Tk | ttk.Frame, options: list, grid_config: dict, callback=None):
        super().__init__(root, values=options, state="readonly")
        self.grid(**grid_config)
        self.callback = callback

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.map(
            "Custom.TCombobox",
            fieldbackground=[("readonly", "lightblue")],
            background=[("active", "lightgray")],
            foreground=[("focus", "black")],
        )

        self.style.configure(
            "Custom.TCombobox",
            foreground="black",
            background="white",
            fieldbackground="lightgray",
            borderwidth=2,
            padding=5,
            font=("Arial", 12)
        )


        self.bind("<<ComboboxSelected>>", self.on_selection_change)
        self.current(0)


    def get_selection(self):
        return self.get()

    def on_selection_change(self, event):
        if self.callback:
            self.callback(self.get())



