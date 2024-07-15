import tkinter as tk

from boxes.blue_area import BlueArea
from boxes.output_area import OutputArea
from boxes.selection_area import SelectionArea
from parts.add_button import AddButton
from parts.scrollable_frame import ScrollableFrame
from parts.scrollable_frame import ScrollableFrame


class MainArea:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tkinter Tool")
        self.root.geometry("860x600")
        self.selection_areas = []
        self.create_widgets()

    def create_widgets(self) -> None:
        self.create_area_label("旧ファイル")
        self.create_scrollable_area()
        AddButton(self.root, command=self.add_selection_area)
        self.create_area_label("新ファイル")
        self.create_blue_area()
        self.add_selection_area()
        self.add_output_area()

    def add_output_area(self) -> None:
        OutputArea(self.blue_area)

    def create_scrollable_area(self) -> None:
        self.scrollable_frame = ScrollableFrame(self.root)
        self.scrollable_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_blue_area(self) -> None:
        self.blue_area = BlueArea(self.root)

    def create_area_label(self, text) -> None:
        self.area_label = tk.Label(self.root, text=text, anchor=tk.W)
        self.area_label.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.W)

    def add_selection_area(self) -> None:
        new_area_frame = SelectionArea(
            self.scrollable_frame.scrollable_frame,
            index=len(self.selection_areas),
            delete_command=lambda: self.remove_selection_area(new_area_frame),
        )
        self.selection_areas.append(new_area_frame)

    def remove_selection_area(self, area: tk.Widget) -> None:
        area.pack_forget()
        self.selection_areas.remove(area)
        self.rearrange_selection_labels()

    def rearrange_selection_labels(self) -> None:
        for index, area in enumerate(self.selection_areas):
            area.update_label(index)
