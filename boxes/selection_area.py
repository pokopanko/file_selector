import tkinter as tk

from parts.delete_button import DeleteButton


class SelectionArea(tk.Frame):
    def __init__(self, parent: tk.Widget, index: int, delete_command=None) -> None:
        super().__init__(parent, relief=tk.RAISED)
        self.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        self.label = tk.Label(self, text=f"No.{index + 1}", width=3)
        self.label.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.W)
        if delete_command:
            DeleteButton(self, delete_command)
        FileSelectionUI(self).pack(side=tk.TOP, fill=tk.X)

    def update_label(self, index: int) -> None:
        self.label.config(text=f"No.{index + 1}")
