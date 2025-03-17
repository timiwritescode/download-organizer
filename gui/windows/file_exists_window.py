from tkinter import ttk
from gui import WindowBase, BaseFrame, directory_changes, OverwriteOptions
from gui.components.option_dropdown import OptionsDropdown


def set_write_option_as_keep_both():
    directory_changes.set_write_option()

def set_write_option_as_overwrite():
    directory_changes.set_write_option(OverwriteOptions.OVERWRITE)

class FileExistsWindow(WindowBase):
    """
    A GUI window to show that file exists in a particular directory
    and a prompt of whether to keep both or overwrite
    """

    def __init__(self, filename: str, directory: str, title="File Organizer"):
        super().__init__(title)
        self.frame = BaseFrame(self, number_of_rows=3, number_of_columns=3)
        # self.columnconfigure()
        custom_font = ("Arial", 10)
        text = f"File {filename} already exists in {directory}"

        self.prompt_label = ttk.Label(
            self.frame,
            text=text,
            font=custom_font,
            wraplength= self.winfo_width() - 50,
            justify="center"
            )

        self.prompt_label.grid(
            column=0,
            row=0,
            columnspan=3,
            sticky="ew",
            padx=5,)



        # buttons to ovewrite or
        self.write_options = ["overwrite", "keep both"]
        config = {
            "column": 1,
            "row": 1,
            "columnspan": 1,
            "padx": 0,
            "pady": 0
        }

        self.dropdown = OptionsDropdown(self.frame, self.write_options, config, callback=self.create_dropdown_options_button)

        self.action_button: ttk.Button | None = None


        self.cancel_button = ttk.Button(self.frame, text="cancel", cursor="hand2", command=self.handle_cancel_button_clicked_event)
        self.cancel_button.grid(
            column=0,
            row=2,
            sticky="sw",
            padx=10,
            pady=10
        )

        self.bind("<Configure>", self.update_wrap)

    def update_wrap(self, event):
        self.prompt_label.config(wraplength=event.width - 50)

    def handle_overwrite_button_clicked(self):
        directory_changes.set_write_option(OverwriteOptions.OVERWRITE)
        self.destroy()

    def handle_keep_both_option_clicked(self):
        directory_changes.set_write_option(OverwriteOptions.KEEP_BOTH)
        self.destroy()


    def handle_cancel_button_clicked_event(self):
        directory_changes.set_write_option(OverwriteOptions.KEEP_BOTH)
        self.destroy()

    def create_dropdown_options_button(self, selected_option):
        """Create or update button with selected dropdown option"""

        over_write_function = self.handle_keep_both_option_clicked \
                                    if selected_option == self.write_options[1] \
                                    else self.handle_overwrite_button_clicked

        if self.action_button:
            self.action_button.config(text=selected_option, command=over_write_function)
        else:

            self.action_button = ttk.Button(self.frame, text=selected_option, cursor="hand2", command=over_write_function)
            self.action_button.grid(
                column=2,
                row=2,
                sticky="se",
                padx=10,
                pady=10
            )


if __name__ == "__main__":
    window = FileExistsWindow("file", "directory")
    window.open_window()