import tkinter as tk


class AddButton(tk.Button):
    def __init__(self, parent: tk.Widget, command) -> None:
        super().__init__(parent, text="追加", command=command)
        self.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.E)
