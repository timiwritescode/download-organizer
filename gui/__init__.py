import tkinter as tk
from doctest import master
from tkinter import ttk
from enum import Enum

class OverwriteOptions(Enum):
    OVERWRITE = "overwrite"
    KEEP_BOTH = "keep_both"

class DirectoryModifications:
    _SELECTED_dir: str | None = None
    _SELECTED_WRITE_OPTION: OverwriteOptions | None = None


    def set_selected_dir(self, dir: str):
        self._SELECTED_dir = dir

    def set_write_option(self, option:OverwriteOptions = OverwriteOptions.KEEP_BOTH):
        """Setter to set the write option for case when a file with the same name
        as the file about to be written already exists in the same directory.
        It defaults to keeping both to preserve data
        """

        self._SELECTED_WRITE_OPTION = option

    def get_write_option(self):
        """Getter to get the write options decided"""
        return self._SELECTED_WRITE_OPTION

    def get_selected_dir(self):
        return self._SELECTED_dir

    def clear_data_cache(self):
        self._SELECTED_dir = None
        self._SELECTED_WRITE_OPTION = None
        print("Cleared data cache")

directory_changes = DirectoryModifications()


class WindowBase(tk.Tk):
    def __init__(self, title: str, geometry: str = "400x200", min_width=400, min_height=200):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.minsize(min_width, min_height)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def open_window(self):
        self.mainloop()


class BaseFrame(ttk.Frame):
    def __init__(self, root: tk.Tk, row_number=0, column_number=0, number_of_rows = 1, number_of_columns =1, padding=0, border_width=0):
        super().__init__(
            root,
            padding=padding,
            borderwidth=border_width,
            relief="ridge")

        self.grid(column=column_number, row=row_number, sticky="nsew")
        for r in range(number_of_rows):
            self.grid_rowconfigure(r, weight=1)
        for c in range(number_of_columns):
            self.grid_columnconfigure(c, weight=1)

        # self.columnconfigure(0, weight=1)


        # self.rowconfigure(0, weight=1)
