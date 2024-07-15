import tkinter as tk


class AreaLabel:
    def __init__(self, root: tk.Tk, text: str) -> None:
        self.label = tk.Label(root, text=text, anchor=tk.W)
        self.label.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.W)
