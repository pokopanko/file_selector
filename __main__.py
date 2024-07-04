import tkinter as tk
from tkinter import filedialog
from typing import List


class ScrollableFrame(tk.Frame):
    """
    Canvas内にスクロール可能なフレームを作成するクラス。

    Attributes:
        canvas (tk.Canvas): スクロール領域を持つキャンバスウィジェット。
        scrollbar (tk.Scrollbar): 垂直方向のスクロールバー。
        scrollable_frame (tk.Frame): スクロール可能なフレーム。
    """

    def __init__(self, parent: tk.Widget, *args, **kwargs) -> None:
        """
        ScrollableFrameの初期化。

        Args:
            parent (tk.Widget): 親ウィジェット。
            *args: 可変長位置引数。
            **kwargs: キーワード引数。
        """
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_canvas_configure(self, event: tk.Event) -> None:
        """
        Canvasウィジェットのサイズ変更時にスクロール領域を設定する。

        Args:
            event (tk.Event): イベントオブジェクト。
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event: tk.Event) -> None:
        """
        スクロール可能なフレームのサイズ変更時にスクロール領域を設定する。

        Args:
            event (tk.Event): イベントオブジェクト。
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event: tk.Event) -> None:
        """
        マウスホイールでスクロールするためのメソッド。

        Args:
            event (tk.Event): マウスイベントオブジェクト。
        """
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class MyApp:
    """
    Tkinterツールのメインアプリケーションクラス。

    Attributes:
        root (tk.Tk): Tkinterのルートウィンドウ。
        scrollable_frame (ScrollableFrame): スクロール可能なフレーム。
        blue_area (tk.Frame): 青い背景のエリア。
        old_files_label (tk.Label): "旧ファイル"ラベル。
        add_button (tk.Button): 追加ボタン。
        selection_areas (List[tk.Frame]): 選択エリアのリスト。
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        MyAppの初期化。

        Args:
            root (tk.Tk): Tkinterのルートウィンドウ。
        """
        self.root = root
        self.root.title("Tkinter Tool")
        self.root.geometry("860x600")

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        アプリケーションのウィジェットを作成するメソッド。
        """
        self.selection_areas = []
        self.create_area_label("旧ファイル")
        self.create_scrollable_area()
        self.create_add_button()
        self.create_area_label("新ファイル")
        self.create_blue_area()
        self.add_selection_area()  # 初期の選択エリアを追加する
        self.add_output_area()

    def add_output_area(self) -> None:
        output_frame = tk.Frame(self.blue_area, relief=tk.RAISED)
        output_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        label = tk.Label(output_frame, text="", width=3)
        label.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.W)
        self.create_file_selection_ui(
            output_frame
        )  # 青い背景エリアにもファイル選択UIを追加する

    def create_scrollable_area(self) -> None:
        """
        スクロール可能なフレームを作成するメソッド。
        """
        self.scrollable_frame = ScrollableFrame(self.root)
        self.scrollable_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_blue_area(self) -> None:
        """
        青い背景のエリアを作成するメソッド。
        """
        self.blue_area = tk.Frame(self.root)
        self.blue_area.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def create_area_label(self, text) -> None:
        """
        エリアのラベルを作成するメソッド。
        """
        self.area_label = tk.Label(self.root, text=text, anchor=tk.W)
        self.area_label.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.W)

    def create_add_button(self) -> None:
        """
        追加ボタンを作成するメソッド。
        """
        self.add_button = tk.Button(
            self.root, text="追加", command=self.add_selection_area
        )
        self.add_button.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.E)

    def add_selection_area(self) -> None:
        """
        選択エリアを追加するメソッド。
        """
        new_area_frame = tk.Frame(
            self.scrollable_frame.scrollable_frame,
            relief=tk.RAISED,
        )
        new_area_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        label_text = f"No.{len(self.selection_areas) + 1}"
        label = tk.Label(new_area_frame, text=label_text, width=3)
        label.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.W)

        if len(self.selection_areas) > 0:
            self.create_delete_button(new_area_frame)

        self.create_file_selection_ui(new_area_frame)

        self.selection_areas.append(new_area_frame)

    def create_file_selection_ui(self, parent: tk.Widget) -> None:
        """
        ファイル選択UIを作成するメソッド。

        Args:
            parent (tk.Widget): 親ウィジェット。
        """
        excel_frame = tk.Frame(parent)
        excel_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        powerpoint_frame = tk.Frame(parent)
        powerpoint_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        self.create_file_entry(
            excel_frame, "テキストファイル:", [("Text files", "*.txt")]
        )
        self.create_file_entry(
            powerpoint_frame, "パワポファイル:", [("PowerPoint files", "*.pptx;*.ppt")]
        )

    def create_file_entry(
        self, parent: tk.Widget, label_text: str, filetypes: List[tuple]
    ) -> None:
        """
        ファイル選択エントリーを作成するメソッド。

        Args:
            parent (tk.Widget): 親ウィジェット。
            label_text (str): ラベルテキスト。
            filetypes (List[tuple]): ファイルタイプのリスト。
        """
        label = tk.Label(parent, text=label_text, width=10)
        label.pack(side=tk.LEFT, padx=10, pady=5, anchor=tk.W)

        file_path_var = tk.StringVar()
        entry = tk.Entry(parent, textvariable=file_path_var, width=80)
        entry.pack(side=tk.LEFT, padx=10, pady=5)

        def select_file():
            file_path = filedialog.askopenfilename(filetypes=filetypes)
            if file_path:
                file_path_var.set(file_path)

        select_button = tk.Button(parent, text="参照", command=select_file)
        select_button.pack(side=tk.LEFT, padx=5, pady=5)

        clear_button = tk.Button(
            parent, text="クリア", command=lambda: file_path_var.set("")
        )
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_delete_button(self, parent: tk.Widget) -> None:
        """
        削除ボタンを作成するメソッド。

        Args:
            parent (tk.Widget): 親ウィジェット。
        """
        delete_button = tk.Button(
            parent, text="削除", command=lambda: self.remove_selection_area(parent)
        )
        delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def remove_selection_area(self, area: tk.Widget) -> None:
        """
        選択エリアを削除するメソッド。

        Args:
            area (tk.Widget): 削除する選択エリアのウィジェット。
        """
        area.pack_forget()
        self.selection_areas.remove(area)
        self.rearrange_selection_labels()

    def rearrange_selection_labels(self) -> None:
        """
        選択エリアのラベルを再配置するメソッド。
        """
        for index, area in enumerate(self.selection_areas):
            label_text = f"No.{index + 1}"
            area.winfo_children()[0].config(text=label_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
