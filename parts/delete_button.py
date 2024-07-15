import tkinter as tk


class DeleteButton(tk.Button):
    def __init__(self, parent: tk.Widget, command) -> None:
        super().__init__(parent, text="削除", command=command)
        self.pack(side=tk.RIGHT, padx=10, pady=10)
