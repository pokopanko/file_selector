import tkinter as tk


class fileEntry:
    def __init__(self, root):
        self.root = root
        self.create_widget()
        self.place_widget()

    def create_widget(self):
        # Create the frame for fileEntry section
        self.file_frame = tk.Frame(self.root)

        # Create widgets for the fileEntry section
        self.label = tk.Label(self.file_frame, text="ラベル")
        self.entry = tk.Entry(self.file_frame)
        self.button_a = tk.Button(
            self.file_frame, text="ボタンA", command=self.on_button_a_click
        )
        self.button_b = tk.Button(self.file_frame, text="ボタンB")

    def place_widget(self):
        # Pack the file_frame
        self.file_frame.pack()

        # Place widgets in the file_frame
        self.label.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_a.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_b.pack(side=tk.LEFT, padx=5, pady=5)

    def on_button_a_click(self):
        print("ボタンAが押されました")


class fileEntry2(fileEntry):
    def __init__(self, root):
        super().__init__(root)
        # Additional initialization if needed

    def create_widget(self):
        # Create additional frames
        self.left_frame = tk.Frame(self.root)
        self.center_frame = tk.Frame(self.root)
        self.right_frame = tk.Frame(self.root)

        # Create widgets for the additional frames
        self.button_x = tk.Button(self.left_frame, text="ボタンX")
        self.button_y = tk.Button(self.left_frame, text="ボタンY")
        self.label_t = tk.Label(self.center_frame, text="ラベルT")
        self.button_1 = tk.Button(self.right_frame, text="ボタン1")
        self.button_2 = tk.Button(self.right_frame, text="ボタン2")

        # 上書き
        self.file_frame = tk.Frame(self.center_frame)
        self.label = tk.Label(self.file_frame, text="ラベル")
        self.entry = tk.Entry(self.file_frame)
        self.button_a = tk.Button(
            self.file_frame, text="ボタンA", command=self.on_button_a_click
        )
        self.button_b = tk.Button(self.file_frame, text="ボタンB")

    def place_widget(self):
        # Pack the frames
        self.left_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        self.center_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        self.right_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)

        # Place buttons X and Y in the left frame
        self.button_x.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_y.pack(side=tk.LEFT, padx=5, pady=5)

        # Place fileEntry widgets in the center frame
        super().place_widget()

        # Place label_t in the center frame
        self.label_t.pack(side=tk.BOTTOM, padx=5, pady=5, anchor=tk.W)

        # Place buttons 1 and 2 in the right frame
        self.button_1.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_2.pack(side=tk.LEFT, padx=5, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tkinter Pack Example - fileEntry2")

    app = fileEntry2(root)

    root.mainloop()
