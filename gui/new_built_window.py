import tkinter
from child_window import ChildWindow


class NewBuiltWindow(ChildWindow):
    new_built_count = 0

    @staticmethod
    def check():
        return __class__.new_built_count < 1

    def close(self):
        __class__.new_built_count -= 1

    def gui_init(self, window):
        __class__.new_built_count += 1