import tkinter as tk


class BlueArea(tk.Frame):
    def __init__(self, parent: tk.Widget, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.pack(side=tk.BOTTOM, fill=tk.BOTH)
