import tkinter as tk


class DeleteButton(tk.Button):
    def __init__(self, parent: tk.Widget, command, *args, **kwargs) -> None:
        super().__init__(parent, text="削除", command=command, *args, **kwargs)
        self.pack(side=tk.RIGHT, padx=10, pady=10)
