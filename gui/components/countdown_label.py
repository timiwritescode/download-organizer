import tkinter as tk
from tkinter import ttk

class CountdownLabel(ttk.Label):
    """The label component for displaying countdown"""
    def __init__(self, frame, root, timeout: int = 30):
        super().__init__(frame, text=f"Closing in {timeout} seconds", font=("Arial", 10))
        super().grid(column=0, row=1, columnspan=3, pady=(5, 10))


        self.timeout = timeout
        self._stop_countdown = False

        self.start_countdown()

    def start_countdown(self):
        """"""
        if self.timeout > 0:
            self.config(text=f"Closing in {self.timeout} sec...")
            self.timeout -= 1
            self.after(1000, self.start_countdown)
        else:
            self.winfo_toplevel().destroy()

    def stop_countdown(self):
        self.destroy()