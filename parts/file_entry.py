import tkinter as tk
from tkinter import filedialog
from typing import List


class FileEntry(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        label_text: str,
        filetypes: List[tuple],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(parent, *args, **kwargs)
        self.file_path_var = tk.StringVar()
        self.label = tk.Label(self, text=label_text, width=10)
        self.label.pack(side=tk.LEFT, padx=10, pady=5, anchor=tk.W)
        self.entry = tk.Entry(self, textvariable=self.file_path_var, width=80)
        self.entry.pack(side=tk.LEFT, padx=10, pady=5)
        self.select_button = tk.Button(self, text="参照", command=self.select_file)
        self.select_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.clear_button = tk.Button(
            self, text="クリア", command=lambda: self.file_path_var.set("")
        )
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.filetypes = filetypes

    def select_file(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=self.filetypes)
        if file_path:
            self.file_path_var.set(file_path)
