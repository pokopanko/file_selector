import tkinter as tk


class BlueArea(tk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.pack(side=tk.BOTTOM, fill=tk.BOTH)
