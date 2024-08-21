import tkinter as tk
from tkinter import ttk

from tkinterdnd2 import DND_FILES, TkinterDnD


class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Warning")
        self.result = None

        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        self.message_label = tk.Label(self, text="削除しますか", anchor="w")
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(
            self, text="今後表示しない", variable=self.checkbox_var
        )
        self.button_frame = tk.Frame(self)
        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.on_ok)
        self.cancel_button = tk.Button(
            self.button_frame, text="キャンセル", command=self.on_cancel
        )

    def _layout_widgets(self):
        self.message_label.pack(padx=10, pady=10, anchor="w")
        self.checkbox.pack(padx=10, pady=10, anchor="w")
        self.button_frame.pack(pady=10)
        self.ok_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

    def on_ok(self):
        self.result = True
        self.destroy()

    def on_cancel(self):
        self.result = False
        self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.result, self.checkbox_var.get()


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

        # ドラッグアンドドロップの設定
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.drop_file)

    def browse_file(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path.delete(0, tk.END)  # 古いパスをクリア
            self.file_path.insert(0, file_path)

    def clear_file(self):
        self.file_path.delete(0, tk.END)

    def add_file_entry(self):
        self.app.insert_file_entry(self)

    def remove_file_entry(self):
        # メッセージボックスの表示
        if not self.app.skip_messagebox:
            dialog = CustomMessageBox(self)
            result, skip_future = dialog.show()
            if skip_future:
                self.app.skip_messagebox = True

            if not result:  # ユーザーがキャンセルを選択した場合
                return

        self.app.remove_file_entry(self)

    def drop_file(self, event):
        files = self.app.tk.splitlist(event.data)
        self.app.handle_dropped_files(self, files)


class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.skip_messagebox = False  # メッセージボックスをスキップするかどうかを記録
        self.title("Tkinter Tool")
        self.setup_ui()
        self.file_entries = []
        self.create_file_entry()

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

    def create_file_entry(self):
        number = len(self.file_entries) + 1
        entry = FileEntry(self.inner_frame, self, number)
        entry.pack(fill=tk.X, pady=2)
        self.file_entries.append(entry)
        self.update_numbers()
        return entry  # 新しいエントリーを返す

    def insert_file_entry(self, current_entry):
        index = self.file_entries.index(current_entry) + 1
        number = len(self.file_entries) + 1
        entry = FileEntry(self.inner_frame, self, number)
        self.file_entries.insert(index, entry)

        self.repack_file_entries()
        self.update_numbers()

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

    def handle_dropped_files(self, target_entry, files):
        # ドロップされたエントリーのインデックスを取得
        index = self.file_entries.index(target_entry)

        for file_path in files:
            if index < len(self.file_entries):
                entry = self.file_entries[index]
                entry.file_path.delete(0, tk.END)  # 古いパスをクリア
                entry.file_path.insert(0, file_path)
            else:
                entry = self.create_file_entry()
                entry.file_path.delete(0, tk.END)  # 古いパスをクリア
                entry.file_path.insert(0, file_path)
            index += 1


if __name__ == "__main__":
    app = App()
    app.mainloop()
