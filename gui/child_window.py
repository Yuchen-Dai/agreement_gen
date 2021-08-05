import tkinter


class ChildWindow():
    # count = 0

    @staticmethod
    def check():
        return True
        # return __class__.count == 0

    def error_report(self, *error):
        self.master.error_report(error)

    def __init__(self, master, width=1260, height=900, minsize_x=400, minsize_y=400, resizable=False,
                 title="森源电气有限公司-合同管理", **data):
        if self.check():
            # __class__.count += 1
            super().__init__()
            self.master = master
            self.window = tkinter.Toplevel(master=master)
            self.window.option_add("*Font", "黑体 15")
            self.window.title(title)
            self.window.resizable(width=resizable, height=resizable)
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight() - 70
            self.window.geometry(
                "%sx%s+%d+%d" % (width, height, (screen_width - width) / 2, (screen_height - height) / 2))
            self.window.minsize(minsize_x, minsize_y)
            self.window.configure(bg="#323232")
            self.window.update()
            self.window.protocol("WM_DELETE_WINDOW", self.close)
            self.data = data
            self.window.grab_set()
            self.window.report_callback_exception = self.error_report
            self.gui_init(self.window)
            # self.window.mainloop()

    def close(self):
        # __class__.count -= 1
        self.window.destroy()
        self.master = None

    def gui_init(self, window):
        pass
