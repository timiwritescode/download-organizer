import tkinter as tk
from tkinter import ttk

from gui.components import *
from gui import WindowBase, BaseFrame


class FileMoverWindow(WindowBase):
    def __init__(self, filename: str, timeout: int = 10):
        super().__init__(title="File Organizer")
        self.timeout = timeout
        # Main Frame
        self.mainframe = BaseFrame(self)

        # Label (Centered)
        custom_font = ("Arial", 13, "bold")
        text = f"Move file '{filename}'?"
        dialog_label = ttk.Label(self.mainframe, text=text, font=custom_font)
        dialog_label.grid(column=0, row=0, columnspan=2, sticky="ew", pady=(10, 20))  # Centered with space

        # Bottom-Right Button
        option_btn = ttk.Button(self.mainframe, cursor="hand2", text="Move", style="Accent.TButton", command=self._toggle_option_buttons)
        option_btn.grid(column=1, row=2, sticky="se", padx=10, pady=10)  # Bottom-right position

        # destination options buttons
        self.options_buttons: DestinationOptionButtons | None = None

        # Countdown Label
        self.countdown_label = CountdownLabel(self.mainframe, timeout)

        # Styling
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"), padding=5)

        self.countdown_label.start_countdown()




    def _toggle_option_buttons(self):
        """Creates destination buttons"""
        self.countdown_label.stop_countdown()
        if not self.options_buttons:
            self.options_buttons = DestinationOptionButtons(self.mainframe, row=5, column=3)
        else:
            self.options_buttons = None


# Example Usage
if __name__ == "__main__":
    window = FileMoverWindow("example.txt")
    window.open_window()
