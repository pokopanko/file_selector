import tkinter as tk
from tkinter import filedialog, ttk


class FileEntry(tk.Frame):
    def __init__(self, parent, app, number, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app  # 親アプリケーションの参照を保持

        self.number = tk.Label(self, text=f"No. {number}")
        self.number.pack(side=tk.LEFT)

        self.file_path = tk.Entry(self, width=50)
        self.file_path.pack(side=tk.LEFT, padx=(5, 5))

        self.browse_button = tk.Button(self, text="参照", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=(5, 5))

        self.clear_button = tk.Button(self, text="クリア", command=self.clear_file)
        self.clear_button.pack(side=tk.LEFT, padx=(5, 5))

        self.add_button = tk.Button(self, text="追加", command=self.add_file_entry)
        self.add_button.pack(side=tk.LEFT, padx=(5, 5))

        self.remove_button = tk.Button(
            self, text="削除", command=self.remove_file_entry
        )
        self.remove_button.pack(side=tk.LEFT, padx=(5, 5))

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path.insert(0, file_path)

    def clear_file(self):
        self.file_path.delete(0, tk.END)

    def add_file_entry(self):
        self.app.insert_file_entry(self)

    def remove_file_entry(self):
        self.app.remove_file_entry(self)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter Tool")
        self.setup_ui()
        self.file_entries = []
        self.add_file_entry()

    def setup_ui(self):
        # Old File Title
        self.old_file_title = tk.Label(self, text="旧ファイル", anchor="w")
        self.old_file_title.pack(fill=tk.X)

        # Old File Area
        self.old_file_area = tk.Frame(self, bd=2, relief=tk.SOLID)
        self.old_file_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # TXT File Title
        self.txt_file_title = tk.Label(
            self.old_file_area, text="TXTファイル", anchor="w"
        )
        self.txt_file_title.pack(fill=tk.X)

        # Scrollable Area
        self.scrollable_frame = ttk.Frame(self.old_file_area)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.scrollable_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.scrollable_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

    def add_file_entry(self):
        number = len(self.file_entries) + 1
        entry = FileEntry(self.inner_frame, self, number)
        entry.pack(fill=tk.X, pady=2)
        self.file_entries.append(entry)
        self.update_numbers()

    def insert_file_entry(self, current_entry):
        index = self.file_entries.index(current_entry) + 1
        number = len(self.file_entries) + 1
        entry = FileEntry(self.inner_frame, self, number)
        self.file_entries.insert(index, entry)

        self.repack_file_entries()
        self.update_numbers()

        print(">>>", self.file_entries)

    def remove_file_entry(self, entry):
        entry.pack_forget()
        entry.destroy()
        self.file_entries.remove(entry)
        self.update_numbers()

    def repack_file_entries(self):
        for widget in self.inner_frame.winfo_children():
            widget.pack_forget()

        for entry in self.file_entries:
            entry.pack(fill=tk.X, pady=2)

    def update_numbers(self):
        for i, entry in enumerate(self.file_entries):
            entry.number.config(text=f"No. {i + 1}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
