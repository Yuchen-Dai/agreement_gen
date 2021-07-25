import tkinter
from child_window import ChildWindow


class WarningWindow(ChildWindow):
    def __init__(self, master, text, width=350, height=150, minsize_x=300, minsize_y=150, resizable=False):
        self.text = text
        super().__init__(master, width, height, minsize_x, minsize_y, resizable)

    def gui_init(self, window):
        sure_img = tkinter.PhotoImage(file="img/button_enabled.png", width=110, height=50)
        sure_button = tkinter.Label(window, width=110, height=50, image=sure_img, text="确定",
                                    bg="#323232", fg="#E4E4E4", compound="center", cursor="hand2")
        self.data["sure_img"] = sure_img

        def cancel(evt):
            self.close()
        sure_button.bind("<Button-1>", cancel)
        tkinter.Frame(window, bg="#323232", height=15).pack(side="bottom")
        sure_button.pack(side="bottom", fill="x")
        label = tkinter.Label(window, text=self.text, bg="#323232", fg="#A0A0A0", font="宋体 12")
        label.pack(expand=1)
