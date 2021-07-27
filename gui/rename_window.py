from child_window import ChildWindow
import tkinter


class RenameWindow(ChildWindow):
    def gui_init(self, window):
        if self.data.get("cid") is False:
            print("warning: ‘cid’ missed in rename window.")
            return
        if self.data.get("command") is False:
            print("warning: ‘command’ missed in rename window.")
            return
        frame = tkinter.Frame(window, bg="#323232", padx=10)
        frame.pack(expand=1, fill="x")
        tkinter.Label(frame, bg="#323232", fg="#A0A0A0", text="新文件名:").pack(side="left")
        self.data["new_name"] = tkinter.Text(frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                             highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                             insertbackground="#A0A0A0",
                                             height=1, width=25, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        self.data["new_name"].pack(side="left")
        button_enabled_img = tkinter.PhotoImage(file="img/button_enabled.png", width=110, height=50)
        self.data["img"] = button_enabled_img
        sure_button = tkinter.Label(frame, width=110, height=50, image=button_enabled_img, text="确认",
                                    bg="#323232", fg="#E4E4E4", compound="center", cursor="hand2")
        sure_button.pack(side="right")

        def return_disabled(evt):
            self.confirm(None)
            return "break"

        self.data["new_name"].bind("<Return>", return_disabled)
        sure_button.bind("<Button-1>", self.confirm)

        self.data["new_name"].focus_set()

    def confirm(self, evt):
        new_name = self.data["new_name"].get("1.0", "end-1c")
        self.data["command"](self.data["cid"], new_name)
        self.close()


