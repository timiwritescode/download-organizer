import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from gui import directory_changes

class DestinationOptionButtons:
    def __init__(self, parent:ttk.Frame, window: tk.Tk, row: int, column: int):
        """Creates three buttons dynamically"""
        self._selectedPath = None

        self.parent = parent
        self.window = window
        self.show = False
        self.frame = None if not self.show else parent

        self.btn1 = ttk.Button(parent, text="Downloads", cursor="hand2", command=self.close_window)
        self.btn1.grid(column=column, row=row, sticky="ew", padx=5, pady=2)

        self.btn2 = ttk.Button(parent, text="Select destination", cursor="hand2", command=self.set_selected_filepath)
        self.btn2.grid(column=column, row=row + 2, sticky="ew", padx=5, pady=2)

        self.btn2 = ttk.Button(parent, text="Save to default", cursor="hand2", command=self.set_filepath_as_default)
        self.btn2.grid(column=column, row=row + 3, sticky="ew", padx=5, pady=2)

    def set_selected_filepath(self):
        selected_dir = askdirectory()
        directory_changes.set_selected_dir(selected_dir)
        self.close_window()

    def set_filepath_as_default(self):
        directory_changes.set_selected_dir("default")
        self.close_window()

    def close_window(self):
        self.window.destroy()



    # def get_selected_path(self):
    #     return self._selectedPath



class Button(ttk.Button):
    def __init__(self,
                 parent,
                 onclick = None,
                 cursor="hand2",
                 text="Select Destination"):
        super().__init__(parent, cursor=cursor, text=text, command=onclick)

