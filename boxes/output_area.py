import tkinter as tk


from boxes.file_selection_ui import FileSelectionUI


class OutputArea(tk.Frame):
    def __init__(self, parent: tk.Widget, *args, **kwargs) -> None:
        super().__init__(parent, relief=tk.RAISED, *args, **kwargs)
        self.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        self.label = tk.Label(self, text="", width=3)
        self.label.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.W)
        FileSelectionUI(self).pack(side=tk.TOP, fill=tk.X)
