import tkinter as tk

from parts.file_entry import FileEntry


class FileSelectionUI(tk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.excel_frame = tk.Frame(self)
        self.excel_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        self.powerpoint_frame = tk.Frame(self)
        self.powerpoint_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        self.create_file_entries()

    def create_file_entries(self) -> None:
        FileEntry(
            self.excel_frame, "テキストファイル:", [("Text files", "*.txt")]
        ).pack(side=tk.TOP, fill=tk.X)
        FileEntry(
            self.powerpoint_frame,
            "パワポファイル:",
            [("PowerPoint files", "*.pptx;*.ppt")],
        ).pack(side=tk.TOP, fill=tk.X)
